class SingleAlphabetReplacementCipher:
    def __init__(self, language="en"):
        if language == "en":
            self.frequency = {
                "e": 12.7, "t": 9.06, "a": 8.17, "o": 7.51, "i": 6.97,
                "n": 6.75, "s": 6.33, "h": 6.09, "r": 5.99, "d": 4.25,
                "l": 4.03, "c": 2.78, "u": 2.76, "m": 2.41, "w": 2.36,
                "f": 2.23, "g": 2.02, "y": 1.97, "p": 1.93, "b": 1.49,
                "v": 0.98, "k": 0.77, "x": 0.15, "j": 0.15, "q": 0.1, "z": 0.05
            }
        else:
            self.frequency = {
                "о": 10.97, "е": 8.45, "а": 8.01, "и": 7.35,
                "н": 6.7, "т": 6.26, "с": 5.47, "р": 4.73,
                "в": 4.54, "л": 4.4, "к": 3.49, "м": 3.21,
                "д": 2.98, "п": 2.81, "у": 2.62, "я": 2.01,
                "ы": 1.9, "ь": 1.74, "г": 1.7, "з": 1.65,
                "б": 1.59, "ч": 1.44, "й": 1.21, "х": 0.97,
                "ж": 0.94, "ш": 0.73, "ю": 0.64, "ц": 0.48,
                "щ": 0.36, "э": 0.32, "ф": 0.26, "ъ": 0.04, "ё": 0.04
            }

    def encode(self, text, key):
        text = text.lower()
        result = ""
        for symbol in text:
            if symbol in key:
                result += key[symbol]
            else:
                result += symbol
        return result

    def decode(self, text, key):
        text = text.lower()
        result = ""
        added_count = 0
        
        for i in range(len(text)):
            symbol = text[i]
            found = False
            for letter in key:
                if key[letter] == symbol:
                    result += letter
                    added_count += 1
                    found = True
                    break
            if not found:
                result += symbol
                added_count += 1
        return result

    def break_cipher(self, text):
        text = text.lower()
        key = {}
        calculated_frequency = {}
        symbols_count = 0

        for letter in text:
            if letter in self.frequency:
                calculated_frequency[letter] = calculated_frequency.get(letter, 0) + 1
                symbols_count += 1

        for letter in calculated_frequency:
            calculated_frequency[letter] = calculated_frequency[letter] * (100 / symbols_count)

        sorted_encoded = sorted(calculated_frequency.keys(), 
                              key=lambda x: calculated_frequency[x], reverse=True)
        all_letters = sorted(self.frequency.keys(), 
                           key=lambda x: self.frequency[x], reverse=True)

        for i in range(min(len(sorted_encoded), len(all_letters))):
            key[all_letters[i]] = sorted_encoded[i]

        return self.decode(text, key)