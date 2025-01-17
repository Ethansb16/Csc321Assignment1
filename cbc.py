from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)  
iv = get_random_bytes(16)  


def encrypt_cbc(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pkcs7(plaintext)
    
    return cipher.encrypt(padded_text)

def encryption(filename: str, key: int):
    with open(filename, 'rb') as f:
        content = f.read()
    print(key, AES.block_size)
    
    plaintext = content[54:]
    headers = content[:54]
    print(type(plaintext[0]))
    print(f'{headers[0]}\n\n\n\n\n{plaintext[0]}')

    ciphertext = encrypt_cbc(plaintext=plaintext, key=key, iv=iv)
    ciphertext = bytes(ciphertext)
    data = headers + ciphertext

    with open(f"{filename}_cbc.bmp", "wb") as f:
        f.write(data)
    return True

def pkcs7(unpadded):
    padding = AES.block_size- len(unpadded)% AES.block_size
    return unpadded + bytes([padding] * padding)

if __name__ == '__main__':
    encryption('images/mustang.bmp', key)
