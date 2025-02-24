def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Шифрує текст plaintext за допомогою шифру Віженера, використовуючи ключ key.
    Повертає зашифрований рядок.
    """
    ciphertext = []
    key_index = 0
    key = key.upper()

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                original_pos = ord(char) - ord('A')
                new_pos = (original_pos + shift) % 26
                new_char = chr(new_pos + ord('A'))
                ciphertext.append(new_char)
            else:
                original_pos = ord(char) - ord('a')
                new_pos = (original_pos + shift) % 26
                new_char = chr(new_pos + ord('a'))
                ciphertext.append(new_char)

            key_index += 1
        else:
            ciphertext.append(char)

    return "".join(ciphertext)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Дешифрує текст ciphertext, зашифрований шифром Віженера з ключем key.
    Повертає розшифрований рядок.
    """
    plaintext = []
    key_index = 0
    key = key.upper()

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                original_pos = ord(char) - ord('A')
                new_pos = (original_pos - shift) % 26
                new_char = chr(new_pos + ord('A'))
                plaintext.append(new_char)
            else:
                original_pos = ord(char) - ord('a')
                new_pos = (original_pos - shift) % 26
                new_char = chr(new_pos + ord('a'))
                plaintext.append(new_char)

            key_index += 1
        else:
            plaintext.append(char)

    return "".join(plaintext)