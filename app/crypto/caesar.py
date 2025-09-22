# app/crypto/caesar.py
# -*- coding: utf-8 -*-

RU_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RU_UPPER = RU_LOWER.upper()
EN_LOWER = "abcdefghijklmnopqrstuvwxyz"
EN_UPPER = EN_LOWER.upper()

def _alphabet_for(ch: str):
    """Вернёт (lower, upper) алфавит под символ или None если не буква."""
    if ch in RU_LOWER or ch in RU_UPPER:
        return RU_LOWER, RU_UPPER
    if ch in EN_LOWER or ch in EN_UPPER:
        return EN_LOWER, EN_UPPER
    return None

def _shift_char(ch: str, k: int) -> str:
    alph = _alphabet_for(ch)
    if not alph:
        return ch
    lower, upper = alph
    if ch.isupper():
        idx = upper.index(ch)
        return upper[(idx + k) % len(upper)]
    else:
        idx = lower.index(ch)
        return lower[(idx + k) % len(lower)]

def caesar_encrypt(text: str, shift: int) -> str:
    """Сдвиг вправо на shift (RU/EN, сохраняет регистр, небуквы не трогаем)."""
    return "".join(_shift_char(c, shift) for c in text)

def caesar_decrypt(text: str, shift: int) -> str:
    """Обратный сдвиг."""
    return "".join(_shift_char(c, -shift) for c in text)

# ---- Совместимость со старым кодом ----
def caesar(text: str, shift: int) -> str:
    """Старое имя: ведёт себя как шифрование (сдвиг вправо)."""
    return caesar_encrypt(text, shift)
