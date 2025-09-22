# app/crypto/playfair.py
# Playfair с поддержкой латиницы (5x5) и кириллицы (8x4, без "ё")
# Авто-детект алфавита по ключу/тексту.

import re
from typing import List, Tuple

LAT_ALPH = "abcdefghiklmnopqrstuvwxyz"  # j -> i
LAT_W, LAT_H = 5, 5
LAT_FILL = "x"

# Русский алфавит без "ё", 32 буквы. Сетка 8x4 (W=8, H=4)
RUS_ALPH = "абвгдежзийклмнопрстуфхцчшщъыьэюя".replace("ё", "")
RUS_W, RUS_H = 8, 4
RUS_FILL = "х"

def _only_letters(s: str) -> str:
    return "".join(ch for ch in s if ch.isalpha())

def _detect_is_russian(text: str, key: str) -> bool:
    t = _only_letters((text or "") + (key or "")).lower()
    return any("а" <= ch <= "я" or ch == "ё" for ch in t)

def _norm_lat(s: str) -> str:
    s = s.lower()
    s = s.replace("j", "i")
    return "".join(ch for ch in s if "a" <= ch <= "z")

def _norm_rus(s: str) -> str:
    s = s.lower()
    s = s.replace("ё", "е")
    return "".join(ch for ch in s if "а" <= ch <= "я")

def _build_table(key: str, is_rus: bool):
    if is_rus:
        alph = RUS_ALPH
        norm = _norm_rus
        W, H = RUS_W, RUS_H
    else:
        alph = LAT_ALPH
        norm = _norm_lat
        W, H = LAT_W, LAT_H

    seen = set()
    seq = []
    for ch in norm(key or "") + alph:
        if ch in alph and ch not in seen:
            seen.add(ch)
            seq.append(ch)

    # матрица и быстрые позиции
    tbl = [seq[i * W:(i + 1) * W] for i in range(H)]
    pos = {tbl[r][c]: (r, c) for r in range(H) for c in range(W)}
    return tbl, pos, W, H

def _prep_pairs(text: str, is_rus: bool) -> List[Tuple[str, str]]:
    if is_rus:
        norm = _norm_rus
        FILL = RUS_FILL
    else:
        norm = _norm_lat
        FILL = LAT_FILL

    t = norm(text or "")
    pairs = []
    i = 0
    while i < len(t):
        a = t[i]
        b = ""
        if i + 1 < len(t):
            b = t[i + 1]
        if b == "" or a == b:
            # вставляем разделитель
            pairs.append((a, FILL))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    if len(pairs) and pairs[-1][1] == "":
        pairs[-1] = (pairs[-1][0], FILL)
    # Если строка нечётной длины и не попали в условия выше
    if len(t) % 2 == 1 and (not pairs or pairs[-1][1] == ""):
        pairs.append((t[-1], FILL))
    return pairs

def _shift_rowcol(a_pos, b_pos, W, H, enc: bool):
    ra, ca = a_pos
    rb, cb = b_pos
    if ra == rb:                    # одна строка
        if enc:
            return (ra, (ca + 1) % W), (rb, (cb + 1) % W)
        else:
            return (ra, (ca - 1) % W), (rb, (cb - 1) % W)
    if ca == cb:                    # один столбец
        if enc:
            return ((ra + 1) % H, ca), ((rb + 1) % H, cb)
        else:
            return ((ra - 1) % H, ca), ((rb - 1) % H, cb)
    # прямоугольник
    return (ra, cb), (rb, ca)

def _process(text: str, key: str, enc: bool) -> str:
    is_rus = _detect_is_russian(text, key)
    tbl, pos, W, H = _build_table(key, is_rus)
    pairs = _prep_pairs(text, is_rus)
    out = []
    for a, b in pairs:
        # если после нормализации символа нет в алфавите — пропустим пару
        if a not in pos or b not in pos:
            continue
        a2pos, b2pos = _shift_rowcol(pos[a], pos[b], W, H, enc)
        ra, ca = a2pos; rb, cb = b2pos
        out.append(tbl[ra][ca] + tbl[rb][cb])
    return "".join(out)

def playfair_encrypt(text: str, key: str) -> str:
    return _process(text, key, enc=True)

def playfair_decrypt(text: str, key: str) -> str:
    return _process(text, key, enc=False)
