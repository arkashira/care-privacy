import json
from data_protection import DataProtection, EncryptionKey

def test_generate_key():
    data_protection = DataProtection()
    key = data_protection.generate_key("key1")
    assert isinstance(key, EncryptionKey)
    assert key.key == "key_key1"
    assert key.rotation_date == "2024-01-01"

def test_encrypt_data_at_rest():
    data_protection = DataProtection()
    data_protection.generate_key("key1")
    data = {"name": "John", "age": 30}
    encrypted_data = data_protection.encrypt_data_at_rest(data, "key1")
    assert isinstance(encrypted_data, str)
    assert encrypted_data != json.dumps(data)

def test_encrypt_data_in_transit():
    data_protection = DataProtection()
    data_protection.generate_key("key1")
    data = {"name": "John", "age": 30}
    encrypted_data = data_protection.encrypt_data_in_transit(data, "key1")
    assert isinstance(encrypted_data, str)
    assert encrypted_data != json.dumps(data)

def test_rotate_key():
    data_protection = DataProtection()
    data_protection.generate_key("key1")
    data_protection.rotate_key("key1")
    key = data_protection.keys["key1"]
    assert key.rotation_date == "2024-01-02"

def test_encrypt_data_at_rest_key_not_found():
    data_protection = DataProtection()
    data = {"name": "John", "age": 30}
    try:
        data_protection.encrypt_data_at_rest(data, "key1")
        assert False
    except ValueError as e:
        assert str(e) == "Key not found"

def test_encrypt_data_in_transit_key_not_found():
    data_protection = DataProtection()
    data = {"name": "John", "age": 30}
    try:
        data_protection.encrypt_data_in_transit(data, "key1")
        assert False
    except ValueError as e:
        assert str(e) == "Key not found"

def test_rotate_key_key_not_found():
    data_protection = DataProtection()
    try:
        data_protection.rotate_key("key1")
        assert False
    except ValueError as e:
        assert str(e) == "Key not found"
