from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime


app = Flask(__name__)
DATABASE = 'sportsbook.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return "Flask framework"


if __name__ == "__main__":
    app.run(debug=True)
