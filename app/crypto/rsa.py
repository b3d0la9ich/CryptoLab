from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Для демонстрации: генерируем пару на лету
def encrypt_decrypt(text: str):
    key = RSA.generate(2048)
    pub = key.publickey()
    enc_cipher = PKCS1_OAEP.new(pub)
    dec_cipher = PKCS1_OAEP.new(key)
    enc = enc_cipher.encrypt(text.encode('utf-8'))
    dec = dec_cipher.decrypt(enc)
    return base64.b64encode(enc).decode('utf-8'), dec.decode('utf-8')
