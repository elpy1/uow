#!/usr/bin/env python
import socket
import rsa_encryption as rsa


def message_send():
    """Prompts user for message, prints it and returns it encoded in bytes"""
    prompt = f'[{nickname}]: '
    msg = f'{prompt}{input(prompt)}'
    return bytes(msg, 'utf-8')


# bind only to localhost (use 0.0.0.0 to listen on all interfaces)
host = '127.0.0.1'
port = 33333
# nicknames for chat
nickname = 'server'
recipient = 'client'

# private key (for decrypting messages)
private_key_file = f'keys/{nickname}.key'
# recipient public key (for encrypting messages)
public_key_file = f'keys/{recipient}.pub'

try:
    # load keys
    pub_key = rsa.load_public_key_file(public_key_file)
    priv_key = rsa.load_private_key_file(private_key_file)
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to port
    s.bind((host, port))
    # only useful for a single chat participant
    s.listen(1)

    print('[*] server started. waiting for connection')

    while True:
        conn, addr = s.accept()
        print('[*] client connected')
        while True:
            client_data = conn.recv(1024)
            if not client_data:
                break
            decrypted = rsa.decrypt(priv_key, client_data)
            print(decrypted.decode('utf-8'))
            conn.send(rsa.encrypt(pub_key, message_send()))
        conn.close()
        print('[*] client disconnected')
except KeyboardInterrupt:
    print('Keyboard interrupt. Exiting')
except ValueError:
    pass
finally:
    s.close()
