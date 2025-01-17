from ebc import ecb_encryption
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

key = get_random_bytes(AES.block_size)

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
    encryption = ecb_encryption(raw_text.encode(), key) # TODO replace with cbc_encryption instead
    return encryption

def verify(data):
    cipher = AES.new(key, mode=AES.MODE_CBC)
    decryption_text = cipher.decrypt(data)
    print(decryption_text)
    hr_text = decryption_text.decode()
    if ';admin=true;' in  hr_text:
        return True
    else:
        return False
    
