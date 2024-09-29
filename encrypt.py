from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from base64 import b64encode, b64decode

# Generate a random key for AES (256 bits)
def generate_key():
    return os.urandom(32)  # 32 bytes = 256 bits

def encrypt_password(password, key):
    # Generate a random 16-byte (128 bits) IV (Initialization Vector)
    iv = os.urandom(16)

    # Create a new AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the password to make sure it's a multiple of 16 bytes
    padded_password = pad(password.encode())
    
    # Encrypt the password
    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()

    # Encode the IV and the encrypted password to make them safe for storage
    return b64encode(iv).decode('utf-8'), b64encode(encrypted_password).decode('utf-8')

def decrypt_password(encrypted_password, key, iv):
    # Decode the base64-encoded values
    iv = b64decode(iv)
    encrypted_password = b64decode(encrypted_password)

    # Create a new AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the password
    decrypted_padded_password = decryptor.update(encrypted_password) + decryptor.finalize()
    
    # Unpad the decrypted password
    return unpad(decrypted_padded_password).decode('utf-8')

def pad(data):
    # Pads the data to make sure its length is a multiple of 16 bytes
    block_size = 16
    padding_needed = block_size - (len(data) % block_size)
    return data + (chr(padding_needed) * padding_needed).encode()

def unpad(padded_data):
    # Remove padding from the data
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]