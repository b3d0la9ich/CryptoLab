# app/crypto/vigenere.py
# -*- coding: utf-8 -*-

from typing import Tuple

# Алфавиты (включая ё/Ё)
RU_LOW = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RU_UP  = RU_LOW.upper()
EN_LOW = "abcdefghijklmnopqrstuvwxyz"
EN_UP  = EN_LOW.upper()

def _alpha_sets(ch: str) -> Tuple[str, str] | None:
    """Возвращает (нижний, верхний) алфавит под символ (RU/EN), иначе None."""
    if ch in RU_LOW or ch in RU_UP:
        return RU_LOW, RU_UP
    if ch in EN_LOW or ch in EN_UP:
        return EN_LOW, EN_UP
    return None

def _shift_for_key_char(kch: str, alpha_low: str, alpha_up: str) -> int:
    """Сдвиг по символу ключа в алфавите соответствующего языка/регистра."""
    if kch in alpha_low:
        return alpha_low.index(kch)
    if kch in alpha_up:
        return alpha_up.index(kch)
    # если буква ключа другого языка — пробуем по её собственному алфавиту
    sets = _alpha_sets(kch)
    if sets:
        low, up = sets
        if kch in low: return low.index(kch)
        if kch in up:  return up.index(kch)
    # не буква — сдвиг 0
    return 0

def vigenere(text: str, key: str, encrypt: bool = True) -> str:
    """
    Виженер для RU/EN (с ё/Ё), сохраняет регистр.
    Небуквенные символы не изменяются И не двигают позицию по ключу.
    """
    if not key:
        return text

    out = []
    k = [c for c in key if _alpha_sets(c)]  # берём из ключа только буквы RU/EN
    if not k:
        return text

    ki = 0  # индекс по ключу
    for ch in text:
        sets = _alpha_sets(ch)
        if not sets:
            # цифры/пробелы/пунктуация — как есть, ключ не продвигаем
            out.append(ch)
            continue

        alpha_low, alpha_up = sets
        # текущий сдвиг по букве ключа
        kch = k[ki % len(k)]
        shift = _shift_for_key_char(kch, alpha_low, alpha_up)

        if ch in alpha_low:
            idx = alpha_low.index(ch)
            if encrypt:
                out.append(alpha_low[(idx + shift) % len(alpha_low)])
            else:
                out.append(alpha_low[(idx - shift) % len(alpha_low)])
            ki += 1
        elif ch in alpha_up:
            idx = alpha_up.index(ch)
            if encrypt:
                out.append(alpha_up[(idx + shift) % len(alpha_up)])
            else:
                out.append(alpha_up[(idx - shift) % len(alpha_up)])
            ki += 1
        else:
            out.append(ch)  # на всякий
    return ''.join(out)
