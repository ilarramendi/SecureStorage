from sys import argv
from datetime import datetime
from base64 import b64encode, b64decode
from os import urandom, path

from functions import encrypt, loadFiles, saveFiles, decrypt

# Loads encrypted files metadata
files = loadFiles()

if argv[1] == 'encrypt':
    # Open file to encrypt and encrypt content
    res = ''
    with open(argv[2], 'rb') as f: 
        res = f.read()
    res = encrypt(res)

    # Generate new random name
    fileName = False
    while not fileName or (fileName in files and path.exists(fileName + '.ENCRYPTED')):
        fileName = str(int.from_bytes(urandom(8), byteorder="big"))

    # Write encrypted data
    with open(fileName + '.ENCRYPTED', 'wb') as f:
        f.write(res['result'])

    # Store random keys, name and date
    files[fileName] = {
        'name': argv[2].rpartition('/')[2],
        'date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
        'AES': b64encode(res['AES']).decode('utf-8'),
        'ChaCha': b64encode(res['ChaCha']).decode('utf-8'),
    }
    saveFiles(files)

    print(f"Successfully encrypted {argv[2]} as {fileName}.ENCRYPTED")

elif argv[1] == 'decrypt':
    info = {}
    name = argv[2].rpartition('.')[0].rpartition('/')[2]
    if name in files: info = files[name]
    else:
        print('File not found')
        exit()

    # Open the file, decrypt it and store it to the new file
    with open(argv[2], 'rb') as f:
        with open(info['name'], 'wb') as f2:
            f2.write(decrypt(f.read(), b64decode(info['keyAES']), b64decode(info['keyChaCha'])))
        print(f"Successfuly decrypted {argv[2]} as {info['name']}")

else: print(f"Wrong action {argv[1]}")
