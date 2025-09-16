import string
ALPH = string.ascii_lowercase

def vigenere(text: str, key: str, encrypt=True) -> str:
    key = ''.join([c.lower() for c in key if c.isalpha()])
    if not key:
        return text
    out, ki = [], 0
    for ch in text:
        if ch.lower() in ALPH:
            k = ALPH.index(key[ki % len(key)])
            t = ALPH.index(ch.lower())
            r = (t + k) % 26 if encrypt else (t - k) % 26
            out.append(ALPH[r].upper() if ch.isupper() else ALPH[r])
            ki += 1
        else:
            out.append(ch)
    return ''.join(out)
