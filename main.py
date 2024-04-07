from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # Import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Initialize CORS

DATABASE = 'mood_tracker.db'

# Initialize the database
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE moods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    # Serve the HTML page
    return render_template('index.html')

@app.route('/submit_mood', methods=['POST'])
def submit_mood():
    mood = request.json.get('mood')
    if mood:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO moods (mood) VALUES (?)', (mood,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200
    return jsonify({'status': 'error', 'message': 'Mood not provided'}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
