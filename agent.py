from flask import Flask, request, jsonify
import os
import oracledb
from dotenv import load_dotenv
load_dotenv()

# Enable thick mode if ORACLE_CLIENT_LIB_DIR is set (resolve relative path)
client_lib_dir = os.getenv("ORACLE_CLIENT_LIB_DIR")
if client_lib_dir:
    client_lib_dir = os.path.abspath(client_lib_dir)
    oracledb.init_oracle_client(lib_dir=client_lib_dir)

app = Flask(__name__)

API_SECRET = os.getenv("AGENT_SECRET", "default_secret")

DEBUG_AGENT = os.getenv("DEBUG_AGENT", "false").lower() == "true"

def debug_print(msg):
    if DEBUG_AGENT:
        print(msg)

def test_oracle_connection_on_startup():
    try:
        dsn = oracledb.makedsn(
            os.getenv("ORACLE_HOST"),
            os.getenv("ORACLE_PORT"),
            service_name=os.getenv("ORACLE_SERVICE")
        )
        conn = oracledb.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=dsn
        )
        conn.close()
        debug_print("DEBUG: Successfully connected to Oracle database on startup")
    except Exception as e:
        debug_print(f"DEBUG: Failed to connect to Oracle database on startup: {e}")

def connect_and_query(sql):
    try:
        dsn = oracledb.makedsn(
            os.getenv("ORACLE_HOST"),
            os.getenv("ORACLE_PORT"),
            service_name=os.getenv("ORACLE_SERVICE")
        )
        conn = oracledb.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=dsn
        )
        debug_print("DEBUG: Successfully connected to Oracle database")
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return {"columns": columns, "rows": rows}
    except Exception as e:
        return {"error": str(e)}

@app.route("/run-query", methods=["POST"])
def run_query():
    auth = request.headers.get("X-API-KEY")
    if auth != API_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    sql = request.json.get("sql")
    if not sql:
        return jsonify({"error": "No SQL query provided"}), 400

    # Only allow read-only SELECT queries
    if not sql.strip().lower().startswith("select"):
        return jsonify({"error": "Only read-only SELECT queries are allowed"}), 403

    result = connect_and_query(sql)
    return jsonify(result)

if __name__ == "__main__":
    test_oracle_connection_on_startup()
    app.run(host="0.0.0.0", port=5001)
