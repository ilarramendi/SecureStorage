import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from json import loads, load, dumps, dump

def encrypt(string, key):
    if not key: key = os.urandom(32)
    
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    # Add random padding
    padding = os.urandom(16)
    num = int((1 - len(string) / 16 + len(string) // 16) * 16)
    if num == 16: num = 0
    
    string = padding[0:num] + string

    return (cipher.encryptor().update(string), iv.decode('ISO-8859-1'), num, key.decode('ISO-8859-1'))

def decrypt(string, key, iv, padding):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv.encode('ISO-8859-1')), backend=backend)
    
    return cipher.decryptor().update(string)[padding:]

def loadFiles(key):
    try:
        files = {}
        with open('files.json', 'rb') as f: files = load(f)

        # Decrypt files.ENCRYPTED and load as a json
        return loads(decrypt(files['data'].encode('ISO-8859-1'), key, files['IV'], files['padding']), encoding='ISO-8859-1')
    except:
        if os.path.exists('files.json') or os.path.exists('files.ENCRYPTED'):
            print('Error loading files.json')
            exit()
        else: return {}

def saveFiles(files, key):
    res = encrypt(str.encode(dumps(files, ensure_ascii=False)), key)
    with open('files.json', 'w') as f:
        dump({'IV': res[1], 'padding': res[2], 'data': res[0].decode('ISO-8859-1')}, f, indent=1, ensure_ascii=False)    