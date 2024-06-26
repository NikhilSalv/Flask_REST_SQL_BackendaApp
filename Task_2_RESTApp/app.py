from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from datetime import datetime, timezone
from dateutil import parser
import pytz
from flask_wtf.csrf import CSRFProtect, generate_csrf


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

DATABASE = 'sportsbook.db'

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    return jsonify({"csrf_token": csrf_token})


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


""" CODE REFACTORED :  Single Search route for search operations in Sports, Events and Selections"""

@app.route('/getdata', methods=['GET'])
def get_data():
    valid_types = ['sports', 'events', 'selections']
    data_type = request.args.get('type')
    
    if data_type not in valid_types:
        return jsonify({"error": "Invalid type parameter"}), 400
    
    query = f"SELECT * FROM {data_type}"
    filters = []
    params = []

    # Common filters
    if 'name' in request.args:
        filters.append("name LIKE ?")
        params.append(f"%{request.args['name']}%")
    
    if 'active' in request.args:
        filters.append("active = ?")
        params.append(request.args['active'])

    # Type-specific filters
    if data_type == 'sports':
        if 'threshold' in request.args:
            try:
                threshold = int(request.args['threshold'])
            except ValueError:
                print("error : Invalid threshold value")
                threshold = 0
            
            filters.append("(SELECT COUNT(*) FROM events WHERE sports.id = events.sport_id AND active = 1) > ?")
            params.append(threshold)

    elif data_type == 'events':
        if 'threshold' in request.args:
            try:
                threshold = int(request.args['threshold'])
            except ValueError:
                print("error : Invalid threshold value")
                threshold = 0

            filters.append("(SELECT COUNT(*) FROM selections WHERE events.id = selections.event_id AND selections.active = 1) > ?")
            params.append(threshold)
        
        if 'status' in request.args:
            filters.append("status = ?")
            params.append(request.args['status'])

        if 'type' in request.args:
            filters.append("type = ?")
            params.append(request.args['type'])
        
        if 'sport_id' in request.args:
            filters.append("sport_id = ?")
            params.append(request.args['sport_id'])
        
        if 'start_time' in request.args and 'end_time' in request.args and 'timezone' in request.args:
            try:
                start_time_str = request.args['start_time']
                end_time_str = request.args['end_time']
                timezone_str = request.args['timezone']
                
                local_tz = pytz.timezone(timezone_str)
                start_time_local = parser.parse(start_time_str)
                end_time_local = parser.parse(end_time_str)

                start_time_local = local_tz.localize(start_time_local)
                end_time_local = local_tz.localize(end_time_local)

                start_time_utc = start_time_local.astimezone(pytz.utc)
                end_time_utc = end_time_local.astimezone(pytz.utc)

                filters.append("scheduled_start BETWEEN ? AND ?")
                params.extend([start_time_utc.isoformat(), end_time_utc.isoformat()])
            except Exception as e:
                return jsonify({"error": str(e)}), 400

    elif data_type == 'selections':
        if 'outcome' in request.args:
            filters.append("outcome = ?")
            params.append(request.args['outcome'])
        
        if 'event_id' in request.args:
            filters.append("event_id = ?")
            params.append(request.args['event_id'])

    if filters:
        query += " WHERE " + " AND ".join(filters)

    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, params)
    data = cur.fetchall()
    return jsonify([dict(row) for row in data])

"""
CODE REFACTORED : Sigle route for Search operations in Sports OR Events with slug
"""

@app.route('/<string:type>/<string:slug>', methods=['GET'])
def get_data_by_slug(type, slug):
    valid_types = ['sports', 'events']
    
    if type not in valid_types:
        return jsonify({"error": "Invalid type parameter"}), 400

    conn = get_db()
    cur = conn.cursor()
    query = f"SELECT * FROM {type} WHERE slug= ?"
    cur.execute(query, (slug,))

    data = cur.fetchone()

    if data:
        return jsonify(dict(data))
    else:
        return jsonify({"error": f"{type[:-1].capitalize()} not found"}), 404

"""
CODE REFACTORED  : Single Route for all entities to create data
"""

