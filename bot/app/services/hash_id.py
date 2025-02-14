from cryptography.fernet import Fernet



SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

def encrypt_id(game_id: int) -> str:
    """Encrypt the game ID so it can be decrypted later."""
    return cipher.encrypt(str(game_id).encode()).decode()

def decrypt_id(encrypted_id: str) -> int:
    """Decrypt the game ID back to its original value."""
    return int(cipher.decrypt(encrypted_id.encode()).decode())
