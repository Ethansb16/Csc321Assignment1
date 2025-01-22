from cbc import encrypt_cbc
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = get_random_bytes(AES.block_size)
iv = get_random_bytes(16)  

def submit(userdata: str):
    url_list = []
    for c in userdata:
        if c ==';':
            url_list.append('%3B')
        elif c == '=':
            url_list.append('%3D')
        else:
            url_list.append(c)
    url_encoded = ''.join(url_list)
    raw_text = "userid=456;userdata=" + url_encoded + ";session-id=31337"
    byte_text = raw_text.encode()
    print('Original message:', byte_text)
    print('Original length:', len(byte_text))
    encryption = encrypt_cbc(byte_text, key, iv)
    print('Encrypted message:', encryption)
    print('Encrypted length:', len(encryption))
    return encryption

def verify(data):
    cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
    print('Recieved cipher:  ', data)
    decryption_text = cipher.decrypt(data)
    decryption_text = unpad(decryption_text, AES.block_size)
    print('Decrypted text:', decryption_text)
    if b'admin=true' in  decryption_text:
        return True
    else:
        return False

if __name__ == '__main__':
    xor = ord('/') ^ ord('=')
    s_str = 'admin/true'
    encryption = submit(s_str)
    encryption = bytearray(encryption)
    slash_i = 25
    block_num =  slash_i // 16
    block_i = slash_i % 16
    position = (block_num-1)*16 + block_i
    encryption[position] ^= xor

    print(verify(bytes(encryption)))
