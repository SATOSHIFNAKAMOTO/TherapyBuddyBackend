from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'mood_tracker.db'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS moods (
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
    data = request.get_json()
    mood = data.get('mood') if data else None

    if mood:
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO moods (mood) VALUES (?)', (mood,))
            conn.commit()
            return jsonify({'status': 'success'}), 200
        except sqlite3.Error as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        finally:
            if conn:
                conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'Mood not provided'}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
