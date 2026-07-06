from flask import Flask, jsonify, request
import psycopg2
import psycopg2.extras
import os
import time

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),
    "port": os.environ.get("DB_PORT", "5432"),
    "dbname": os.environ.get("DB_NAME", "appdb"),
    "user": os.environ.get("DB_USER", "appuser"),
    "password": os.environ.get("DB_PASSWORD", "apppassword"),
}


def get_connection(retries=10, delay=2):
    """Retry connecting to Postgres — useful while the db container is
    still starting up, even with a compose healthcheck in place."""
    last_err = None
    for _ in range(retries):
        try:
            return psycopg2.connect(**DB_CONFIG)
        except psycopg2.OperationalError as e:
            last_err = e
            time.sleep(delay)
    raise last_err


@app.route("/health")
def health():
    try:
        conn = get_connection(retries=1)
        conn.close()
        return jsonify(status="ok", db="connected"), 200
    except Exception as e:
        return jsonify(status="error", db=str(e)), 503


@app.route("/items", methods=["GET"])
def list_items():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, name, quantity, created_at FROM items ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json(force=True) or {}
    name = data.get("name")
    quantity = data.get("quantity", 0)
    if not name:
        return jsonify(error="name is required"), 400

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "INSERT INTO items (name, quantity) VALUES (%s, %s) "
        "RETURNING id, name, quantity, created_at;",
        (name, quantity),
    )
    new_item = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_item), 201


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if deleted == 0:
        return jsonify(error="item not found"), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
