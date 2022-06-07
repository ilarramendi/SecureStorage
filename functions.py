from os import urandom, path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend
from json import loads, load, dumps, dump

def encrypt(string, keyAES = False, keyChaCha = False):
    if not keyAES: keyAES = urandom(32)
    if not keyChaCha: keyChaCha = urandom(32)

    nonce = urandom(12)
    nonce2 = urandom(12)

    string = nonce + AESGCM(keyAES).encrypt(nonce, string, None)
    string = nonce2 + ChaCha20Poly1305(keyChaCha).encrypt(nonce2, string, None)
    
    return (string, keyAES.decode('ISO-8859-1'), keyChaCha.decode('ISO-8859-1'))

def decrypt(string, keyAES, keyChaCha):
    string = ChaCha20Poly1305(keyChaCha).decrypt(string[:12], string[12:], None)
    return AESGCM(keyAES).decrypt(string[:12], string[12:], None)

def loadFiles(key):
    try:
        data = ''
        with open('files.ENCRYPTED', 'rb') as f: data = f.read()

        # Decrypt files.ENCRYPTED and load as a json
        return loads(decrypt(data, key, key), encoding='ISO-8859-1')
    except:
        if path.exists('files.ENCRYPTED'):
            print('Error loading files.ENCRYPTED')
            exit()
        else: return {}

def saveFiles(files, key):
    res = encrypt(str.encode(dumps(files, ensure_ascii=False)), key, key)
    with open('files.ENCRYPTED', 'wb') as f:
        f.write(res[0])