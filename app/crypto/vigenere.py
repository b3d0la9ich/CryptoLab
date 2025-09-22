# -*- coding: utf-8 -*-
# Поддержка RU/EN, сохранение регистра, небуквенные символы не трогаем.
# Совместимость: есть и vigenere_encrypt/vigenere_decrypt, и vigenere(text, key, encrypt=True)

RU = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
EN = "abcdefghijklmnopqrstuvwxyz"

def _alphabets_for(ch: str):
    lo = ch.lower()
    if lo in RU:
        return RU, RU.upper()
    if lo in EN:
        return EN, EN.upper()
    return None, None

def _kseq(text: str, key: str):
    # последовательность сдвигов по буквам ключа (небуквы ключа игнорируем)
    kletters = [c for c in key if c.isalpha()]
    if not kletters:
        return [0] * len(text)
    res, j = [], 0
    for c in text:
        lo, up = _alphabets_for(c)
        if lo:
            kch = kletters[j % len(kletters)]
            klo, kup = _alphabets_for(kch)
            if not klo:
                res.append(0)   # ключ из другого алфавита → мягко даём 0-сдвиг
            else:
                res.append(klo.index(kch.lower()))
            j += 1
        else:
            res.append(0)
    return res

def vigenere_encrypt(text: str, key: str) -> str:
    ks = _kseq(text, key)
    out = []
    for c, k in zip(text, ks):
        lo, up = _alphabets_for(c)
        if not lo:
            out.append(c); continue
        if c.isupper():
            i = up.index(c)
            out.append(up[(i + k) % len(up)])
        else:
            i = lo.index(c)
            out.append(lo[(i + k) % len(lo)])
    return "".join(out)

def vigenere_decrypt(text: str, key: str) -> str:
    ks = _kseq(text, key)
    out = []
    for c, k in zip(text, ks):
        lo, up = _alphabets_for(c)
        if not lo:
            out.append(c); continue
        if c.isupper():
            i = up.index(c)
            out.append(up[(i - k) % len(up)])
        else:
            i = lo.index(c)
            out.append(lo[(i - k) % len(lo)])
    return "".join(out)

# ---- Совместимость со старым кодом ----
def vigenere(text: str, key: str, encrypt: bool = True) -> str:
    """Старое имя. encrypt=True → шифр, False → дешифр."""
    return vigenere_encrypt(text, key) if encrypt else vigenere_decrypt(text, key)
