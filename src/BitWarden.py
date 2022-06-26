from base64 import b64encode
from json import dumps, loads
from subprocess import check_output, DEVNULL, run


def updateNote(content, id):
    # Sync vault first
    if run(['bw', 'sync'], stdout=DEVNULL).returncode == 0:
        # Get base item from BitWarden
        item = loads(check_output(['bw', 'get', 'item', id]).decode())
        
        # Set content as notes
        item['notes'] = content

        # Encode to base64 string
        encoded = b64encode(dumps(item).encode()).decode()

        # Update item
        if run(['bw', 'edit', 'item', id, encoded], stdout=DEVNULL).returncode == 0:
            print('[Bitwarden] Successfully updated item:', item['name'])
            return True
        else:
            return print('[Bitwarden] Successfully updated item:', item['name'])
    return print('[Bitwarden] Error syincing.')

def getNote(id):
    # Sync vault first
    if run(['bw', 'sync'], stdout=DEVNULL).returncode == 0:
        # Get item
        item = loads(check_output(['bw', 'get', 'item', id]).decode())
        name = item['name']
        
        try:
            # Parse json from item notes
            item = loads(item['notes'])
            
            print('[Bitwarden] Successfuly loaded item:', name)
            return item
        except:
            return print('[Bitwarden] Error loading:', name)
    return print('[Bitwarden] Error syincing.')
