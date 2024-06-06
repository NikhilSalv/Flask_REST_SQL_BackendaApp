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

@app.route('/sports', methods=['GET'])
def get_sports():
    query = "SELECT * FROM sports"
    filters = []
    params = []

    if 'name' in request.args:
        filters.append("name LIKE ?")
        params.append(f"%{request.args['name']}%")
    
    if 'active' in request.args:
        filters.append("active = ?")
        params.append(request.args['active'])
    
    if filters:
        query += " WHERE " + " AND ".join(filters)
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, params)
    sports = cur.fetchall()
    return jsonify([dict(row) for row in sports])


@app.route('/sports/<string:slug>', methods=['GET'])
def get_sports_slug(slug):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sports WHERE slug= ?", (slug,))

    sport = cur.fetchone()

    if sport:
        return jsonify(dict(sport))
    else:
        return jsonify({"error": "Sport not found"}), 404

if __name__ == "__main__":
    app.run(debug=True,port=8000)
