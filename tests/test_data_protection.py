from data_protection import DataProtection, EncryptionKey

def test_generate_key():
    data_protection = DataProtection()
    key = data_protection.generate_key("key1")
    assert isinstance(key, EncryptionKey)
    assert key.key == "key1"
    assert key.rotation_date == "2024-01-01"

def test_encrypt_data():
    data_protection = DataProtection()
    data_protection.generate_key("key1")
    encrypted_data = data_protection.encrypt_data("data1", "hello", "key1")
    assert encrypted_data == "encrypted_hello"

def test_decrypt_data():
    data_protection = DataProtection()
    data_protection.generate_key("key1")
    data_protection.encrypt_data("data1", "hello", "key1")
    decrypted_data = data_protection.decrypt_data("data1", "key1")
    assert decrypted_data == "hello"

def test_rotate_key():
    data_protection = DataProtection()
    data_protection.generate_key("key1")
    data_protection.rotate_key("key1")
    key = data_protection.keys["key1"]
    assert key.rotation_date == "2024-01-15"

def test_key_not_found():
    data_protection = DataProtection()
    try:
        data_protection.encrypt_data("data1", "hello", "key1")
        assert False
    except ValueError as e:
        assert str(e) == "Key not found"

def test_data_not_found():
    data_protection = DataProtection()
    data_protection.generate_key("key1")
    try:
        data_protection.decrypt_data("data1", "key1")
        assert False
    except ValueError as e:
        assert str(e) == "Data or key not found"
