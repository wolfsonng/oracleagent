import os
import sys
import platform
import logging
import oracledb
from config import Config

def init_oracle_client():
    lib_dir = os.path.abspath(Config.ORACLE_CLIENT_LIB_DIR)
    system = platform.system().lower()

    if system == "darwin":  # macOS
        lib_name = "libclntsh.dylib"
    elif system == "windows":
        lib_name = "oci.dll"
    else:  # Assume Linux/Unix
        lib_name = "libclntsh.so"

    lib_path = os.path.join(lib_dir, lib_name)
    if not os.path.exists(lib_path):
        logging.error(f"{lib_name} not found at: {lib_path}")
        logging.warning("Oracle client initialization failed, will use thin mode")
        return False

    try:
        oracledb.init_oracle_client(lib_dir=lib_dir)
        logging.info(f"Oracle client initialized with {lib_name} at {lib_dir}")
        return True
    except Exception as e:
        logging.error(f"Oracle client initialization error: {e}")
        logging.warning("Will use thin mode")
        return False

# Try to initialize Oracle client
if not init_oracle_client():
    logging.warning("Oracle client initialization failed, will use thin mode")

def connect_and_query(sql):
    try:
        dsn = oracledb.makedsn(
            config.ORACLE_HOST,
            config.ORACLE_PORT,
            service_name=config.ORACLE_SERVICE
        )
        conn = oracledb.connect(
            user=config.ORACLE_USER,
            password=config.ORACLE_PASSWORD,
            dsn=dsn
        )
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return {"columns": columns, "rows": rows}
    except Exception as e:
        logging.exception("Oracle query failed")
        return {"error": str(e)}
