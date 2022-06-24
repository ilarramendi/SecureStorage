from base64 import b64encode
from datetime import datetime
from json import dumps
from subprocess import call
from sys import argv

ID = argv[1]
name = 'SecureStorage'

base = {
    'object': 'item',
    'id': ID,
    'organizationId': None,
    'folderId': None,
    'type': 2,
    'reprompt': 0,
    'name': 'SecureStorage',
    'notes': '',
    'favorite': True,
    'secureNote': {'type': 0},
    'collectionIds': [],
    'revisionDate': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    'deletedDate': None
}

with open('files.json', 'r') as f:
    base['notes'] = f.read()

call(['bw', 'edit', 'item', ID, b64encode(dumps(base).encode()).decode()])