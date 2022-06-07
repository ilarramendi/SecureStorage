from sys import argv, getsizeof
from random import randint
from datetime import datetime

from functions import encrypt, loadFiles, saveFiles, decrypt

key = b"super secret passw that cant sen"

# Loads encrypted files metadata
files = loadFiles(key)

if argv[1] == 'encrypt':
    # Generate new random name
    fileName = str(randint(1000000000, 9999999999))
    while fileName in files: fileName = str(randint(1000000000, 9999999999))

    # Open file to encrypt and encrypt content
    res = []
    with open(argv[2], 'rb') as f: 
        res = encrypt(f.read(), key)

    # Write encrypted data
    with open(fileName + '.ENCRYPTED', 'wb') as f:
        f.write(res[0])

    # Store IV, padding and name
    files[fileName] = {
        'IV': res[1],
        'padding': res[2],
        'name': argv[2].rpartition('/')[2],
        'date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
    }

    # Encrypt and store files metadata
    saveFiles(files, key)

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
            f2.write(decrypt(f.read(), key, info['IV'], info['padding']))

    print(f"Successfuly decrypted {argv[2]} as {info['name']}")

elif argv[1] == 'list': 
    maxLength = 0
    for name in files:
        length = len(files[name]['name'])
        if length > maxLength: maxLength = length

    print(f"\nName{' ' * (maxLength - 4)} | Encrypted Name       | Date")
    print(f"-------{'-' * (maxLength - 4)}-------------------------------------------")
    for name in files:
        item = files[name]
        print(f"{item['name']}{' ' * (maxLength - len(item['name']))} | {name}.ENCRYPTED | {item['date']}")
    print()

else: print(f"Wrong action {argv[1]}")
