from flask import Flask, Blueprint, request, jsonify 
import sqlite3
from datetime import datetime

api = Blueprint('api', __name__)

# SQLite database configuration
DATABASE = 'mood_tracker.db'

# Create a connection to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@api.route('/submit_mood', methods=['POST'])
def submit_mood():
    print('Received request data:', request.get_json())
    data = request.get_json()

    if not data:  
        print("No JSON data received")
        return jsonify({'status': 'error', 'message': 'Invalid request. No data received.'}), 400

    mood = data.get('mood')
    print('Extracted mood:', mood) 

    if mood:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = get_db_connection()
        print('Database connection established')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO moods (mood, timestamp) VALUES (?, ?)', (mood, timestamp))
        print('Mood inserted into the database')
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Mood saved successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Mood not provided'}), 400
