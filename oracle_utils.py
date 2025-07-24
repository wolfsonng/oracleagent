import os
import oracledb
from config import Config
import logging

config = Config()

def init_oracle_client():
    """Initialize Oracle client with better error handling"""
    if not config.ORACLE_CLIENT_LIB_DIR:
        logging.warning("ORACLE_CLIENT_LIB_DIR not set, trying thin mode")
        return False

    try:
        lib_dir = os.path.abspath(config.ORACLE_CLIENT_LIB_DIR)
        logging.info(f"Initializing Oracle client from: {lib_dir}")

        # Check if the directory exists
        if not os.path.exists(lib_dir):
            logging.error(f"Oracle client directory does not exist: {lib_dir}")
            return False

        # Check if libclntsh.so exists
        libclntsh_path = os.path.join(lib_dir, "libclntsh.so")
        if not os.path.exists(libclntsh_path):
            logging.error(f"libclntsh.so not found at: {libclntsh_path}")
            return False

        oracledb.init_oracle_client(lib_dir=lib_dir)
        logging.info("Oracle client initialized successfully")
        return True

    except Exception as e:
        logging.error(f"Failed to initialize Oracle client: {e}")
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
