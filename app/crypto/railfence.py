# app/crypto/railfence.py
# -*- coding: utf-8 -*-

def railfence_encrypt(text: str, rails: int) -> str:
    """Классический «забор» без фильтрации символов: пробелы/пунктуация/цифры
    остаются и участвуют в зигзаге. Переводы строк тоже учитываются.
    """
    if rails < 2 or len(text) <= 1:
        return text

    rows = [[] for _ in range(rails)]
    r, step = 0, 1
    for ch in text:
        rows[r].append(ch)
        r += step
        if r == rails - 1 or r == 0:
            step *= -1
    return ''.join(''.join(row) for row in rows)


def railfence_decrypt(cipher: str, rails: int) -> str:
    """Обратное преобразование к encrypt выше (также без какой-либо фильтрации)."""
    n = len(cipher)
    if rails < 2 or n <= 1:
        return cipher

    # 1) Считаем, сколько символов придётся на каждую «рельсу»
    counts = [0] * rails
    r, step = 0, 1
    for _ in range(n):
        counts[r] += 1
        r += step
        if r == rails - 1 or r == 0:
            step *= -1

    # 2) Нарезаем шифртекст на куски по рельсам
    rails_data = []
    i = 0
    for c in counts:
        rails_data.append(list(cipher[i:i + c]))
        i += c

    # 3) Снова идём по зигзагу и собираем исходную строку
    out = []
    r, step = 0, 1
    for _ in range(n):
        out.append(rails_data[r].pop(0))
        r += step
        if r == rails - 1 or r == 0:
            step *= -1

    return ''.join(out)
