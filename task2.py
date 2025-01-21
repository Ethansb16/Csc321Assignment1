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
    print("Original text: \n" + raw_text)
    encryption = encrypt_cbc(raw_text.encode(), key, iv)
    return encryption

def verify(data):
    
    cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
    decrypted_text = cipher.decrypt(data)
    try:
        hr_text = decrypted_text.decode() 
        print("Decrypted Text:", hr_text)
        return ';admin=true;' in hr_text
    except UnicodeDecodeError:
        print("Decryption failed")
        return False

def flip_bit(ciphertext, position, bit_mask):
    ciphertext_mutable = bytearray(ciphertext)
    ciphertext_mutable[position] ^= bit_mask
    return bytes(ciphertext_mutable)


if __name__ == '__main__':
    try:         
        s_str = 'admin/True'
        encryption = submit(s_str)
        print(encryption)
        position_to_flip = AES.block_size + 11
        modified_encrypted_data = flip_bit(encryption, position_to_flip, 0x10)  # / -> =
        print(verify(encryption))
        #print("Original message:", msg)
        #print("Message length:", len(msg))
    

    except Exception as e:
        print(f"An error occurred: {e}")
    
