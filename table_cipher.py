def _generate_row_order(key: str) -> list[int]:
    """
    Аналог _generate_key_order, але "по рядках":
    Сортуємо літери key і повертаємо порядок індексів (row).
    """
    enumerated_key = [(ch, i) for i, ch in enumerate(key)]
    sorted_key = sorted(enumerated_key, key=lambda x: (x[0].upper(), x[1]))
    order = [orig_i for (ch, orig_i) in sorted_key]
    return order


def table_encrypt(plaintext: str, key: str) -> str:
    """
    Приклад "табличного шифру":
    - Кількість рядків = довжина key
    - Заповнюємо таблицю ПО КОЛОНКАХ
    - Переставляємо рядки за алфавітним порядком символів key
    - Зчитуємо таблицю рядок за рядком => ciphertext
    """
    row_count = len(key)
    length = len(plaintext)
    col_count = (length + row_count - 1) // row_count
    
    table = [[""] * col_count for _ in range(row_count)]

    idx = 0
    for col in range(col_count):
        for row in range(row_count):
            if idx < length:
                table[row][col] = plaintext[idx]
                idx += 1

    order = _generate_row_order(key)
    new_table = [table[row_idx] for row_idx in order]

    ciphertext = "".join("".join(r) for r in new_table)
    return ciphertext


def table_decrypt(ciphertext: str, key: str) -> str:
    """
    Зворотний процес для "table_encrypt".
    - Кількість рядків = len(key)
    - col_count = ceil(len(ciphertext)/row_count)
    - Спершу відтворюємо "переставлену" таблицю (new_table)
    - Потім за зворотнім порядком відновлюємо оригінальні рядки
    - Зчитуємо їх поколоночно => plaintext
    """
    row_count = len(key)
    length = len(ciphertext)
    col_count = (length + row_count - 1) // row_count

    new_table = []
    idx = 0
    for _ in range(row_count):
        row_part = ciphertext[idx:idx+col_count]
        idx += col_count
        new_table.append(list(row_part))

    order = _generate_row_order(key)
    original_table = [[] for _ in range(row_count)]
    for i, row_idx in enumerate(order):
        original_table[row_idx] = new_table[i]

    plaintext_chars = []
    for col in range(col_count):
        for row in range(row_count):
            if col < len(original_table[row]):
                ch = original_table[row][col]
                if ch != "":
                    plaintext_chars.append(ch)

    return "".join(plaintext_chars) 


def double_table_encrypt(plaintext: str, key_vigenere: str, key_table: str) -> str:
    """
    Рівень 2 табличного шифру:
      - спочатку шифр Віженера (key_vigenere)
      - потім табличний шифр (key_table)
    """
    from vigenere_cipher import vigenere_encrypt
    step1 = vigenere_encrypt(plaintext, key_vigenere)
    step2 = table_encrypt(step1, key_table)
    return step2


def double_table_decrypt(ciphertext: str, key_vigenere: str, key_table: str) -> str:
    """
    Зворотний процес для double_table_encrypt
      - спочатку розшифрувати табличним шифром (key_table)
      - потім шифром Віженера (key_vigenere)
    """
    from vigenere_cipher import vigenere_decrypt
    step1 = table_decrypt(ciphertext, key_table)
    step2 = vigenere_decrypt(step1, key_vigenere)
    return step2