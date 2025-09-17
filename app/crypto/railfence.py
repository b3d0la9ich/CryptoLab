def railfence_encrypt(text: str, rails: int) -> str:
    rows = [''] * rails
    r, step = 0, 1
    for ch in text:
        rows[r] += ch
        if r == 0: step = 1
        elif r == rails-1: step = -1
        r += step
    return ''.join(rows)

def railfence_decrypt(cipher: str, rails: int) -> str:
    # восстановим траекторию
    n = len(cipher)
    pattern = [0]*n
    r, step = 0, 1
    for i in range(n):
        pattern[i] = r
        if r == 0: step = 1
        elif r == rails-1: step = -1
        r += step
    # посчитаем длины для каждой рельсы
    counts = [pattern.count(j) for j in range(rails)]
    idx = [0]*rails
    start = 0
    rails_str = []
    for c in counts:
        rails_str.append(cipher[start:start+c])
        start += c
    # собираем по узору
    out = []
    for i in range(n):
        r = pattern[i]
        out.append(rails_str[r][idx[r]])
        idx[r] += 1
    return ''.join(out)
