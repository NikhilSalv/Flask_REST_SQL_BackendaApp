from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime


app = Flask(__name__)
DATABASE = 'sportsbook.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/sports', methods=['POST'])
def create_sport():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO sports (name, slug, active) VALUES (?, ?, ?)",
                (data['name'], data['slug'], data['active']))
    conn.commit()
    return jsonify({"id": cur.lastrowid}), 201


if __name__ == "__main__":
    app.run(debug=True)
