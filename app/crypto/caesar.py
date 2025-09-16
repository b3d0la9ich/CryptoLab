import string
ALPH = string.ascii_lowercase

def shift_char(ch, shift):
    if ch.lower() not in ALPH:
        return ch
    base = ALPH.index(ch.lower())
    res = ALPH[(base + shift) % 26]
    return res.upper() if ch.isupper() else res

def caesar(text: str, shift: int) -> str:
    return ''.join(shift_char(c, shift) for c in text)
    