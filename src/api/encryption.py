"""
Encryption Middleware
AES-256 encryption for sensitive data
"""

from cryptography.fernet import Fernet
import os
import json
import logging

logger = logging.getLogger(__name__)

# Generate or load encryption key
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    logger.warning("No ENCRYPTION_KEY in .env - generated temporary key. Add to .env for persistence!")

cipher = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)


def encrypt_data(data: str) -> str:
    """Encrypt string data using AES-256"""
    try:
        return cipher.encrypt(data.encode()).decode()
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        raise


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt encrypted string data"""
    try:
        return cipher.decrypt(encrypted_data.encode()).decode()
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        raise


def encrypt_dict(data: dict) -> str:
    """Encrypt dictionary to encrypted JSON string"""
    try:
        json_str = json.dumps(data)
        return encrypt_data(json_str)
    except Exception as e:
        logger.error(f"Dict encryption error: {e}")
        raise


def decrypt_dict(encrypted_data: str) -> dict:
    """Decrypt encrypted JSON string to dictionary"""
    try:
        json_str = decrypt_data(encrypted_data)
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"Dict decryption error: {e}")
        raise


# Sensitive field names that should be encrypted
SENSITIVE_FIELDS = [
    'password',
    'api_key',
    'secret',
    'token',
    'bank_account',
    'credit_card',
    'ssn',
    'tax_id',
]


def encrypt_sensitive_fields(data: dict) -> dict:
    """Automatically encrypt sensitive fields in a dictionary"""
    encrypted = data.copy()
    for key, value in data.items():
        if any(sensitive in key.lower() for sensitive in SENSITIVE_FIELDS):
            if isinstance(value, str):
                encrypted[key] = f"ENC:{encrypt_data(value)}"
            elif value is not None:
                encrypted[key] = f"ENC:{encrypt_data(str(value))}"
    return encrypted


def decrypt_sensitive_fields(data: dict) -> dict:
    """Automatically decrypt sensitive fields in a dictionary"""
    decrypted = data.copy()
    for key, value in data.items():
        if isinstance(value, str) and value.startswith("ENC:"):
            try:
                decrypted[key] = decrypt_data(value[4:])  # Remove "ENC:" prefix
            except Exception as e:
                logger.error(f"Failed to decrypt {key}: {e}")
                decrypted[key] = None
    return decrypted


if __name__ == "__main__":
    # Test encryption
    print("Testing Encryption Module...")
    
    # Test string encryption
    test_data = "Sensitive financial data: $100,000"
    encrypted = encrypt_data(test_data)
    decrypted = decrypt_data(encrypted)
    
    print(f"Original: {test_data}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}")
    
    # Test dict encryption
    test_dict = {
        "company": "ABC Corp",
        "revenue": 1000000,
        "api_key": "secret_key_12345",
        "bank_account": "1234567890"
    }
    
    print("\nTesting sensitive field encryption...")
    encrypted_dict = encrypt_sensitive_fields(test_dict)
    print(f"Encrypted: {encrypted_dict}")
    
    decrypted_dict = decrypt_sensitive_fields(encrypted_dict)
    print(f"Decrypted: {decrypted_dict}")
    
    print("\n[OK] Encryption module working!")