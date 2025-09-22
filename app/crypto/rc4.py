# app/crypto/rc4.py
# -*- coding: utf-8 -*-
"""
RC4 (ARC4) — учебная реализация.

API:
- rc4_encrypt(plaintext:str, key:str) -> str           # Base64(шифртекст) — имя, которого ждут твои views
- rc4_decrypt(cipher_b64:str, key:str) -> str          # расшифровка из Base64 в UTF-8 строку

Дополнительно оставлены функции:
- rc4_encrypt_b64 / rc4_decrypt_b64 (идентичные по поведению)
- rc4(text, key, encrypt=True) — совместимая обёртка
"""
import base64
from typing import Iterable


def _ksa(key_bytes: bytes) -> list:
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]
    return S


def _prga(S: list) -> Iterable[int]:
    i = j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]


def _rc4_bytes(key_bytes: bytes, data: bytes) -> bytes:
    if not (1 <= len(key_bytes) <= 256):
        raise ValueError("Длина ключа RC4 должна быть от 1 до 256 байт")
    S = _ksa(key_bytes)
    keystream = _prga(S)
    return bytes([b ^ next(keystream) for b in data])


# ===== Основные функции, которых ждут твои views =====

def rc4_encrypt(plaintext: str, key: str) -> str:
    """Шифрует строку UTF-8 и возвращает Base64(шифртекст)."""
    pt = plaintext.encode("utf-8")
    kb = key.encode("utf-8")
    ct = _rc4_bytes(kb, pt)
    return base64.b64encode(ct).decode("utf-8")


def rc4_decrypt(cipher_b64: str, key: str) -> str:
    """Дешифрует Base64(шифртекст) и возвращает строку UTF-8."""
    ct = base64.b64decode(cipher_b64.encode("utf-8"))
    kb = key.encode("utf-8")
    pt = _rc4_bytes(kb, ct)
    return pt.decode("utf-8", errors="replace")


# ===== Синонимы (если где-то используются b64-имена) =====

def rc4_encrypt_b64(plaintext: str, key: str) -> str:
    return rc4_encrypt(plaintext, key)


def rc4_decrypt_b64(cipher_b64: str, key: str) -> str:
    return rc4_decrypt(cipher_b64, key)


# ===== Совместимая обёртка =====

def rc4(text: str, key: str, encrypt: bool = True) -> str:
    return rc4_encrypt(text, key) if encrypt else rc4_decrypt(text, key)
