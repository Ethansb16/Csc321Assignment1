import Crypto.Cipher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(AES.block_size)

def encryption(filename: str, key: int):
    with open(filename, 'rb') as f:
        content = f.read()
    print(key, AES.block_size)
    
    plaintext = content[54:]
    headers = content[:54]
    print(type(plaintext[0]))
    print(f'{headers[0]}\n\n\n\n\n{plaintext[0]}')

    ciphertext = ecb_encryption(plaintext=plaintext, key=key)
    ciphertext = b''.join(ciphertext)
    data = headers + ciphertext

    with open(f"{filename}_enc.bmp", "wb") as f:
        f.write(data)
    return True

def ecb_encryption(plaintext, key):
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    padded_text = pkcs7(plaintext)
    blocks = [padded_text[idx:idx+AES.block_size] for idx in range(0, len(padded_text), 16)]

    ciphered_text = [
        cipher.encrypt(bytes([block[i] ^ key[i] for i in range(AES.block_size)]))
        for block in blocks]
    return ciphered_text

def pkcs7(unpadded):
    padding = AES.block_size- len(unpadded)% AES.block_size
    return unpadded + bytes([padding] * padding)


if __name__ == '__main__':
    encryption('images/mustang.bmp', key)

