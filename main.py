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

@app.route('/get_moods', methods=['GET'])
def get_moods():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM moods ORDER BY timestamp DESC')
    moods = cursor.fetchall()

    # Convert the response to a list of dicts, which can be easily turned into JSON
    moods_list = [dict(row) for row in moods]

    conn.close()
    return jsonify(moods_list)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))  # Get port from environment, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)  # Bind to all interfaces
