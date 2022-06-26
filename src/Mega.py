from subprocess import run, DEVNULL

def download(email, password, file):
    # Log out if logged in already
    run(['mega-logout'], stdout=DEVNULL)

    # Login with new credentials
    if run(['mega-login', email, password], stdout=DEVNULL).returncode == 0:
        print('[MEGA] Logged in successfuly')

        # download file
        success = run(['mega-get', file], stdout=DEVNULL).returncode  == 0

        print('[MEGA] Successfuly downloaded:' if success 
                else '[MEGA] Error downloading:',
                file)

        # Log out
        run(['mega-logout'], stdout=DEVNULL)
        return success
    else:
        return print('[MEGA] Error loggin in.')

def upload(email, password, file):
    # Log out if logged in already
    run(['mega-logout'], stdout=DEVNULL)

    # Login with new credentials
    if run(['mega-login', email, password], stdout=DEVNULL).returncode == 0:
        print('[MEGA] Logged in successfuly')

        # Upload file
        success = run(['mega-put', file], stdout=DEVNULL).returncode == 0
        
        print('[MEGA] Successfuly uploaded' if success
                else '[MEGA] Error uploading:',
                file)
        
        # Log out
        run(['mega-logout'], stdout=DEVNULL)
        return success

    else:
        return print('[MEGA] Error loggin in.')
