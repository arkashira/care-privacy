import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class EncryptionKey:
    key: str
    rotation_date: str

class DataProtection:
    def __init__(self):
        self.keys = {}

    def generate_key(self, key_id: str) -> EncryptionKey:
        key = EncryptionKey(key=f"key_{key_id}", rotation_date="2024-01-01")
        self.keys[key_id] = key
        return key

    def encrypt_data_at_rest(self, data: Dict, key_id: str) -> str:
        key = self.keys.get(key_id)
        if key:
            encrypted_data = json.dumps(data).encode()
            # Simulate AES-256 encryption
            encrypted_data = encrypted_data.hex()
            return encrypted_data
        else:
            raise ValueError("Key not found")

    def encrypt_data_in_transit(self, data: Dict, key_id: str) -> str:
        key = self.keys.get(key_id)
        if key:
            encrypted_data = json.dumps(data).encode()
            # Simulate TLS 1.3 encryption
            encrypted_data = encrypted_data.hex()
            return encrypted_data
        else:
            raise ValueError("Key not found")

    def rotate_key(self, key_id: str) -> None:
        key = self.keys.get(key_id)
        if key:
            key.rotation_date = "2024-01-02"
        else:
            raise ValueError("Key not found")
