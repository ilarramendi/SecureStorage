from sys import argv, getsizeof
from random import randint
from datetime import datetime

from functions import encrypt, loadFiles, saveFiles, decrypt

key = argv[1].encode('ascii')

# Loads encrypted files metadata
files = loadFiles(key)

if argv[2] == 'encrypt':
    # Generate new random name
    fileName = str(randint(1000000000, 9999999999))
    while fileName in files: fileName = str(randint(1000000000, 9999999999))

    # Open file to encrypt and encrypt content
    res = ''
    with open(argv[3], 'rb') as f: 
        res = f.read()
    res = encrypt(res, False)

    # Write encrypted data
    with open(fileName + '.ENCRYPTED', 'wb') as f:
        f.write(res[0])

    # Store nonce, padding and name
    files[fileName] = {
        'name': argv[3].rpartition('/')[2],
        'date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
        'key': res[1]
    }

    # Encrypt and store files metadata
    saveFiles(files, key)

    print(f"Successfully encrypted {argv[3]} as {fileName}.ENCRYPTED")

elif argv[2] == 'decrypt':
    info = {}
    name = argv[3].rpartition('.')[0].rpartition('/')[2]
    if name in files: info = files[name]
    else:
        print('File not found')
        exit()

    # Open the file, decrypt it and store it to the new file
    with open(argv[3], 'rb') as f:
        with open(info['name'], 'wb') as f2:
            f2.write(decrypt(f.read(), info['key'].encode('ISO-8859-1')))
        print(f"Successfuly decrypted {argv[3]} as {info['name']}")

elif argv[2] == 'list': 
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

else: print(f"Wrong action {argv[2]}")
