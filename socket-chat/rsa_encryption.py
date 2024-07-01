from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes, serialization

# Functions below were created based on documentation at:
# https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa

def generate_private_key(keysize=3072):
    """
    Generate a new RSA private key.
    """
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=keysize
    )

def load_private_key_file(filename, password=None):
    """
    Load an on-disk private key in PEM format.
    """
    with open(filename, 'rb') as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=password,
        )
    return private_key

def load_public_key_file(filename):
    """
    Load an on-disk public key in PEM format.
    """
    with open(filename, 'rb') as f:
        public_key = load_pem_public_key(f.read())
    return public_key

def key_to_pem(private_key):
    """
    Serialize a loaded private key and return (private, public) in PEM format.
    """
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

def save_keys_to_file(private_key, filename):
    """
    Save key pair to file in PEM format.
    """
    priv, pub = key_to_pem(private_key)
    with open(filename + '.key', 'wb') as f:
        f.write(priv)
    with open(filename + '.pub', 'wb') as f:
        f.write(pub)

def generate_keypair(keysize=3072):
    """
    Generate a new RSA key pair and return (private, public) in PEM format.
    """
    private_key = generate_private_key(keysize=keysize)
    private_pem, public_pem = key_to_pem(private_key)
    return private_pem, public_pem

def encrypt(public_key, plaintext):
    """
    Encrypt plaintext message using public key.
    """
    return public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt(private_key, ciphertext):
    """
    Decrypt ciphertext using private key.
    """
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
