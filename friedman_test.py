import string
from vigenere_cipher import vigenere_decrypt

def index_of_coincidence(ciphertext: str) -> float:
    """
    Обчислює індекс збігів (IC) для заданого шифротексту.
    Повертає значення IC (дійсне число).
    """
    filtered = [ch.upper() for ch in ciphertext if ch.isalpha()]
    N = len(filtered)
    if N < 2:
        return 0.0

    freq = {}
    for ch in filtered:
        freq[ch] = freq.get(ch, 0) + 1

    numerator = sum(count * (count - 1) for count in freq.values())
    denominator = N * (N - 1)
    return numerator / denominator if denominator else 0.0


def friedman_test(ciphertext: str) -> float:
    """
    Виконує тест Фрідмана (Index of Coincidence) для оцінки довжини ключа (приблизно).
    """
    ic = index_of_coincidence(ciphertext)
    if ic <= 0 or (ic - 0.0385) == 0:
        return 1.0
    K_approx = 0.0279 / (ic - 0.0385) + 1
    return K_approx


def guess_vigenere_key(ciphertext: str, max_key_len=20) -> str:
    """
    Спрощений приклад пошуку ключа:
      1) За тестом Фрідмана отримуємо приблизну довжину.
      2) Перебираємо декілька варіантів довжин навколо оцінки.
      3) Для кожної довжини – частотний аналіз "колонок" і пошук найбільш ймовірного зсуву.
      4) Обираємо ключ, що дає найкращий "score".
    Повертає рядок (ймовірний ключ) У ВЕЛИКИХ ЛІТЕРАХ.
    """
    approx_len = int(round(friedman_test(ciphertext)))
    candidates = range(max(1, approx_len-2), min(max_key_len, approx_len+3))

    best_key = ""
    best_score = float('-inf')

    for length_candidate in candidates:
        columns = split_into_columns(ciphertext, length_candidate)

        shifts = [guess_shift_by_frequency(col) for col in columns]
        candidate_key = "".join(chr(s + ord('A')) for s in shifts)
        
        decrypted_candidate = vigenere_decrypt(ciphertext, candidate_key)
        score_val = compute_english_score(decrypted_candidate)

        if score_val > best_score:
            best_score = score_val
            best_key = candidate_key
    
    return best_key


def split_into_columns(ciphertext: str, key_length: int) -> list[str]:
    """
    Розбити шифртекст на key_length колонки: 
    col0 = символи з індексами 0, key_length, 2*key_length, ...
    col1 = символи з індексами 1, key_length+1, ...
    і т.д.
    (Ігноруємо символи, що не є літерами, або можете адаптувати під ваш варіант.)
    """
    filtered = [ch.upper() for ch in ciphertext if ch.isalpha()]
    columns = [[] for _ in range(key_length)]
    for i, ch in enumerate(filtered):
        columns[i % key_length].append(ch)
    return ["".join(col) for col in columns]


def guess_shift_by_frequency(column: str) -> int:
    """
    Підбирає зсув [0..25], який найбільше узгоджується з англійською частотною таблицею.
    """
    best_shift = 0
    best_score = float('inf')

    for shift in range(26):
        decrypted_col = apply_shift(column, -shift)
        diff = compare_with_english_freq(decrypted_col)
        if diff < best_score:
            best_score = diff
            best_shift = shift

    return best_shift


def apply_shift(text: str, shift: int) -> str:
    """
    Зсув літер A-Z на значення shift (додатній або від’ємний).
    """
    res = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            new_ord = (ord(ch) - ord('A') + shift) % 26 + ord('A')
            res.append(chr(new_ord))
        else:
            res.append(ch)
    return "".join(res)


def compare_with_english_freq(text: str) -> float:
    """
    Порівнює частоти символів у text з 
    типовими частотами англійської мови. Повертає "відстань", 
    де менше значення означає кращу відповідність.
    """
    english_freq = {
        'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
        'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
        'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
        'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
        'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
        'Z': 0.00074
    }
    length = len(text)
    if length == 0:
        return 9999.0

    freq = {ch: 0 for ch in english_freq.keys()}
    for ch in text:
        if ch in freq:
            freq[ch] += 1

    for ch in freq:
        freq[ch] = freq[ch] / length

    total_diff = 0.0
    for letter in english_freq:
        total_diff += abs(freq[letter] - english_freq[letter])

    return total_diff


def compute_english_score(decrypted_text: str) -> float:
    """
    Дуже проста метрика "англійськості":
    кількість пробілів + голосних + 
    (можна додавати детальніший аналіз).
    """
    vowels = set("AEIOUaeiou")
    spaces = decrypted_text.count(' ')
    vowels_count = sum(ch in vowels for ch in decrypted_text)
    score = spaces + 0.5 * vowels_count
    return score