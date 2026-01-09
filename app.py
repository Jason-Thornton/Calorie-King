from flask import Flask, request, jsonify, send_file, session, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import anthropic
import base64
import os
import json
from PIL import Image
import io
import database

app = Flask(__name__)
CORS(app)
# Use environment variable for secret key in production, random for development
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24).hex())

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user_data = database.get_user_by_id(int(user_id))
    if user_data:
        return User(user_data['id'], user_data['username'])
    return None

# You'll need to set your Anthropic API key
# Get one at: https://console.anthropic.com/
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

if not ANTHROPIC_API_KEY:
    print("WARNING: ANTHROPIC_API_KEY environment variable not set!")
    print("Set it with: set ANTHROPIC_API_KEY=your-key-here")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@app.route('/')
def index():
    return send_file('food-analyzer.html')

@app.route('/login-page')
def login_page():
    return send_file('login.html')

@app.route('/history')
@login_required
def history_page():
    return send_file('history.html')

# Authentication endpoints
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    user_id = database.create_user(username, password)

    if user_id:
        user = User(user_id, username)
        login_user(user)
        return jsonify({'success': True, 'username': username})
    else:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user_data = database.verify_password(username, password)

    if user_data:
        user = User(user_data['id'], user_data['username'])
        login_user(user)
        return jsonify({'success': True, 'username': username})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'success': True})

@app.route('/api/current-user')
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'username': current_user.username})
    else:
        return jsonify({'authenticated': False})

@app.route('/analyze', methods=['POST'])
def analyze_food():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    
    try:
        # Read and encode image
        image_data = image_file.read()
        
        # Convert to base64
        base64_image = base64.standard_b64encode(image_data).decode('utf-8')
        
        # Determine media type
        media_type = image_file.content_type or 'image/jpeg'
        
        # Call Claude API
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": """Analyze this food image and provide a detailed breakdown of the meal. 
                            
Identify each food item visible in the image, estimate the portion size, and calculate approximate calories.

Return your response in this EXACT JSON format (no markdown, no code blocks, just raw JSON):
{
    "foods": [
        {
            "name": "Food name",
            "portion": "Estimated portion (e.g., '6 oz', '1 cup', '1/2 cup')",
            "calories": 280
        }
    ],
    "total_calories": 500
}

Be specific with food names (e.g., "Grilled chicken breast" not just "chicken"). Provide realistic portion estimates and calorie counts based on standard nutritional data."""
                        }
                    ],
                }
            ],
        )
        
        # Extract the response text
        response_text = message.content[0].text
        
        # Parse JSON response
        # Claude sometimes wraps JSON in markdown, so let's handle that
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()
        
        result = json.loads(response_text)

        # Save meal to database if user is logged in
        meal_name = request.form.get('meal_name', 'Unnamed Meal')
        should_save = request.form.get('save_meal', 'false') == 'true'

        if current_user.is_authenticated and should_save:
            # Check if user provided edited food data
            foods_data_str = request.form.get('foods_data')
            total_calories_str = request.form.get('total_calories')

            if foods_data_str and total_calories_str:
                # Use edited data from user
                foods_to_save = json.loads(foods_data_str)
                total_cal_to_save = int(total_calories_str)
            else:
                # Use AI analysis data
                foods_to_save = result['foods']
                total_cal_to_save = result['total_calories']

            # Save with image data
            database.save_meal(
                user_id=current_user.id,
                meal_name=meal_name,
                foods=foods_to_save,
                total_calories=total_cal_to_save,
                image_data=base64_image
            )
            result['saved'] = True

        return jsonify(result)
    
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response was: {response_text}")
        return jsonify({
            'error': 'Failed to parse AI response',
            'details': str(e)
        }), 500
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'error': 'Failed to analyze image',
            'details': str(e)
        }), 500

# Re-analyze single food item
@app.route('/api/reanalyze-item', methods=['POST'])
def reanalyze_item():
    data = request.json
    food_name = data.get('food_name')

    if not food_name:
        return jsonify({'error': 'Food name required'}), 400

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=512,
            messages=[
                {
                    "role": "user",
                    "content": f"""For the food item "{food_name}", provide the typical portion size and calorie count.

Return your response in this EXACT JSON format (no markdown, no code blocks, just raw JSON):
{{
    "portion": "typical portion size (e.g., '1 medium', '1 cup', '6 oz')",
    "calories": 250
}}

Be specific and use standard nutritional data."""
                }
            ]
        )

        response_text = message.content[0].text

        # Parse JSON response
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0].strip()
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0].strip()

        result = json.loads(response_text)
        return jsonify(result)

    except Exception as e:
        print(f"Error re-analyzing item: {e}")
        return jsonify({'error': 'Failed to re-analyze item'}), 500

# Meal history endpoints
@app.route('/api/meals', methods=['GET'])
@login_required
def get_meals():
    meals = database.get_user_meals(current_user.id)
    return jsonify({'meals': meals})

@app.route('/api/meals/<int:meal_id>', methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    success = database.delete_meal(meal_id, current_user.id)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Meal not found or unauthorized'}), 404

if __name__ == '__main__':
    print("=" * 50)
    print("Food Analyzer Server Starting!")
    print("=" * 50)
    print("\nIMPORTANT: Set your Anthropic API key:")
    print("  set ANTHROPIC_API_KEY=your-key-here")
    print("\nGet your API key at: https://console.anthropic.com/")
    print("\nServer will run at: http://localhost:5000")
    print("=" * 50)
    # Use PORT environment variable for deployment, default to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
