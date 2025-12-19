import random

class ElGamal:
    def __init__(self):
        self.p = 257
        self.g = 3
        self.public_key = None
        self.private_key = None
    
    def _mod_pow(self, base, exp, mod):
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        return result
    
    def _mod_inverse(self, a, m):
        m0, x0, x1 = m, 0, 1
        if m == 1:
            return 0
        while a > 1:
            q = a // m
            m, a = a % m, m
            x0, x1 = x1 - q * x0, x0
        if x1 < 0:
            x1 += m0
        return x1
    
    def generate_keys(self):
        x = 102  # как в оригинале
        y = self._mod_pow(self.g, x, self.p)
        
        self.public_key = {'y': y, 'p': self.p, 'g': self.g}
        self.private_key = x
        
        return {
            'publicKey': {'y': str(y), 'p': str(self.p), 'g': str(self.g)},
            'privateKey': str(x)
        }
    
    def encode(self, M):
        m = int(M)
        if m < 0 or m >= self.p:
            raise ValueError(f"M={m} должно быть < {self.p-1}")
        
        y = self.public_key['y']
        p = self.p
        g = self.g
        k = 178  # как в оригинале
        
        a = self._mod_pow(g, k, p)
        b = (self._mod_pow(y, k, p) * m) % p
        
        return {'a': str(a), 'b': str(b)}
    
    def decode(self, ciphertext):
        a = int(ciphertext['a'])
        b = int(ciphertext['b'])
        x = self.private_key
        p = self.p
        
        a_x = self._mod_pow(a, x, p)
        inv = self._mod_inverse(a_x, p)
        M = (b * inv) % p
        
        return str(M)
    
    def set_public_key(self, key):
        self.public_key = {
            'y': int(key['y']),
            'p': int(key['p']),
            'g': int(key['g'])
        }
    
    def set_private_key(self, key):
        self.private_key = int(key)
    
    def encode_text(self, text):
        bytes_data = text.encode('utf-8')
        blocks = []
        for byte in bytes_data:
            cipher = self.encode(str(byte))
            blocks.append(f"{cipher['a']}:{cipher['b']}")
        return ';'.join(blocks)
    
    def decode_text(self, encoded_string):
        if not encoded_string:
            return ''
        
        blocks = encoded_string.split(';')
        bytes_list = []
        
        for block in blocks:
            if not block:
                continue
            a_str, b_str = block.split(':')
            M_str = self.decode({'a': a_str, 'b': b_str})
            bytes_list.append(int(M_str))
        
        return bytes(bytes_list).decode('utf-8')