@app.route('/create', methods=['POST'])
def create_data():
    data = request.json
    entity_type = data.get('entity_type')

    valid_types = ['sports', 'events', 'selections']
    if entity_type not in valid_types:
        return jsonify({"error": "Invalid type parameter"}), 400

    conn = get_db()
    cur = conn.cursor()
    
    if entity_type == 'sports':
        cur.execute("INSERT INTO sports (name, slug, active) VALUES (?, ?, ?)",
                    (data['name'], data['slug'], data['active']))
        conn.commit()
        return jsonify({"id": cur.lastrowid}), 201

    elif entity_type == 'events':
        actual_start = None
        default_value = 0
        if data['status'] == "Started":
            current_time_utc = datetime.now(timezone.utc)
            actual_start = current_time_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        cur.execute("""INSERT INTO events (name, slug, active, type, sport_id, status, scheduled_start, actual_start)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (data['name'], data['slug'], default_value, data['type'], data['sport_id'],
                     data['status'], data['scheduled_start'], actual_start))
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM events WHERE sport_id = ? AND active = ?", (data['sport_id'], 1))
        active_events_count = cur.fetchone()[0]
        cur.execute("UPDATE sports SET active = ? WHERE id = ?", (1 if active_events_count > 0 else 0, data['sport_id']))
        conn.commit()

        return jsonify({"id": cur.lastrowid}), 201

    elif entity_type == 'selections':
        formatted_price = round(float(data['price']), 2)
        cur.execute("""INSERT INTO selections (name, event_id, price, active, outcome)
                       VALUES (?, ?, ?, ?, ?)""",
                    (data['name'], data['event_id'], formatted_price, data['active'], data['outcome']))
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM selections WHERE event_id = ? AND active = ?", (data['event_id'], 1))
        active_selection_count = cur.fetchone()[0]
        cur.execute("UPDATE events SET active = ? WHERE id = ?", (1 if active_selection_count > 0 else 0, data['event_id']))
        conn.commit()

        return jsonify({"id": cur.lastrowid}), 201


"""
SINGLE ROUTE FOR UPDATE : Three routes merged to a single route to update data
"""

@app.route('/update/<string:type>/<int:id>', methods=['PUT'])
def update_data(type, id):
    valid_types = ['sports', 'events', 'selections']
    
    if type not in valid_types:
        return jsonify({"error": "Invalid type parameter"}), 400

    data = request.json
    conn = get_db()
    cur = conn.cursor()

    if type == 'sports':
        cur.execute("SELECT * FROM sports WHERE id = ?", (id,))
        sport = cur.fetchone()
        if not sport:
            return jsonify({"error": "Sport not found"}), 404

        # Prepare the updated values, using the existing ones if not provided
        name = data.get('name', sport['name'])
        slug = data.get('slug', sport['slug'])
        active = data.get('active', sport['active'])

        # Update the record
        cur.execute("UPDATE sports SET name = ?, slug = ?, active = ? WHERE id = ?",
                    (name, slug, active, id))
        conn.commit()

        return jsonify({"updated": cur.rowcount})

    elif type == 'events':
        cur.execute("SELECT * FROM events WHERE id = ?", (id,))
        event = cur.fetchone()
        if not event:
            return jsonify({"error": "Event not found"}), 404

        # Prepare the updated values, using the existing ones if not provided
        name = data.get('name', event['name'])
        slug = data.get('slug', event['slug'])
        active = event['active']
        event_type = data.get('type', event['type'])
        sport_id = data.get('sport_id', event['sport_id'])
        status = data.get('status', event['status'])
        scheduled_start = data.get('scheduled_start', event['scheduled_start'])
        actual_start = event['actual_start']
        if status == "Started":
            current_time_utc = datetime.now(timezone.utc)
            actual_start = current_time_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

        # Update the record
        cur.execute("""UPDATE events SET name = ?, slug = ?, active = ?, type = ?, sport_id = ?, 
                       status = ?, scheduled_start = ?, actual_start = ? WHERE id = ?""",
                    (name, slug, active, event_type, sport_id, status, scheduled_start, actual_start, id))
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM events WHERE sport_id = ? AND active = ?", (sport_id, 1))
        active_events_count = cur.fetchone()[0]
        cur.execute("UPDATE sports SET active = ? WHERE id = ?", (1 if active_events_count > 0 else 0, sport_id))
        conn.commit()

        return jsonify({"updated": cur.rowcount})

    elif type == 'selections':
        cur.execute("SELECT * FROM selections WHERE id = ?", (id,))
        selection = cur.fetchone()

        if not selection:
            return jsonify({"error": "Selection not found"}), 404
        
        name = data.get("name", selection["name"])
        event_id = data.get("event_id", selection["event_id"])
        price = data.get("price", selection["price"])
        active = data.get("active", selection["active"])
        outcome = data.get("outcome", selection["outcome"])

        price = round(float(price), 2) if price is not None else selection["price"]

        cur.execute("UPDATE selections SET name = ?, event_id = ?, price = ? , active = ?, outcome = ? WHERE id = ?", 
                    (name, event_id, price, active, outcome, id))
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM selections WHERE event_id = ? AND active = ?", (event_id, 1))
        active_selection_count = cur.fetchone()[0]
        cur.execute("UPDATE events SET active = ? WHERE id = ?", (1 if active_selection_count > 0 else 0, event_id))
        conn.commit()

        return jsonify({"updated": cur.rowcount})


if __name__ == "__main__":
    app.run(debug=True)
