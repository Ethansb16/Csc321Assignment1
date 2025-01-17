from cbc import encrypt_cbc
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

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
    encryption = encrypt_cbc(raw_text.encode(), key, iv) # TODO replace with cbc_encryption instead
    return encryption

def verify(data):
    cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
    decryption_text = cipher.decrypt(data)
    hr_text = decryption_text.decode()
    print(hr_text)
    if ';admin=true;' in  hr_text:
        return True
    else:
        return False

if __name__ == '__main__':
    s_str = 'admin/True'
    encryption = submit(s_str)
    print(encryption)
    print(verify(encryption))
