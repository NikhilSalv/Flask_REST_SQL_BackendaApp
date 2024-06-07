from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime


app = Flask(__name__)
DATABASE = 'sportsbook.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

"""
SPORTS APIs
"""

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

@app.route("/sports/<int:sport_id>", methods=["PUT"])
def update_sport(sport_id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sports WHERE id = ?", (sport_id,))
    sport = cur.fetchone()
    if not sport:
        return jsonify({"error": "Sport not found"}), 404

    # Prepare the updated values, using the existing ones if not provided
    name = data.get('name', sport['name'])
    slug = data.get('slug', sport['slug'])
    active = data.get('active', sport['active'])

    # Update the record
    cur.execute("UPDATE sports SET name = ?, slug = ?, active = ? WHERE id = ?",
                (name, slug, active, sport_id))
    conn.commit()

    return jsonify({"updated": cur.rowcount})

"""
EVENTS APIs
"""

def create_event():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""INSERT INTO events (name, slug, active, type, sport_id, status, scheduled_start)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (data['name'], data['slug'], data['active'], data['type'], data['sport_id'],
                 data['status'], data['scheduled_start']))
    conn.commit()
    return jsonify({"id": cur.lastrowid}), 201

@app.route('/events', methods=['GET'])
def get_events():
    query = "SELECT * FROM events"
    filters = []
    params = []

    if 'name' in request.args:
        filters.append("name LIKE ?")
        params.append(f"%{request.args['name']}%")
    
    if 'active' in request.args:
        filters.append("active = ?")
        params.append(request.args['active'])
    
    if 'status' in request.args:
        filters.append("status = ?")
        params.append(request.args['status'])
    
    if 'type' in request.args:
        filters.append("type = ?")
        params.append(request.args['type'])
    
    if 'sport_id' in request.args:
        filters.append("sport_id = ?")
        params.append(request.args['sport_id'])
    
    if filters:
        query += " WHERE " + " AND ".join(filters)
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, params)
    events = cur.fetchall()
    return jsonify([dict(row) for row in events])


@app.route('/events/<string:slug>', methods=['GET'])
def get_events_slug(slug):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events WHERE slug= ?", (slug,))

    sport = cur.fetchone()

    if sport:
        return jsonify(dict(sport))
    else:
        return jsonify({"error": "Event not found"}), 404


@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cur.fetchone()
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Prepare the updated values, using the existing ones if not provided
    print(event["type"] + "_____")
    name = data.get('name', event['name'])
    slug = data.get('slug', event['slug'])
    active = data.get('active', event['active'])
    type = data.get('type', event['type'])
    status = data.get('status', event['status'])
    scheduled_start = data.get('scheduled_start', event['scheduled_start'])
    actual_start = data.get('actual_start', event['actual_start'])

  

    # Update the record
    cur.execute("UPDATE events SET name = ?, slug = ?, active = ?, type = ?, status = ?, scheduled_start = ?, actual_start = ? WHERE id = ?",
                (name, slug, active,type, status, scheduled_start, actual_start, event_id))
    conn.commit()

    return jsonify({"updated": cur.rowcount})


if __name__ == "__main__":
    app.run(debug=True,port=8000)
