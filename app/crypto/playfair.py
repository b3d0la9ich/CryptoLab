import string

def _prepare_key(key: str):
    key = ''.join(ch for ch in key.lower() if ch.isalpha()).replace('j','i')
    seen = set()
    alphabet = "abcdefghiklmnopqrstuvwxyz"  # без j
    table = []
    for ch in key + alphabet:
        if ch not in seen:
            seen.add(ch); table.append(ch)
    # 5x5
    return [table[i*5:(i+1)*5] for i in range(5)]

def _pos(tbl, ch):
    ch = 'i' if ch == 'j' else ch
    for r in range(5):
        for c in range(5):
            if tbl[r][c] == ch:
                return r, c
    raise ValueError(ch)

def _prepare_text(txt: str):
    s = ''.join(ch for ch in txt.lower() if ch.isalpha()).replace('j','i')
    digrams = []
    i = 0
    while i < len(s):
        a = s[i]; b = s[i+1] if i+1 < len(s) else 'x'
        if a == b:
            digrams.append((a, 'x')); i += 1
        else:
            digrams.append((a, b)); i += 2
    if len(digrams[-1]) == 1:
        digrams[-1] = (digrams[-1][0], 'x')
    return digrams

def playfair_encrypt(text: str, key: str) -> str:
    tbl = _prepare_key(key)
    res = []
    for a,b in _prepare_text(text):
        ra, ca = _pos(tbl, a); rb, cb = _pos(tbl, b)
        if ra == rb:
            res.append(tbl[ra][(ca+1)%5] + tbl[rb][(cb+1)%5])
        elif ca == cb:
            res.append(tbl[(ra+1)%5][ca] + tbl[(rb+1)%5][cb])
        else:
            res.append(tbl[ra][cb] + tbl[rb][ca])
    return ''.join(res).upper()

def playfair_decrypt(cipher: str, key: str) -> str:
    tbl = _prepare_key(key)
    s = ''.join(ch for ch in cipher.lower() if ch.isalpha()).replace('j','i')
    res = []
    for i in range(0, len(s), 2):
        a, b = s[i], s[i+1] if i+1 < len(s) else 'x'
        ra, ca = _pos(tbl, a); rb, cb = _pos(tbl, b)
        if ra == rb:
            res.append(tbl[ra][(ca-1)%5] + tbl[rb][(cb-1)%5])
        elif ca == cb:
            res.append(tbl[(ra-1)%5][ca] + tbl[(rb-1)%5][cb])
        else:
            res.append(tbl[ra][cb] + tbl[rb][ca])
    return ''.join(res).upper()
