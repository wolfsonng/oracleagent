#!/usr/bin/env python3
"""
Oracle Agent Credential Encryption Helper
Generates encrypted credentials for secure deployment
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_encryption_key():
    """Generate a new encryption key"""
    return Fernet.generate_key().decode()

def validate_encryption_key(key):
    """Validate if the provided key is a valid Fernet key"""
    try:
        Fernet(key.encode())
        return True
    except Exception:
        return False

def encrypt_value(value, encryption_key):
    """Encrypt a value using the provided key"""
    fernet = Fernet(encryption_key.encode())
    encrypted_value = fernet.encrypt(value.encode())
    return encrypted_value.decode()

def main():
    print("🔐 Oracle Agent Credential Encryption Helper")
    print("=" * 50)

    # Get or generate encryption key
    print("\n1. Encryption Key:")
    use_existing = input("Use existing encryption key? (y/N): ").lower().strip()

    if use_existing == 'y':
        while True:
            encryption_key = input("Enter your encryption key: ").strip()
            if validate_encryption_key(encryption_key):
                print("✅ Valid encryption key provided")
                break
            else:
                print("❌ Invalid encryption key. Please provide a valid Fernet key or generate a new one.")
                generate_new = input("Generate new key instead? (y/N): ").lower().strip()
                if generate_new == 'y':
                    encryption_key = generate_encryption_key()
                    print(f"✅ Generated new encryption key: {encryption_key}")
                    break
    else:
        encryption_key = generate_encryption_key()
        print(f"✅ Generated new encryption key: {encryption_key}")

    # Get API secret
    print("\n2. API Secret:")
    api_secret = input("Enter your API secret: ").strip()
    if not api_secret:
        api_secret = "your-secure-api-secret-here"
        print(f"⚠️  Using default API secret: {api_secret}")

    # Get Oracle passwords
    print("\n3. Oracle Database Passwords:")
    db1_password = input("Enter DB1 Oracle password: ").strip()
    db2_password = input("Enter DB2 Oracle password: ").strip()

    # Encrypt values
    print("\n4. Encrypting values...")
    encrypted_secret = encrypt_value(api_secret, encryption_key)
    encrypted_db1_password = encrypt_value(db1_password, encryption_key)
    encrypted_db2_password = encrypt_value(db2_password, encryption_key)

    # Display results
    print("\n" + "=" * 50)
    print("✅ ENCRYPTION COMPLETE")
    print("=" * 50)

    print(f"\n🔑 Encryption Key:")
    print(f"ENCRYPTION_KEY={encryption_key}")

    print(f"\n🔐 Encrypted API Secret:")
    print(f"ENCRYPTED_SECRET={encrypted_secret}")

    print(f"\n🔐 Encrypted DB1 Password:")
    print(f"DB1_ENCRYPTED_ORACLE_PASSWORD={encrypted_db1_password}")

    print(f"\n🔐 Encrypted DB2 Password:")
    print(f"DB2_ENCRYPTED_ORACLE_PASSWORD={encrypted_db2_password}")

    # Generate .env content
    print(f"\n" + "=" * 50)
    print("📝 SAMPLE .env CONTENT")
    print("=" * 50)

    env_content = f"""# Oracle Agent Environment Configuration
# Copy this to .env and fill in your database details

# Database 1 Configuration
DB1_ORACLE_HOST=your-db1-host
DB1_ORACLE_PORT=1521
DB1_ORACLE_SERVICE=your-db1-service
DB1_ORACLE_USER=your-db1-username

# Database 2 Configuration
DB2_ORACLE_HOST=your-db2-host
DB2_ORACLE_PORT=1521
DB2_ORACLE_SERVICE=your-db2-service
DB2_ORACLE_USER=your-db2-username

# Shared Encryption (Security)
ENCRYPTION_KEY={encryption_key}
ENCRYPTED_SECRET={encrypted_secret}

# Database-specific encrypted passwords
DB1_ENCRYPTED_ORACLE_PASSWORD={encrypted_db1_password}
DB2_ENCRYPTED_ORACLE_PASSWORD={encrypted_db2_password}

# Debug Mode
DEBUG_AGENT=true

# IP Whitelist (optional)
ALLOWED_IPS=192.168.1.100,10.0.0.50"""

    print(env_content)

    # Save to file
    save_to_file = input(f"\n💾 Save sample .env content to 'sample.env'? (y/N): ").lower().strip()
    if save_to_file == 'y':
        with open('sample.env', 'w') as f:
            f.write(env_content)
        print("✅ Saved to 'sample.env'")

    print(f"\n🎯 Next steps:")
    print("1. Copy the .env content above")
    print("2. Create .env file: cp env.template .env")
    print("3. Paste the encrypted values into .env")
    print("4. Update database connection details")
    print("5. Test with: python test_config.py")

if __name__ == "__main__":
    main()