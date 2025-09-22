# app/crypto/rsa.py
# -*- coding: utf-8 -*-

import base64
from typing import Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


# ===== Генерация ключей =====

def generate_keypair(bits: int = 2048) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Генерирует пару RSA ключей."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def private_to_pem(priv: rsa.RSAPrivateKey) -> str:
    """Приватный ключ -> PEM (PKCS#8, без пароля)."""
    pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem.decode('utf-8')


def public_to_pem(pub: rsa.RSAPublicKey) -> str:
    """Публичный ключ -> PEM (SubjectPublicKeyInfo)."""
    pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem.decode('utf-8')


def pem_to_private(pem: str) -> rsa.RSAPrivateKey:
    return serialization.load_pem_private_key(
        pem.encode('utf-8'),
        password=None,
        backend=default_backend()
    )


def pem_to_public(pem: str) -> rsa.RSAPublicKey:
    return serialization.load_pem_public_key(
        pem.encode('utf-8'),
        backend=default_backend()
    )


# ===== Шифрование / расшифрование OAEP(SHA-256) =====

def rsa_encrypt_b64(plaintext: str, public_pem: str) -> str:
    """
    Шифрует строку UTF-8 публичным ключом (PEM) с OAEP(SHA-256).
    Возвращает Base64(шифртекст).
    """
    pub = pem_to_public(public_pem)
    ct = pub.encrypt(
        plaintext.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )
    return base64.b64encode(ct).decode('utf-8')


def rsa_decrypt_b64(cipher_b64: str, private_pem: str) -> str:
    """
    Дешифрует Base64(шифртекст) приватным ключом (PEM) с OAEP(SHA-256).
    Возвращает исходную строку UTF-8.
    """
    priv = pem_to_private(private_pem)
    ct = base64.b64decode(cipher_b64.encode('utf-8'))
    pt = priv.decrypt(
        ct,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )
    return pt.decode('utf-8')


# ===== Совместимость со старым кодом =====

def encrypt_decrypt(text: str) -> Tuple[str, str]:
    """
    Совместимая функция для уже написанных view/template:
    генерирует пару ключей, шифрует текст, тут же расшифровывает.
    Возвращает (enc_b64, dec_text).
    """
    priv, pub = generate_keypair()
    pub_pem = public_to_pem(pub)
    priv_pem = private_to_pem(priv)
    enc_b64 = rsa_encrypt_b64(text, pub_pem)
    dec_text = rsa_decrypt_b64(enc_b64, priv_pem)
    return enc_b64, dec_text


# ===== Утилиты для UI (если нужно показать ключи пользователю) =====

def generate_keypair_pem(bits: int = 2048) -> Tuple[str, str]:
    """
    Возвращает пару PEM-строк (private_pem, public_pem) для отображения/сохранения.
    """
    priv, pub = generate_keypair(bits)
    return private_to_pem(priv), public_to_pem(pub)
