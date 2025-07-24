import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()

def get_oracle_client_lib_dir():
    # 1. Use environment variable if set
    env_path = os.getenv("ORACLE_CLIENT_LIB_DIR")
    if env_path and os.path.exists(env_path):
        return env_path

    # 2. Try instantclient_23_8 (Linux/x86-64)
    local_path = os.path.join(os.path.dirname(__file__), "instantclient_23_8")
    if os.path.exists(local_path):
        return local_path

    # 3. Try oracle (macOS or legacy)
    mac_path = os.path.join(os.path.dirname(__file__), "oracle")
    if os.path.exists(mac_path):
        return mac_path

    # 4. Try Docker default
    docker_path = "/app/oracle"
    if os.path.exists(docker_path):
        return docker_path

    # 5. Fallback: None (will use thin mode)
    return None

class Config:
    # Database Configuration
    ORACLE_USER = os.getenv("ORACLE_USER")
    ORACLE_HOST = os.getenv("ORACLE_HOST")
    ORACLE_PORT = os.getenv("ORACLE_PORT")
    ORACLE_SERVICE = os.getenv("ORACLE_SERVICE")
    ORACLE_CLIENT_LIB_DIR = get_oracle_client_lib_dir()

    # Debug and Security
    DEBUG_AGENT = os.getenv("DEBUG_AGENT", "false").lower() == "true"
    ALLOWED_IPS = os.getenv("ALLOWED_IPS", "").split(",") if os.getenv("ALLOWED_IPS") else []

    # Encryption
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    ENCRYPTED_SECRET = os.getenv("ENCRYPTED_SECRET")
    ENCRYPTED_ORACLE_PASSWORD = os.getenv("ENCRYPTED_ORACLE_PASSWORD")

    # Decrypt credentials
    @classmethod
    def get_api_secret(cls):
        if not cls.ENCRYPTION_KEY or not cls.ENCRYPTED_SECRET:
            raise ValueError("Missing encryption key or encrypted secret")
        try:
            fernet = Fernet(cls.ENCRYPTION_KEY.encode())
            return fernet.decrypt(cls.ENCRYPTED_SECRET.encode()).decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt API secret: {e}")

    @classmethod
    def get_oracle_password(cls):
        if not cls.ENCRYPTION_KEY or not cls.ENCRYPTED_ORACLE_PASSWORD:
            raise ValueError("Missing encryption key or encrypted Oracle password")
        try:
            fernet = Fernet(cls.ENCRYPTION_KEY.encode())
            return fernet.decrypt(cls.ENCRYPTED_ORACLE_PASSWORD.encode()).decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt Oracle password: {e}")

    # Properties for easy access
    @property
    def API_SECRET(self):
        return self.get_api_secret()

    @property
    def ORACLE_PASSWORD(self):
        return self.get_oracle_password()