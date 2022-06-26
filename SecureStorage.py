from os import urandom, path, remove
from datetime import datetime
from base64 import b64encode, b64decode
from json import dumps

from src.Encryption import encrypt, decrypt
from src.BitWarden import updateNote, getNote
from src.Mega import upload, download

action = input('1) Upload\n2) Download\n')
files = getNote(input('Bitwarden item id: '))

if action == "1":
    original = ''
    while len(original) == 0 or not path.exists(original):
        original = input('Select a file: ')

    if files or files == '': 
        # Generate new random name
        fileName = False
        while not fileName or fileName in files:
            fileName = str(int.from_bytes(urandom(8), byteorder="big"))

        print('Selected name:', fileName)

        # Open file to encrypt and encrypt its content
        res = b''
        with open(original, 'rb') as f: 
            res = encrypt(f.read())
        
        # Write encrypted data
        out = fileName + '.ENCRYPTED'
        with open(out, 'wb') as f:
            f.write(res['result'])
        print('Successfuly encrypted file')

        try:
            # Store random keys, name and date
            files[fileName] = {
                'name': original.rpartition('/')[2],
                'date': datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
                'AES': b64encode(res['AES']).decode('utf-8'),
                'ChaCha': b64encode(res['ChaCha']).decode('utf-8'),
            }

            # Upload encrypted file
            if upload(input('Enter Mega username: '), input('Enter Mega password: '), out):
                if updateNote(dumps(files), id): 
                    remove(original)
                    print('DONE')
                else: print('Error updating note')
                remove(out)
        except KeyboardInterrupt:
            remove(out)
    else: print('Error loading note')

elif action == "2":    
    if files:
        fileName = ''
        info = None
        
        while not info:
            for (i, file) in enumerate(files):
                print(f"{i} | {file.ljust(20)} | {files[file]['date']} | {files[file]['name']}")
            number = input('Select a file: ')
            
            if number.isdecimal():
                number = int(number)
                
                if number > 0 and number < len(files):
                    fileName = list(files.keys())[number] + '.ENCRYPTED'
                    info = files[list(files.keys())[number]]
        
        if download(input('Enter Mega username: '), input('Enter Mega password: '), fileName):
            with open(fileName, 'rb') as f:
                with open(info['name'], 'wb') as f2:
                    f2.write(decrypt(f.read(), b64decode(info['AES']), b64decode(info['ChaCha'])))
                print(f"Successfuly decrypted {fileName} as {info['name']}")
            
            remove(fileName)
        else: print('Error downloading file')
    else: print('Error loading files.')

else: print(f"Wrong action {action}")