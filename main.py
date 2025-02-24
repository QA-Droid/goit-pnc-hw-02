from vigenere_cipher import vigenere_encrypt, vigenere_decrypt
from friedman_test import friedman_test, guess_vigenere_key
from transposition_cipher import (
    transposition_encrypt,
    transposition_decrypt,
    double_transposition_encrypt,
    double_transposition_decrypt
)
from table_cipher import (
    table_encrypt,
    table_decrypt,
    double_table_encrypt,
    double_table_decrypt
)

def main():
    original_text = """The artist is the creator of beautiful things. To reveal art and conceal the artist 
is art's aim. The critic is he who can translate into another manner or a new material his impression 
of beautiful things. The highest, as the lowest, form of criticism is a mode of autobiography. Those 
who find ugly meanings in beautiful things are corrupt without being charming. This is a fault. Those 
who find beautiful meanings in beautiful things are the cultivated. For these there is hope. They are 
the elect to whom beautiful things mean only Beauty. There is no such thing as a moral or an immoral 
book. Books are well written, or badly written. That is all. The nineteenth-century dislike of realism 
is the rage of Caliban seeing his own face in a glass. The nineteenth-century dislike of Romanticism 
is the rage of Caliban not seeing his own face in a glass. The moral life of man forms part of the subject 
matter of the artist, but the morality of art consists in the perfect use of an imperfect medium. No artist 
desires to prove anything. Even things that are true can be proved. No artist has ethical sympathies. An 
ethical sympathy in an artist is an unpardonable mannerism of style. No artist is ever morbid. The artist 
can express everything. Thought and language are to the artist instruments of an art. Vice and virtue are 
to the artist materials for an art. From the point of view of form, the type of all the arts is the art 
of the musician. From the point of view of feeling, the actor's craft is the type. All art is at once 
surface and symbol. Those who go beneath the surface do so at their peril. Those who read the symbol do 
so at their peril. It is the spectator, and not life, that art really mirrors. Diversity of opinion about 
a work of art shows that the work is new, complex, vital. When critics disagree the artist is in accord 
with himself. We can forgive a man for making a useful thing as long as he does not admire it. The only 
excuse for making a useless thing is that one admires it intensely. All art is quite useless.
"""

    print("=======================================================")
    print("1) Шифр Віженера (Рівень 1: ключ = 'CRYPTOGRAPHY')")
    key_vigenere_known = "CRYPTOGRAPHY"
    encrypted_vig = vigenere_encrypt(original_text, key_vigenere_known)
    decrypted_vig = vigenere_decrypt(encrypted_vig, key_vigenere_known)

    print("  Зашифрований (фрагмент) :", encrypted_vig[:80], "...")
    print("  Дешифрований (фрагмент) :", decrypted_vig[:80], "...")
    print("  Співпадає з оригіналом?  :", decrypted_vig == original_text)

    print("\n2) Шифр Віженера (Рівень 2: невідомий ключ) => Тест Фрідмана + спроба частотного аналізу")

    approx_len = friedman_test(encrypted_vig)
    print(f"  Оцінка довжини ключа (Фрідман) ~ {approx_len:.2f}")

    guessed_key = guess_vigenere_key(encrypted_vig, max_key_len=20)
    print(f"  Припущення щодо ключа: {guessed_key}")

    decrypted_guess = vigenere_decrypt(encrypted_vig, guessed_key)
    print("  Перевірка: чи схожий результат на оригінал? :", decrypted_guess[:80], "...")
    match_percent = similarity(decrypted_guess, original_text)
    print(f"  Збіг з оригіналом: {match_percent*100:.1f}%")

    print("\n=======================================================")
    print("3) Шифр перестановки (Рівень 1: ключ-фраза 'SECRET')")
    key_transposition_simple = "SECRET"
    encrypted_transp = transposition_encrypt(original_text, key_transposition_simple)
    decrypted_transp = transposition_decrypt(encrypted_transp, key_transposition_simple)

    print("  Зашифрований (фрагмент) :", encrypted_transp[:80], "...")
    print("  Дешифрований (фрагмент) :", decrypted_transp[:80], "...")
    print("  Співпадає з оригіналом?  :", decrypted_transp == original_text)

    print("\n4) Шифр перестановки (Рівень 2: подвійна перестановка, ключі 'SECRET' та 'CRYPTO')")
    key1 = "SECRET"
    key2 = "CRYPTO"
    encrypted_double = double_transposition_encrypt(original_text, key1, key2)
    decrypted_double = double_transposition_decrypt(encrypted_double, key1, key2)

    print("  Зашифрований (фрагмент) :", encrypted_double[:80], "...")
    print("  Дешифрований (фрагмент) :", decrypted_double[:80], "...")
    print("  Співпадає з оригіналом?  :", decrypted_double == original_text)

    print("\n=======================================================")
    print("5) Табличний шифр (Рівень 1: фраза-ключ 'MATRIX')")
    key_table_simple = "MATRIX"
    encrypted_table = table_encrypt(original_text, key_table_simple)
    decrypted_table = table_decrypt(encrypted_table, key_table_simple)

    print("  Зашифрований (фрагмент) :", encrypted_table[:80], "...")
    print("  Дешифрований (фрагмент) :", decrypted_table[:80], "...")
    print("  Співпадає з оригіналом?  :", decrypted_table == original_text)

    print("\n6) Табличний шифр (Рівень 2: спочатку Віженер, потім табличний з ключем 'CRYPTO')")
    key_vigenere_L2 = "CRYPTO"
    key_table_L2 = "CRYPTO"
    encrypted_combo = double_table_encrypt(original_text, key_vigenere_L2, key_table_L2)
    decrypted_combo = double_table_decrypt(encrypted_combo, key_vigenere_L2, key_table_L2)

    print("  Зашифрований (фрагмент) :", encrypted_combo[:80], "...")
    print("  Дешифрований (фрагмент) :", decrypted_combo[:80], "...")
    print("  Співпадає з оригіналом?  :", decrypted_combo == original_text)


def similarity(str1: str, str2: str) -> float:
    """
    Дуже проста функція для оцінки відсотка збігів символів 
    між двома рядками однакової довжини.
    Використовуємо мінімальну довжину з обох.
    """
    length = min(len(str1), len(str2))
    if length == 0:
        return 0.0
    matches = sum(a == b for a, b in zip(str1[:length], str2[:length]))
    return matches / length


if __name__ == "__main__":
    main()