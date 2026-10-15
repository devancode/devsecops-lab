import os
import sqlite3
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)

# VULN-1: Hardcoded secret
ADMIN_PASSWORD = "super-secret-admin-password-123"
DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, owner TEXT, body TEXT)"
    )
    return conn


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/admin")
def admin():
    if request.args.get("password") == ADMIN_PASSWORD:
        return jsonify(message="Welcome, admin!")
    return jsonify(error="Access denied"), 403


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json(force=True)
    conn = get_db()
    # Safe: parameterised query (compare with VULN-2 below)
    conn.execute("INSERT INTO notes (owner, body) VALUES (?, ?)", (data["owner"], data["body"]))
    conn.commit()
    return jsonify(saved=True), 201


@app.route("/notes/<owner>")
def list_notes(owner):
    conn = get_db()
    # VULN-2: SQL injection - user input concatenated into SQL
    query = "SELECT id, body FROM notes WHERE owner = '" + owner + "'"
    rows = conn.execute(query).fetchall()
    return jsonify(notes=[{"id": r[0], "body": r[1]} for r in rows])

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # VULN-3: Command injection - shell=True with user input
    out = subprocess.check_output("ping -c 1 " + host, shell=True) 
    return jsonify(output=out.decode())

def add(a, b):
    return a + b


if __name__ == "__main__":
    app.run(port=5001)