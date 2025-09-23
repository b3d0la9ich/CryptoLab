# app/crypto/rsa.py
# -*- coding: utf-8 -*-

import base64
from typing import Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


# ===== Генерация ключей =====

def generate_keypair(bits: int = 2048) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """Возвращает пару ключей (private_obj, public_obj)."""
    priv = rsa.generate_private_key(public_exponent=65537, key_size=bits)
    pub = priv.public_key()
    return priv, pub


def private_to_pem(priv: rsa.RSAPrivateKey) -> str:
    """Приватный ключ -> PEM (PKCS#8, без пароля)."""
    pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem.decode("utf-8")


def public_to_pem(pub: rsa.RSAPublicKey) -> str:
    """Публичный ключ -> PEM (SubjectPublicKeyInfo)."""
    pem = pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem.decode("utf-8")


def pem_to_private(pem: str) -> rsa.RSAPrivateKey:
    """PEM -> приватный ключ."""
    return serialization.load_pem_private_key(
        pem.encode("utf-8"),
        password=None,
    )


def pem_to_public(pem: str) -> rsa.RSAPublicKey:
    """PEM -> публичный ключ."""
    return serialization.load_pem_public_key(pem.encode("utf-8"))


# ===== Шифрование / расшифрование OAEP(SHA-256) =====

def rsa_encrypt_b64(plaintext: str, public_pem: str) -> str:
    """
    Шифрует строку UTF-8 публичным ключом (PEM) с OAEP(SHA-256).
    Возвращает Base64(шифртекст).
    """
    pub = pem_to_public(public_pem)
    ct = pub.encrypt(
        plaintext.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return base64.b64encode(ct).decode("utf-8")


def rsa_decrypt_b64(cipher_b64: str, private_pem: str) -> str:
    """
    Дешифрует Base64(шифртекст) приватным ключом (PEM) с OAEP(SHA-256).
    Возвращает исходную строку UTF-8.
    """
    priv = pem_to_private(private_pem)
    # убираем пробелы/переводы строк и валидируем Base64
    ct = base64.b64decode("".join(cipher_b64.split()).encode("utf-8"), validate=True)
    pt = priv.decrypt(
        ct,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return pt.decode("utf-8")


# ===== Утилиты для UI =====

def generate_keypair_pem(bits: int = 2048) -> Tuple[str, str]:
    """
    Возвращает пару PEM-строк (private_pem, public_pem) для отображения/сохранения.
    """
    priv, pub = generate_keypair(bits)
    return private_to_pem(priv), public_to_pem(pub)


# ===== Совместимость со старым кодом =====

def encrypt_decrypt(text: str) -> Tuple[str, str]:
    """
    Оставлено для совместимости со старыми view/template:
    генерирует пару ключей, шифрует текст, тут же расшифровывает.
    Возвращает (enc_b64, dec_text).
    """
    priv, pub = generate_keypair()
    pub_pem = public_to_pem(pub)
    priv_pem = private_to_pem(priv)
    enc_b64 = rsa_encrypt_b64(text, pub_pem)
    dec_text = rsa_decrypt_b64(enc_b64, priv_pem)
    return enc_b64, dec_text
