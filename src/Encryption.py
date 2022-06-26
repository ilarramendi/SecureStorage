from os import urandom
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

def encrypt(string, keyAES = False, keyChaCha = False):
    # Encrypt with AES
    if not keyAES: keyAES = urandom(32)
    nonceAES = urandom(12)
    string = nonceAES + AESGCM(keyAES).encrypt(nonceAES, string, None)

    # Encrypt with ChaCha20
    if not keyChaCha: keyChaCha = urandom(32)
    nonceChaCha = urandom(12)
    string = nonceChaCha + ChaCha20Poly1305(keyChaCha).encrypt(nonceChaCha, string, None)

    return {
        'result': string,
        'AES': keyAES,
        'ChaCha': keyChaCha
    }

def decrypt(bytes, keyAES, keyChaCha):
    # ChaCha
    bytes = ChaCha20Poly1305(keyChaCha).decrypt(bytes[:12], bytes[12:], None)
    
    # AES
    bytes = AESGCM(keyAES).decrypt(bytes[:12], bytes[12:], None)
    
    return bytes 