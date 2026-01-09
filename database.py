import sqlite3
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'calorie_king.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables"""
    conn = get_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create meals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            meal_name TEXT,
            foods JSON NOT NULL,
            total_calories INTEGER NOT NULL,
            image_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

# User functions
def create_user(username, password):
    """Create a new user"""
    conn = get_db()
    cursor = conn.cursor()

    password_hash = generate_password_hash(password)

    try:
        cursor.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    return dict(user) if user else None

def verify_password(username, password):
    """Verify user password"""
    user = get_user_by_username(username)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

# Meal functions
def save_meal(user_id, meal_name, foods, total_calories, image_data=None):
    """Save a meal to the database"""
    conn = get_db()
    cursor = conn.cursor()

    foods_json = json.dumps(foods)

    cursor.execute(
        '''INSERT INTO meals (user_id, meal_name, foods, total_calories, image_data)
           VALUES (?, ?, ?, ?, ?)''',
        (user_id, meal_name, foods_json, total_calories, image_data)
    )

    conn.commit()
    meal_id = cursor.lastrowid
    conn.close()

    return meal_id

def get_user_meals(user_id, limit=50):
    """Get all meals for a user"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT id, meal_name, foods, total_calories, image_data, created_at
           FROM meals
           WHERE user_id = ?
           ORDER BY created_at DESC
           LIMIT ?''',
        (user_id, limit)
    )

    meals = cursor.fetchall()
    conn.close()

    result = []
    for meal in meals:
        meal_dict = dict(meal)
        meal_dict['foods'] = json.loads(meal_dict['foods'])
        result.append(meal_dict)

    return result

def delete_meal(meal_id, user_id):
    """Delete a meal (only if it belongs to the user)"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        'DELETE FROM meals WHERE id = ? AND user_id = ?',
        (meal_id, user_id)
    )

    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()

    return deleted

# Initialize database on import
init_db()
