from os import urandom, path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from json import load, dump
import random

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

def decrypt(string, keyAES, keyChaCha):
    # ChaCha
    string = ChaCha20Poly1305(keyChaCha).decrypt(string[:12], string[12:], None)
    
    # AES
    string = AESGCM(keyAES).decrypt(string[:12], string[12:], None)
    
    return string 

def loadFiles():
    if path.exists('files.json'):
        try:
            with open('files.json', 'r') as f: 
                return load(f)
        except:
                print('Error loading files.json')
                exit()
    else: return {}

def saveFiles(files):
    with open('files.json', 'w') as f:
        dump(files, f, indent=1)
