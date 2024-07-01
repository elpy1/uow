#!/usr/bin/env python
import socket
import rsa_encryption as rsa


def message_send():
    """Prompts user for message, prints it and returns it encoded in bytes"""
    prompt = f'[{nickname}]: '
    msg = f'{prompt}{input(prompt)}'
    return bytes(msg, 'utf-8')


# server host and port
host = '127.0.0.1'
port = 33333
# nickname for chat
nickname = 'client'
recipient = 'server'
# load keys
pub_key = rsa.load_public_key_file(f'keys/{recipient}.pub')
priv_key = rsa.load_private_key_file(f'keys/{nickname}.key')

try:
    # create socket and connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print('[*] connected to server')

    # loop for sending and receiving data over socket
    while True:
        encrypted = rsa.encrypt(pub_key, message_send())
        s.send(encrypted)
        data = s.recv(1024)
        decrypted = rsa.decrypt(priv_key, data)
        print(decrypted.decode('utf-8'))
except KeyboardInterrupt:
    print('Keyboard interrupt. Exiting.')
except socket.error as e:
    raise SystemExit(f'Socket error: {e}') from e
except ValueError:
    pass
