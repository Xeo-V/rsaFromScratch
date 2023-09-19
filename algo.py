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



def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=1024):
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

def funrandom gen 
def generate_keypair(p, q):
    try:
        n = p * q
        phi = (p - 1) * (q - 1)
        e = random.randrange(2, phi)
        g = gcd(e, phi)

        while g != 1:
            e = random.randrange(2, phi)
            g = gcd(e, phi)

        d = mod_inv(e, phi)
        if d is None:
            raise ValueError("Modular inverse does not exist.")
        return ((e, n), (d, n))
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def encrypt(public_key, plaintext):
    try:
        e, n = public_key
        cipher = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_char = {executor.submit(lambda p: (ord(p) ** e) % n, c): c for c in plaintext}
            for future in concurrent.futures.as_completed(future_to_char):
                cipher.append(future.result())
        return cipher
    except Exception as e:
        print(f"Error: {e}")
        return None

def decrypt(private_key, ciphertext):
    try:
        d, n = private_key
        plain = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_char = {executor.submit(lambda p: chr((p ** d) % n), c): c for c in ciphertext}
            for future in concurrent.futures.as_completed(future_to_char):
                plain.append(future.result())
        return ''.join(plain)
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    try:
        length = int(input("Enter bit length for p and q (e.g., 8, 16, 32): "))
        p = generate_prime_number(length)
        q = generate_prime_number(length)

        print(f"p = {p}, q = {q}")

        public, private = generate_keypair(p, q)

        if public and private:
            print(f"Public key: {public}")
            print(f"Private key: {private}")

            text = input("Enter text to encrypt: ")

            encrypted_msg = encrypt(public, text)
            print(f"Encrypted: {encrypted_msg}")

            decrypted_msg = decrypt(private, encrypted_msg)
            print(f"Decrypted: {decrypted_msg}")
    except Exception as e:
        print(f"Error: {e}")
