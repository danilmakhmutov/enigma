from .rc5 import RC5
import base64

class StreamCipherWithRC5:
    def __init__(self):
        self.rc5 = RC5()
    
    def _generate_keystream(self, length, key):
        stream = bytearray()
        counter = 0
        
        while len(stream) < length:
            ctr_block = counter.to_bytes(8, 'little')
            gamma_block = self.rc5.encode_for_stream_cipher(ctr_block, key)
            
            take = min(8, length - len(stream))
            stream.extend(gamma_block[:take])
            counter += 1
        
        return bytes(stream)
    
    def encode(self, text, key):
        if isinstance(text, str):
            text = text.encode('utf-8')
        
        if isinstance(key, str):
            key = key.encode('utf-8')[:16]
        
        gamma = self._generate_keystream(len(text), key)
        
        ct = bytearray(len(text))
        for i in range(len(text)):
            ct[i] = text[i] ^ gamma[i]
        
        return base64.b64encode(ct).decode('ascii')
    
    def decode(self, text, key):
        if isinstance(key, str):
            key = key.encode('utf-8')[:16]
        
        ct = base64.b64decode(text)
        gamma = self._generate_keystream(len(ct), key)
        
        pt = bytearray(len(ct))
        for i in range(len(ct)):
            pt[i] = ct[i] ^ gamma[i]
        
        return pt.decode('utf-8')