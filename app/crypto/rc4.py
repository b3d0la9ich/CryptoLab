def _ksa(key_bytes):
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key_bytes[i % len(key_bytes)]) % 256
        s[i], s[j] = s[j], s[i]
    return s

def _prga(s, n):
    i = j = 0
    out = bytearray()
    for _ in range(n):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]
        out.append(k)
    return bytes(out)

def rc4_encrypt(text: str, key: str) -> bytes:
    data = text.encode('utf-8')
    key_b = key.encode('utf-8')
    s = _ksa(key_b)
    keystream = _prga(s, len(data))
    return bytes([d ^ k for d, k in zip(data, keystream)])

def rc4_decrypt(cipher: bytes, key: str) -> str:
    # RC4 симметричен: xor с тем же потоком
    key_b = key.encode('utf-8')
    s = _ksa(key_b)
    keystream = _prga(s, len(cipher))
    plain = bytes([c ^ k for c, k in zip(cipher, keystream)])
    return plain.decode('utf-8', errors='replace')
