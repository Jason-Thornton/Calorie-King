from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import anthropic
import base64
import os
import json
from PIL import Image
import io

app = Flask(__name__)
CORS(app)

# You'll need to set your Anthropic API key
# Get one at: https://console.anthropic.com/
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', 'your-api-key-here')

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@app.route('/')
def index():
    return send_file('food-analyzer.html')

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
            model="claude-sonnet-4-20250514",
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

if __name__ == '__main__':
    print("=" * 50)
    print("🥗 Food Analyzer Server Starting!")
    print("=" * 50)
    print("\nIMPORTANT: Set your Anthropic API key:")
    print("  export ANTHROPIC_API_KEY='your-key-here'")
    print("\nGet your API key at: https://console.anthropic.com/")
    print("\nServer will run at: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
