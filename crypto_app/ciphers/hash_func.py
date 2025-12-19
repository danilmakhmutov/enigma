from .rc5 import RC5

def hash(text):
    data = text.encode('utf-8')
    
    # Паддинг
    pad_len = 8 - (len(data) % 8)
    padded = bytearray(data)
    for i in range(pad_len):
        padded.append(0)
    
    rc5 = RC5()
    H = bytearray(8)  # нулевой хэш
    
    for i in range(0, len(padded), 8):
        block = padded[i:i+8]
        key = bytearray(16)
        key[:8] = H
        key[8:] = H
        
        encoded = rc5.encode_for_stream_cipher(bytes(block), bytes(key))
        
        new_H = bytearray(8)
        for j in range(8):
            new_H[j] = encoded[j] ^ block[j]
        
        H = new_H
    
    return ''.join(f'{b:02x}' for b in H)