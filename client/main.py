from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64
import random

# 生产随机域名


def generate_domain() -> str:
    domain = random.getrandbits(64)
    domain = hex(domain)[2:]
    return domain + ".xiaomian"


def generate_key():

    # Generate a new RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Convert keys to bytes
    private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Encode bytes as base64 
    private_key_base64 = base64.b64encode(private_key_bytes).decode('utf-8')
    public_key_base64 = base64.b64encode(public_key_bytes).decode('utf-8')
    
    return private_key_base64,public_key_base64



# # Encrypt a message using the public key
# message = b"Hello World"
# encrypted_message = public_key.encrypt(
#     message,
#     padding.OAEP(
#         mgf=padding.MGF1(algorithm=hashes.SHA256()),
#         algorithm=hashes.SHA256(),
#         label=None
#     )
# )

# # Decrypt the message using the private key
# decrypted_message = private_key.decrypt(
#     encrypted_message,
#     padding.OAEP(
#         mgf=padding.MGF1(algorithm=hashes.SHA256()),
#         algorithm=hashes.SHA256(),
#         label=None
#     )
# )
# print(decrypted_message)
if __name__ == '__main__':
    print("Welcome to my xiaomiao tor network")
    domain = generate_domain()
    private_key_base64,public_key_base64 = generate_key()
