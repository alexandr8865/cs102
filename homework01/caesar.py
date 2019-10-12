def encrypt_caesar(plaintext: str) -> str:
    """
        >>> encrypt_caesar("PYTHON")
        'SBWKRQ'
        >>> encrypt_caesar("python")
        'sbwkrq'
        >>> encrypt_caesar("Python3.6")
        'Sbwkrq3.6'
        >>> encrypt_caesar("")
        ''
        """
    for i in plaintext:
        x = ord(i)
        if (x > 64 and x < 123):
            if (x > 87 and x < 91) or (x < 123 and x > 119):
                x = x - 26
            y = chr(x + 3)
            plaintext = plaintext.replace(i, y)
    return plaintext


def decrypt_caesar(ciphertext: str) -> str:
    """
       >>> decrypt_caesar("SBWKRQ")
       'PYTHON'
       >>> decrypt_caesar("sbwkrq")
       'python'
       >>> decrypt_caesar("Sbwkrq3.6")
       'Python3.6'
       >>> decrypt_caesar("")
       ''
       """
    for i in ciphertext:
        x = ord(i)
        if (x > 64 and x < 123):
            if (x < 68 and x < 91) or (x < 100 and x > 96):
                x = x + 26
            y = chr(x - 3)
            ciphertext = ciphertext.replace(i, y)
    return ciphertext
