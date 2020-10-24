import typing as tp

def encrypt_caesar(plaintext: str, shift: int = 3) -> str:

    ciphertext = ""
    s = 'abcdefghijklmnopqrstuvwxyz'
    b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in plaintext:
        if i in s:
            if s.find(i) + shift > 25:
                l = s.find(i) + shift - 26
            else:
                l = s.find(i) + shift
            ciphertext += s[l]
        elif i in b:
            if b.find(i) + shift > 25:
                l = b.find(i) + shift - 26
            else:
                l = b.find(i) + shift
            ciphertext += b[l]
        else:
            ciphertext += i
    return ciphertext

def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:

    plaintext = ""
    s = 'abcdefghijklmnopqrstuvwxyz'
    b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in ciphertext:
        if i in s:
            if s.find(i) - shift < 0:
                l = 26 + s.find(i) - shift
            else:
                l = s.find(i) - shift
            plaintext += s[l]
        elif i in b:
            if b.find(i) - shift < 0:
                l = 26 + b.find(i) - shift
            else:
                l = b.find(i) - shift
            plaintext += b[l]
        else:
            plaintext += i
    return plaintext

def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:

    best_shift = 0
    return best_shift


