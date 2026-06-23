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
        self.data = {}

    def generate_key(self, key_id: str) -> EncryptionKey:
        key = EncryptionKey(key_id, "2024-01-01")
        self.keys[key_id] = key
        return key

    def encrypt_data(self, data_id: str, data: str, key_id: str) -> str:
        key = self.keys.get(key_id)
        if key:
            encrypted_data = f"encrypted_{data}"
            self.data[data_id] = encrypted_data
            return encrypted_data
        else:
            raise ValueError("Key not found")

    def decrypt_data(self, data_id: str, key_id: str) -> str:
        encrypted_data = self.data.get(data_id)
        key = self.keys.get(key_id)
        if encrypted_data and key:
            decrypted_data = encrypted_data.replace("encrypted_", "")
            return decrypted_data
        else:
            raise ValueError("Data or key not found")

    def rotate_key(self, key_id: str) -> None:
        key = self.keys.get(key_id)
        if key:
            key.rotation_date = "2024-01-15"
        else:
            raise ValueError("Key not found")
