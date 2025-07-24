#!/usr/bin/env python3
"""
Test script to verify decryption works correctly
"""

from cryptography.fernet import Fernet

# The values from our encryption script
ENCRYPTION_KEY = "dEXFw2mYtOLIS5XjXz_0AxknbRauTEuSyStO1WJsS98="
ENCRYPTED_SECRET = "gAAAAABogYTeP7PCyZ1P1sgNoBZWeCaSqXRHyyz1RafMStsjj5ZUa3kUjREC5vm8MwBwkqAnq--s1kDbkyq27HjhgQ4-8xUmcQ=="
ENCRYPTED_DB1_PASSWORD = "gAAAAABogYTeKNGNbIvfmro5fwWlFWUaCHOEAUL45uujcqIs7f_ovH9I2w5YSc3nfU39hSww489S-vzWGxKBX9uw1XwHoo9V0A=="
ENCRYPTED_DB2_PASSWORD = "gAAAAABogYTeg6KzP_HrOL5-Y9NNAr9VcuYcaK24bLmtQHd0Aoq2m8q6D7sP1yMaLv9ZDuVlhORb8tkE2x--DkrLST1KHQ7xNQ=="

def test_decryption():
    print("🔐 Testing Decryption")
    print("=" * 50)

    try:
        # Create Fernet instance
        fernet = Fernet(ENCRYPTION_KEY.encode())

        # Decrypt API secret
        api_secret = fernet.decrypt(ENCRYPTED_SECRET.encode()).decode()
        print(f"✅ API Secret decrypted: {api_secret}")

        # Decrypt DB1 password
        db1_password = fernet.decrypt(ENCRYPTED_DB1_PASSWORD.encode()).decode()
        print(f"✅ DB1 Password decrypted: {db1_password}")

        # Decrypt DB2 password
        db2_password = fernet.decrypt(ENCRYPTED_DB2_PASSWORD.encode()).decode()
        print(f"✅ DB2 Password decrypted: {db2_password}")

        print(f"\n🎯 Expected values:")
        print(f"API Secret: sunvair")
        print(f"DB1 Password: QUANTUM")
        print(f"DB2 Password: QUANTUM")

        print(f"\n🔍 Verification:")
        print(f"API Secret match: {api_secret == 'sunvair'}")
        print(f"DB1 Password match: {db1_password == 'QUANTUM'}")
        print(f"DB2 Password match: {db2_password == 'QUANTUM'}")

    except Exception as e:
        print(f"❌ Decryption failed: {e}")

if __name__ == "__main__":
    test_decryption()