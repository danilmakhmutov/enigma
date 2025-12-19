class GermanCipher:
    def __init__(self):
        self.sequence = "adfgvx"
        self.all_symbols = "abcdefghijklmnopqrstuvwxyz1234567890"
        
        self.replacement_table = []
        for i in range(len(self.sequence)):
            start = len(self.sequence) * i
            arr = list(self.all_symbols[start:start + len(self.sequence)])
            self.replacement_table.append(arr)
        
        self.replacement = {}
        self.reverse_replacement = {}
        for i in range(len(self.replacement_table)):
            for j in range(len(self.replacement_table[0])):
                symbol = self.replacement_table[i][j]
                code = self.sequence[i] + self.sequence[j]
                self.replacement[symbol] = code
                self.reverse_replacement[code] = symbol

    def _sort_columns(self, matrix):
        column_data = []
        for j in range(len(matrix[0])):
            column = []
            for i in range(len(matrix)):
                column.append(matrix[i][j])
            column_data.append({
                'index': j,
                'first': matrix[0][j],
                'data': column
            })
        
        column_data.sort(key=lambda x: (x['first'], x['index']))
        
        new_matrix = []
        for i in range(len(matrix)):
            new_row = []
            for j in range(len(column_data)):
                new_row.append(column_data[j]['data'][i])
            new_matrix.append(new_row)
        return new_matrix

    def encode(self, text, key):
        text = text.lower()
        encoded_seq = ""
        
        for char in text:
            if char in self.replacement:
                encoded_seq += self.replacement[char]
        
        key_len = len(key)
        rows = (len(encoded_seq) + key_len - 1) // key_len
        
        matrix = [list(key)]
        for i in range(rows):
            start = i * key_len
            end = start + key_len
            row = list(encoded_seq[start:end])
            if len(row) < key_len:
                row.extend([''] * (key_len - len(row)))
            matrix.append(row)
        
        matrix = self._sort_columns(matrix)
        
        result = ""
        for j in range(key_len):
            for i in range(1, len(matrix)):
                if matrix[i][j]:
                    result += matrix[i][j]
        return result

    def decode(self, text, key):
        text = text.replace(" ", "").lower()
        
        if len(text) % 2 != 0:
            return "Некорректный формат"
        
        header = list(key)
        key_len = len(key)
        full_rows = len(text) // key_len
        rem = len(text) % key_len
        
        columns = []
        for i, letter in enumerate(header):
            length = full_rows + 1 if i < rem else full_rows
            columns.append({
                'letter': letter,
                'index': i,
                'length': length,
                'data': []
            })
        
        sorted_cols = sorted(columns, key=lambda x: (x['letter'], x['index']))
        
        pos = 0
        for col in sorted_cols:
            col['data'] = list(text[pos:pos + col['length']])
            pos += col['length']
        
        restored = [None] * key_len
        for col in sorted_cols:
            restored[col['index']] = col['data']
        
        rows_count = full_rows + (1 if rem > 0 else 0)
        encoded_seq = ""
        for i in range(rows_count):
            for col in range(key_len):
                if i < len(restored[col]):
                    encoded_seq += restored[col][i]
        
        result = ""
        for i in range(0, len(encoded_seq), 2):
            pair = encoded_seq[i:i+2]
            if pair in self.reverse_replacement:
                result += self.reverse_replacement[pair]
        
        return result