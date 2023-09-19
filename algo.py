import random
import concurrent.futures

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inv(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=1024):
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(2, phi)
        g = gcd(e, phi)
    d = mod_inv(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_char = [executor.submit(lambda p: (ord(p) ** e) % n, c) for c in plaintext]
    cipher = [future.result() for future in future_to_char]
    return cipher

def decrypt(private_key, ciphertext):
    d, n = private_key
    plain = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_char = [executor.submit(lambda p: chr((p ** d) % n), c) for c in ciphertext]
    plain = [future.result() for future in future_to_char]
    return ''.join(plain)

if __name__ == '__main__':
    length = int(input("Enter bit length for p and q (e.g., 8, 16, 32): "))
    p = generate_prime_number(length)
    q = generate_prime_number(length)

    print(f"p = {p}, q = {q}")

    public, private = generate_keypair(p, q)

    print(f"Public key: {public}")
    print(f"Private key: {private}")

    text = input("Enter text to encrypt: ")

    encrypted_msg = encrypt(public, text)
    print(f"Encrypted (as list of integers): {encrypted_msg}")

    decrypted_msg = decrypt(private, encrypted_msg)
    print(f"Decrypted: {decrypted_msg}")
