def railfence_encrypt(text: str, rails: int) -> str:
    if rails < 2: return text
    rows = [''] * rails
    r, step = 0, 1
    for ch in text:
        rows[r] += ch
        if r == 0: step = 1
        elif r == rails-1: step = -1
        r += step
    return ''.join(rows)

def railfence_decrypt(cipher: str, rails: int) -> str:
    if rails < 2: return cipher
    # вычисляем длины строк
    pattern = []
    r, step = 0, 1
    for _ in cipher:
        pattern.append(r)
        if r == 0: step = 1
        elif r == rails-1: step = -1
        r += step
    counts = [pattern.count(i) for i in range(rails)]
    # нарезаем
    idx = 0
    rows = []
    for c in counts:
        rows.append(list(cipher[idx:idx+c]))
        idx += c
    # восстановление
    res = []
    pos = [0]*rails
    for row in pattern:
        res.append(rows[row][pos[row]])
        pos[row] += 1
    return ''.join(res)
