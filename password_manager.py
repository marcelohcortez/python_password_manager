import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from key import masterPassword

salt = os.urandom(16)
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000)
key = base64.urlsafe_b64encode(kdf.derive(masterPassword.encode()))
fern = Fernet(key)

def view():
    with open('data.txt', 'r') as file:
        for line in file.readlines():
            data = line.rstrip()
            user, passw = data.split(";")
            print(f'User: {user}\nPassword: {fern.decrypt(passw.encode()).decode()}\n\n')

def add():
    name = input('User: ')
    pwd = input('Password: ')

    with open('data.txt', 'a') as file:
        file.write(f'{name};{fern.encrypt(pwd.encode()).decode()}\n')


def program():
    inputPassword = input('What is the master password? \n')

    if inputPassword == masterPassword:
        while True:

            mode = input('Do you want to add a entry (ADD), view all entries (VIEW) or quit (Q)? \n').lower()

            if mode == 'q':
                break

            elif mode == 'view':
                view()
                continue

            elif mode == 'add':
                add()
                continue
            
            else:
                print('That\'s not a valid option. Try again.\n')
                continue
    else:
        fail = input('Wrong password. Try again (TRY) or quit (Q)? \n').lower()

        if fail == 'q':
            exit()
        
        elif fail == 'try':
            program()

        else:
            print('That\'s not a valid option. Try again.\n')
            program()

program()

