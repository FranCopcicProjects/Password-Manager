import base64
import hmac
import sys
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256, SHA512
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

def main():
    if sys.argv[1] == 'init':
        first_encription = encrypt('First Encryption', sys.argv[2])
        with open('database.db', 'wt') as file:
            file.write(first_encription)
        create_hmac(first_encription, sys.argv[2])
        print('Password manager initialized.')
    elif sys.argv[1] == 'put':
        with open('database.db', 'rt') as file:
            db_content = file.read()

        if not check_hmac(db_content, sys.argv[2]):
            print('Master password incorrect or integrity check failed.')
            return

        decrypted = decrypt(db_content, sys.argv[2])
        if not decrypted:
            return
        decrypted_pairs = decrypted.split('\n')
        pairs = {}
        for pair in decrypted_pairs:
            parts = pair.split(' ')
            if len(parts) == 2:
                pairs[parts[0]] = parts[1]

        pairs[sys.argv[3]] = sys.argv[4]
        txt_to_enc = ''
        for adress in pairs.keys():
            txt_to_enc += adress + ' ' + pairs[adress] + '\n'

        new_encription = encrypt(txt_to_enc, sys.argv[2])
        with open('database.db', 'wt') as file:
            file.write(new_encription)

        create_hmac(new_encription, sys.argv[2])
        print(f'Stored password for {sys.argv[3]}.')

    elif sys.argv[1] == 'get':
        with open('database.db', 'rt') as file:
            db_content = file.read()

        if not check_hmac(db_content, sys.argv[2]):
            print('Master password incorrect or integrity check failed.')
            return

        decrypted = decrypt(db_content, sys.argv[2])
        if not decrypted:
            return
        decrypted_pairs = decrypted.split('\n')
        pairs = {}
        for pair in decrypted_pairs:
            parts = pair.split(' ')
            if len(parts) == 2:
                pairs[parts[0]] = parts[1]
        if sys.argv[3] in pairs:
            print(f'Password for {sys.argv[3]} is {pairs[sys.argv[3]]}.')
        else:
            print('There is no password for this address.')
    else:
        print('Wrong command.')


def encrypt(txt_to_enc, key):
    try:
        salt = get_random_bytes(16)
        iv = get_random_bytes(16)
        with open('saltIV.bin', 'wb') as file:
            file.write(iv)
            file.write(salt)
        secret_key = PBKDF2(key.encode(), salt, dkLen=32, count=65536, hmac_hash_module=SHA256)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        encrypted_bytes = cipher.encrypt(pad(txt_to_enc.encode(), AES.block_size))
        return base64.b64encode(encrypted_bytes).decode()
    except Exception:
        print('Encryption error.')
        return None

def create_hmac(data, key):
    try:
        with open('saltIV.bin', 'rb') as file:
            iv = file.read(16)
            salt = file.read(16)
        secret_key = PBKDF2(key.encode(), salt, dkLen=32, count=65536, hmac_hash_module=SHA256)
        h = HMAC.new(secret_key, digestmod=SHA512)
        h.update(data.encode())
        with open('hmac.bin', 'wb') as file:
            file.write(h.digest())
        return
    except Exception:
        print('HMAC creation error.')
        return None

def decrypt(txt_to_dec, key):
    try:
        with open('saltIV.bin', 'rb') as file:
            iv = file.read(16)
            salt = file.read(16)
        secret_key = PBKDF2(key.encode(), salt, dkLen=32, count=65536, hmac_hash_module=SHA256)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        decrypted_bytes = cipher.decrypt(base64.b64decode(txt_to_dec))
        return unpad(decrypted_bytes, AES.block_size).decode()
    except Exception:
        return None

def check_hmac(data, key):
    try:
        with open('saltIV.bin', 'rb') as file:
            iv = file.read(16)
            salt = file.read(16)
        secret_key = PBKDF2(key.encode(), salt, dkLen=32, count=65536, hmac_hash_module=SHA256)
        h = HMAC.new(secret_key, digestmod=SHA512)
        h.update(data.encode())
        calculated_hmac = h.digest()
        with open('hmac.bin', 'rb') as file:
            stored_hmac = file.read()
        return hmac.compare_digest(stored_hmac, calculated_hmac)
    except Exception:
        return False

if __name__ == '__main__':
    main()

