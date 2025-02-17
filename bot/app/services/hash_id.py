import base64

def encode_id(game_id: int) -> str:
    return base64.urlsafe_b64encode(str(game_id).encode()).decode().rstrip("=")

def decode_id(encoded_id: str) -> int:
    return int(base64.urlsafe_b64decode(encoded_id + "=" * (len(encoded_id) % 4)).decode())

# Example
enc = encode_id(12345)
print("Encoded:", enc)

dec = decode_id(enc)
print("Decoded:", dec)
