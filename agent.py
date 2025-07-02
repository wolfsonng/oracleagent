from flask import Flask, request, jsonify
import os
import cx_Oracle

app = Flask(__name__)

API_SECRET = os.getenv("AGENT_SECRET", "default_secret")

def connect_and_query(sql):
    try:
        dsn = cx_Oracle.makedsn(
            os.getenv("ORACLE_HOST"),
            os.getenv("ORACLE_PORT"),
            service_name=os.getenv("ORACLE_SERVICE")
        )
        conn = cx_Oracle.connect(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=dsn
        )
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

    result = connect_and_query(sql)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
