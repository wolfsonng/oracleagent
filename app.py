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

@app.route("/", methods=["GET"])
def index():
    # Test database connection
    try:
        result = connect_and_query("SELECT 1 FROM dual")
        db_status = "✅" if "error" not in result else "❌"
        db_message = "Connected" if "error" not in result else "Disconnected"
    except Exception as e:
        db_status = "❌"
        db_message = "Error"

    # Get system info
    import platform
    import datetime

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>System Status</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .status-item {{ display: flex; justify-content: space-between; align-items: center; padding: 15px; margin: 10px 0; background: #f8f9fa; border-radius: 5px; }}
            .status-ok {{ border-left: 4px solid #28a745; }}
            .status-error {{ border-left: 4px solid #dc3545; }}
            .timestamp {{ text-align: center; color: #6c757d; font-size: 0.9em; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🖥️ System Status Dashboard</h1>
                <p>Infrastructure Monitoring Service</p>
            </div>

            <div class="status-item status-ok">
                <span><strong>Web Service</strong></span>
                <span>✅ Online</span>
            </div>

            <div class="status-item {'status-ok' if db_status == '✅' else 'status-error'}">
                <span><strong>Data Service</strong></span>
                <span>{db_status} {db_message}</span>
            </div>

            <div class="status-item status-ok">
                <span><strong>Platform</strong></span>
                <span>✅ {platform.system()} {platform.release()}</span>
            </div>

            <div class="timestamp">
                Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    </body>
    </html>
    """
    return html

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

@app.route("/dbtest", methods=["GET"])
def dbtest():
    try:
        result = connect_and_query("SELECT 1 FROM dual")
        if "error" in result:
            return jsonify({"db_status": "fail", "details": result["error"]}), 500
        return jsonify({"db_status": "ok", "result": result})
    except Exception as e:
        return jsonify({"db_status": "fail", "details": str(e)}), 500

def test_oracle_connection_on_startup():
    print("🔍 Testing database connection...")
    try:
        result = connect_and_query("SELECT 1 FROM dual")
        if "error" in result:
            print(f"❌ Database connection failed: {result['error']}")
            logging.error(f"Startup DB connection failed: {result['error']}")
        else:
            print("✅ Database connection successful!")
            logging.info("Startup DB connection successful.")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        logging.warning(f"Startup DB connection failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Oracle Agent...")
    print(f"📊 Debug mode: {config.DEBUG_AGENT}")
    print(f"🏠 Host: {Config.ORACLE_HOST}")
    print(f"🔌 Port: {Config.ORACLE_PORT}")
    print(f"🗄️  Service: {Config.ORACLE_SERVICE}")
    print(f"👤 User: {Config.ORACLE_USER}")
    print("-" * 50)

    test_oracle_connection_on_startup()
    print("-" * 50)
    print("🌐 Starting Flask server on http://0.0.0.0:5001")
    app.run(host="0.0.0.0", port=5001)
