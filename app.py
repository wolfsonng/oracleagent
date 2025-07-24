from flask import Flask, request, jsonify, abort
from config import Config
from oracle_utils import connect_and_query
import logging
import re

app = Flask(__name__)
config = Config()
logging.basicConfig(level=logging.DEBUG if config.DEBUG_AGENT else logging.INFO)

# @app.before_request
# def limit_remote_addr():
#     client_ip = request.remote_addr
#     if config.ALLOWED_IPS and client_ip not in config.ALLOWED_IPS:
#         logging.warning(f"Unauthorized IP attempt: {client_ip}")
#         abort(403)

@app.route("/run-query", methods=["POST"])
def run_query():

    api_key = request.headers.get("X-API-KEY")
    logging.debug(f"Received API key: {api_key}")  # Debug statement
    # Check if the API key matches the configured secret
    if api_key != config.API_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    sql = request.json.get("sql")
    if not sql:
        return jsonify({"error": "No SQL query provided"}), 400

    if not sql.strip().lower().startswith("select"):
        return jsonify({"error": "Only read-only SELECT queries are allowed"}), 403

    if re.search(r"\b(insert|update|delete|merge|drop|alter|grant|execute|dbms_|utl_)\b", sql, re.IGNORECASE):
        return jsonify({"error": "Query contains disallowed keywords"}), 403

    result = connect_and_query(sql)
    return jsonify(result)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/describe", methods=["GET"])
def describe():
    return jsonify({
        "name": "Oracle Read Agent",
        "version": "1.1",
        "endpoints": ["/run-query", "/health", "/describe"],
        "notes": "Only SELECT queries allowed. Protected by API key and IP whitelist."
    })

def test_oracle_connection_on_startup():
    try:
        result = connect_and_query("SELECT 1 FROM dual")
        logging.info("Startup DB connection successful.")
    except Exception as e:
        logging.warning(f"Startup DB connection failed: {e}")

if __name__ == "__main__":
    test_oracle_connection_on_startup()
    app.run(host="0.0.0.0", port=5001)
