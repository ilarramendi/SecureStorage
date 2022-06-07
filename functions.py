import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from json import loads, load, dumps, dump

def encrypt(string, key):
    if not key: key = os.urandom(32)
    nonce = os.urandom(12)
    
    return (nonce + AESGCM(key).encrypt(nonce, string, None), key.decode('ISO-8859-1'))

def decrypt(string, key):
    return AESGCM(key).decrypt(string[:12], string[12:], None)

def loadFiles(key):
    try:
        data = ''
        with open('files.ENCRYPTED', 'rb') as f: data = f.read()

        # Decrypt files.ENCRYPTED and load as a json
        return loads(decrypt(data, key), encoding='ISO-8859-1')
    except:
        if os.path.exists('files.ENCRYPTED'):
            print('Error loading files.ENCRYPTED')
            exit()
        else: return {}

def saveFiles(files, key):
    res = encrypt(str.encode(dumps(files, ensure_ascii=False)), key)
    with open('files.ENCRYPTED', 'wb') as f:
        f.write(res[0])