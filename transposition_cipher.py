def _generate_key_order(key: str) -> list[int]:
    """
    Повертає порядок індексів стовпців за ключем.
    Напр.: 'SECRET' -> масив (залежить від алф. порядку літер і врахування дублетів).
    """
    enumerated_key = [(ch, i) for i, ch in enumerate(key)]
    sorted_key = sorted(enumerated_key, key=lambda x: (x[0].upper(), x[1]))
    order = [orig_i for (ch, orig_i) in sorted_key]
    return order


def transposition_encrypt(plaintext: str, key: str) -> str:
    """
    Проста стовпчикова перестановка (Columnar Transposition).
    """
    col_count = len(key)
    order = _generate_key_order(key)

    rows = []
    for i in range(0, len(plaintext), col_count):
        rows.append(plaintext[i:i+col_count])

    ciphertext_parts = []
    for col_index in order:
        part = []
        for row in rows:
            if col_index < len(row):
                part.append(row[col_index])
        ciphertext_parts.append("".join(part))

    return "".join(ciphertext_parts)


def transposition_decrypt(ciphertext: str, key: str) -> str:
    """
    Дешифрування стовпчикової перестановки.
    """
    col_count = len(key)
    order = _generate_key_order(key)

    length = len(ciphertext)
    rows_count = (length + col_count - 1) // col_count

    col_sizes = [length // col_count] * col_count
    remainder = length % col_count
    for i in range(remainder):
        col_sizes[i] += 1

    col_texts = {}
    start_idx = 0
    for i, col_index in enumerate(order):
        size = col_sizes[col_index]
        col_texts[col_index] = ciphertext[start_idx:start_idx+size]
        start_idx += size

    rows = [[] for _ in range(rows_count)]
    for col_i in range(col_count):
        col_str = col_texts[col_i]
        for row_i in range(len(col_str)):
            rows[row_i].insert(col_i, col_str[row_i])

    plaintext = []
    for row in rows:
        plaintext.append("".join(row))

    return "".join(plaintext)


def double_transposition_encrypt(plaintext: str, key1: str, key2: str) -> str:
    """
    Подвійна перестановка: спочатку за key1, потім за key2.
    """
    step1 = transposition_encrypt(plaintext, key1)
    step2 = transposition_encrypt(step1, key2)
    return step2


def double_transposition_decrypt(ciphertext: str, key1: str, key2: str) -> str:
    """
    Дешифрування подвійної перестановки: у зворотному порядку ключів.
    """
    step1 = transposition_decrypt(ciphertext, key2)
    step2 = transposition_decrypt(step1, key1)
    return step2