import typing as tp
def encrypt_vigenere(plaintext: str, keyword: str) -> str:

    ciphertext = ""
    s = 'abcdefghijklmnopqrstuvwxyz'
    b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while len(plaintext) > len(keyword): keyword += keyword
    k=0
    for i in plaintext:
        if i in s:
            shift = s.find(keyword[k])
            if s.find(i) + shift > 25:
                l = s.find(i) + shift - 26
            else:
                l = s.find(i) + shift
            ciphertext += s[l]
        elif i in b:
            shift = b.find(keyword[k])
            if b.find(i) + shift > 25:
                l = b.find(i) + shift - 26
            else:
                l = b.find(i) + shift
            ciphertext += b[l]
        else:
            ciphertext += i
        k+=1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:

    plaintext = ""
    s = 'abcdefghijklmnopqrstuvwxyz'
    b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while len(ciphertext) > len(keyword): keyword += keyword
    k=0
    for i in ciphertext:
        if i in s:
            shift = s.find(keyword[k])
            if s.find(i) - shift < 0:
                l = 26 + s.find(i) - shift
            else:
                l = s.find(i) - shift
            plaintext += s[l]
        elif i in b:
            shift = b.find(keyword[k])
            if b.find(i) - shift < 0:
                l = 26 + b.find(i) - shift
            else:
                l = b.find(i) - shift
            plaintext += b[l]
        else:
            plaintext += i
        k+=1
    return plaintext
