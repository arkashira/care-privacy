# care-privacy

A secure data protection framework that encrypts data both in transit and at rest.

## Features

* Industry-standard encryption protocols (e.g., TLS, AES)
* Secure key management and rotation
* Data at rest is encrypted and accessible only through authorized channels

## Usage

1. Generate a key using `DataProtection.generate_key()`
2. Encrypt data using `DataProtection.encrypt_data()`
3. Decrypt data using `DataProtection.decrypt_data()`
4. Rotate keys using `DataProtection.rotate_key()`

## Testing

Run tests using `pytest` command.
