import random
import base64

class RC5:
    def __init__(self):
        self.r = 12
        self.w = 32
        self.b = 16
        self.u = self.w // 8
        self.t = 2 * (self.r + 1)
        self.P32 = 0xB7E15163
        self.Q32 = 0x9E3779B9

    def _left_rotate(self, x, y):
        y %= 32
        return ((x << y) | (x >> (32 - y))) & 0xFFFFFFFF

    def _right_rotate(self, x, y):
        y %= 32
        return ((x >> y) | (x << (32 - y))) & 0xFFFFFFFF

    def _expand_key(self, key):
        import struct
        L = [0] * ((self.b + self.u - 1) // self.u)
        
        for i in range(self.b):
            if isinstance(key, str):
                byte_val = ord(key[i]) if i < len(key) else 0
            else:
                byte_val = key[i] if i < len(key) else 0
            idx = i // self.u
            shift = 8 * (i % self.u)
            L[idx] = (L[idx] | (byte_val << shift)) & 0xFFFFFFFF
        
        S = [0] * self.t
        S[0] = self.P32
        for i in range(1, self.t):
            S[i] = (S[i-1] + self.Q32) & 0xFFFFFFFF
        
        i = j = 0
        A = B = 0
        v = 3 * max(self.t, len(L))
        
        for _ in range(v):
            A = S[i] = self._left_rotate((S[i] + A + B) & 0xFFFFFFFF, 3)
            B = L[j] = self._left_rotate((L[j] + A + B) & 0xFFFFFFFF, (A + B) & 31)
            i = (i + 1) % self.t
            j = (j + 1) % len(L)
        
        return S

    def _encode_block(self, A, B, S):
        A = (A + S[0]) & 0xFFFFFFFF
        B = (B + S[1]) & 0xFFFFFFFF
        
        for i in range(1, self.r + 1):
            A = (self._left_rotate(A ^ B, B & 31) + S[2*i]) & 0xFFFFFFFF
            B = (self._left_rotate(B ^ A, A & 31) + S[2*i + 1]) & 0xFFFFFFFF
        
        return A, B

    def _decode_block(self, A, B, S):
        for i in range(self.r, 0, -1):
            B = self._right_rotate((B - S[2*i + 1]) & 0xFFFFFFFF, A & 31) ^ A
            A = self._right_rotate((A - S[2*i]) & 0xFFFFFFFF, B & 31) ^ B
        
        B = (B - S[1]) & 0xFFFFFFFF
        A = (A - S[0]) & 0xFFFFFFFF
        
        return A, B

    def _pad(self, data):
        pad_len = 8 - (len(data) % 8)
        padded = bytearray(data)
        for _ in range(pad_len):
            padded.append(pad_len)
        return bytes(padded)

    def _unpad(self, data):
        if len(data) == 0:
            return data
        pad_len = data[-1]
        if pad_len < 1 or pad_len > 8:
            raise ValueError("Bad padding")
        return data[:-pad_len]

    def random_key(self):
        return ''.join(chr(random.randint(0, 255)) for _ in range(16))

    def encode_for_stream_cipher(self, text, key):
        import struct
        if len(text) != 8:
            raise ValueError("Need 8 bytes")
        
        if isinstance(text, str):
            text = text.encode('latin-1')
        
        A = struct.unpack('<I', text[:4])[0]
        B = struct.unpack('<I', text[4:8])[0]
        
        S = self._expand_key(key)
        A, B = self._encode_block(A, B, S)
        
        result = bytearray(8)
        result[:4] = struct.pack('<I', A)
        result[4:8] = struct.pack('<I', B)
        return bytes(result)

    def encode(self, text, key):
        if isinstance(text, str):
            text = text.encode('utf-8')
        
        if isinstance(key, str):
            key = key.encode('utf-8')[:self.b]
        
        padded = self._pad(text)
        S = self._expand_key(key)
        
        result = bytearray()
        for i in range(0, len(padded), 8):
            block = padded[i:i+8]
            A = int.from_bytes(block[:4], 'little')
            B = int.from_bytes(block[4:8], 'little')
            
            A, B = self._encode_block(A, B, S)
            
            result.extend(A.to_bytes(4, 'little'))
            result.extend(B.to_bytes(4, 'little'))
        
        return base64.b64encode(result).decode('ascii')

    def decode(self, ciphertext, key):
        if isinstance(key, str):
            key = key.encode('utf-8')[:self.b]
        
        data = base64.b64decode(ciphertext)
        if len(data) % 8 != 0:
            raise ValueError("Invalid ciphertext length")
        
        S = self._expand_key(key)
        
        result = bytearray()
        for i in range(0, len(data), 8):
            A = int.from_bytes(data[i:i+4], 'little')
            B = int.from_bytes(data[i+4:i+8], 'little')
            
            A, B = self._decode_block(A, B, S)
            
            result.extend(A.to_bytes(4, 'little'))
            result.extend(B.to_bytes(4, 'little'))
        
        unpadded = self._unpad(result)
        return unpadded.decode('utf-8')