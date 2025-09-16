from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# Демонстрация AES-CBC (учебный пример)
def encrypt_cbc(text: str, key: bytes):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ct).decode('utf-8')

def decrypt_cbc(b64: str, key: bytes):
    raw = base64.b64decode(b64)
    iv, ct = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')
