#!/usr/bin/env python
import os
import rsa_encryption as rsa

# get full path to directory where script was run
cwd = os.path.dirname(os.path.realpath(__file__))

# get user's chat nickname for writing key files
print('enter your nickname: ', end='')

# full file path
file = f'{cwd}/{input()}'

# generate a new private key
p = rsa.generate_private_key()

# save private key to <username>.key and public key to <username>.pub
rsa.save_keys_to_file(p, file)

print('success: keypair created and saved to current directory')
