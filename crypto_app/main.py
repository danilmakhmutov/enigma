import tkinter as tk
from tkinter import ttk, scrolledtext
import re
from ciphers import (
    SingleAlphabetReplacementCipher,
    GermanCipher,
    RC5,
    StreamCipherWithRC5,
    ElGamal,
    hash
)

def get_language(text):
    has_english = bool(re.search(r'[a-zA-Z]', text))
    has_russian = bool(re.search(r'[а-яА-ЯёЁ]', text))
    if has_english and not has_russian:
        return 'en'
    elif not has_english and has_russian:
        return 'rus'
    else:
        return None

def has_only_english(text):
    has_english = bool(re.search(r'[a-zA-Z]', text))
    has_russian = bool(re.search(r'[а-яА-ЯёЁ]', text))
    return has_english and not has_russian

def parse_key_sarc(key_text):
    obj_key = {}
    lines = key_text.replace('\n', '').replace(' ', '').split(',')
    for line in lines:
        if ':' in line:
            pair = line.split(':')
            if len(pair) == 2:
                obj_key[pair[0]] = pair[1]
    return obj_key

class CryptoApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторные по информационной безопасности")
        self.root.geometry("1400x800")
        self.root.configure(bg='black')
        self.current_frame = None
        self.frames = {}
        
        self.create_menu_buttons()
        self.create_all_frames()
        self.show_frame("SARC")

    def create_menu_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        buttons = [
            ("Шифр одноалфавитной замены", "SARC"),
            ("Немецкий шифр 1-й мировой", "germanCipher"),
            ("Стандарт RC5", "RC5"),
            ("Поточный шифр", "streamCipher"),
            ("Цифровая подпись Эль-Гамаля", "ElGamal"),
            ("Хэширование", "Hash")
        ]
        
        for text, frame_id in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                width=25,
                height=2,
                font=('Constantia', 11),
                command=lambda fid=frame_id: self.show_frame(fid)
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def create_all_frames(self):
        self.create_sarc_frame()
        self.create_german_frame()
        self.create_rc5_frame()
        self.create_stream_frame()
        self.create_elgamal_frame()
        self.create_hash_frame()
    
    def create_sarc_frame(self):
        # БЫСТРЫЕ НАСТРОЙКИ ЦВЕТОВ
        FRAME_BG = 'white'
        TEXT_BG = "#41831a"
        TEXT_FG = "#C21F1F"
        BUTTON_GREEN = '#4CAF50'
        BUTTON_BLUE = '#2196F3'
        TITLE_BG = '#2196F3'
        TITLE_FG = 'white'
        
        frame = tk.Frame(self.root, bg=FRAME_BG)
        frame = tk.Frame(self.root)
        self.frames["SARC"] = frame
        
        tk.Label(frame, text="Шифр одноалфавитной замены", font=('Constantia', 14, 'bold')).pack(pady=10)
        
        # Текст
        tk.Label(frame, text="Текст:").pack(anchor=tk.W, padx=20)
        self.text_sarc = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.text_sarc.pack(padx=20, pady=5)
        self.text_sarc.insert('1.0', "Шифр подстановки — это метод шифрования, в котором элементы исходного открытого текста заменяются зашифрованным текстом в соответствии с некоторым правилом.")
        
        # Ключ
        tk.Label(frame, text="Ключ (формат: буква:буква, ...):").pack(anchor=tk.W, padx=20)
        self.key_sarc = scrolledtext.ScrolledText(frame, width=100, height=4)
        self.key_sarc.pack(padx=20, pady=5)
        self.key_sarc.insert('1.0', "ё:ю,й:б,ц:ь,у:т,к:и,е:м,н:с,г:ч,ш:я,щ:э,з:ж,х:д,ъ:л,ф:о,ы:р,в:п,а:в,п:а,р:ы,о:ф,л:ъ,д:х,ж:з,э:щ,я:ш,ч:г,с:н,м:е,и:к,т:у,ь:ц,б:й,ю:ё")
        
        # Результат
        tk.Label(frame, text="Результат:").pack(anchor=tk.W, padx=20)
        self.result_sarc = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.result_sarc.pack(padx=20, pady=5)
        
        # Кнопки
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Зашифровать", width=15,
                 command=self.encode_sarc).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Расшифровать", width=15,
                 command=self.decode_sarc).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Взломать", width=15,
                 command=self.break_sarc).pack(side=tk.LEFT, padx=5)
    
    def encode_sarc(self):
        text = self.text_sarc.get('1.0', tk.END).strip()
        key_text = self.key_sarc.get('1.0', tk.END).strip()
        key = parse_key_sarc(key_text)
        
        language = get_language(text)
        if not language:
            self.text_sarc.delete('1.0', tk.END)
            self.text_sarc.insert('1.0', 'Используйте английский или русский алфавит!')
            return
        
        cipher = SingleAlphabetReplacementCipher(language)
        result = cipher.encode(text, key)
        self.result_sarc.delete('1.0', tk.END)
        self.result_sarc.insert('1.0', result)
    
    def decode_sarc(self):
        text = self.text_sarc.get('1.0', tk.END).strip()
        key_text = self.key_sarc.get('1.0', tk.END).strip()
        key = parse_key_sarc(key_text)
        
        language = get_language(text)
        if not language:
            self.text_sarc.delete('1.0', tk.END)
            self.text_sarc.insert('1.0', 'Используйте английский или русский алфавит!')
            return
        
        cipher = SingleAlphabetReplacementCipher(language)
        result = cipher.decode(text, key)
        self.result_sarc.delete('1.0', tk.END)
        self.result_sarc.insert('1.0', result)
    
    def break_sarc(self):
        text = self.text_sarc.get('1.0', tk.END).strip()
        language = get_language(text)
        if not language:
            self.text_sarc.delete('1.0', tk.END)
            self.text_sarc.insert('1.0', 'Используйте английский или русский алфавит!')
            return
        
        cipher = SingleAlphabetReplacementCipher(language)
        result = cipher.break_cipher(text)
        self.result_sarc.delete('1.0', tk.END)
        self.result_sarc.insert('1.0', result)
    
    def create_german_frame(self):
                # БЫСТРЫЕ НАСТРОЙКИ ЦВЕТОВ
        FRAME_BG = 'white'
        TEXT_BG = '#f9f9f9'
        TEXT_FG = '#333333'
        BUTTON_GREEN = '#4CAF50'
        BUTTON_BLUE = '#2196F3'
        TITLE_BG = '#2196F3'
        TITLE_FG = 'white'
        
        frame = tk.Frame(self.root, bg=FRAME_BG)
        frame = tk.Frame(self.root)
        self.frames["germanCipher"] = frame
        
        tk.Label(frame, text="Немецкий шифр 1-й мировой", font=('Constantia', 14, 'bold')).pack(pady=10)
        
        tk.Label(frame, text="Текст (ENG):").pack(anchor=tk.W, padx=20)
        self.text_german = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.text_german.pack(padx=20, pady=5)
        self.text_german.insert('1.0', "Watermelon its a good fruit. You eat, you drink, you wash your face.")
        
        tk.Label(frame, text="Ключевое слово (ENG):").pack(anchor=tk.W, padx=20)
        self.key_german = tk.Entry(frame, width=50)
        self.key_german.pack(padx=20, pady=5)
        self.key_german.insert(0, "secret")
        
        tk.Label(frame, text="Результат:").pack(anchor=tk.W, padx=20)
        self.result_german = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.result_german.pack(padx=20, pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Зашифровать", width=15,
                 command=self.encode_german).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Расшифровать", width=15,
                 command=self.decode_german).pack(side=tk.LEFT, padx=5)
    
    def encode_german(self):
        text = self.text_german.get('1.0', tk.END).strip()
        key = self.key_german.get().strip()
        
        if not has_only_english(text):
            self.text_german.delete('1.0', tk.END)
            self.text_german.insert('1.0', 'Используйте английский алфавит!')
            return
        
        cipher = GermanCipher()
        result = cipher.encode(text, key)
        self.result_german.delete('1.0', tk.END)
        self.result_german.insert('1.0', result)
    
    def decode_german(self):
        text = self.text_german.get('1.0', tk.END).strip()
        key = self.key_german.get().strip()
        
        if not has_only_english(text):
            self.text_german.delete('1.0', tk.END)
            self.text_german.insert('1.0', 'Используйте английский алфавит!')
            return
        
        cipher = GermanCipher()
        result = cipher.decode(text, key)
        self.result_german.delete('1.0', tk.END)
        self.result_german.insert('1.0', result)
    
    def create_rc5_frame(self):
                # БЫСТРЫЕ НАСТРОЙКИ ЦВЕТОВ
        FRAME_BG = 'white'
        TEXT_BG = '#f9f9f9'
        TEXT_FG = '#333333'
        BUTTON_GREEN = '#4CAF50'
        BUTTON_BLUE = '#2196F3'
        TITLE_BG = '#2196F3'
        TITLE_FG = 'white'
        
        frame = tk.Frame(self.root, bg=FRAME_BG)
        frame = tk.Frame(self.root)
        self.frames["RC5"] = frame
        
        tk.Label(frame, text="Стандарт RC5", font=('Constantia', 14, 'bold')).pack(pady=10)
        
        tk.Label(frame, text="Текст:").pack(anchor=tk.W, padx=20)
        self.text_rc5 = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.text_rc5.pack(padx=20, pady=5)
        self.text_rc5.insert('1.0', "Watermelon its a good fruit. You eat, you drink, you wash your face")
        
        tk.Label(frame, text="Ключ (автозаполнение):").pack(anchor=tk.W, padx=20)
        self.key_rc5 = tk.Entry(frame, width=50)
        self.key_rc5.pack(padx=20, pady=5)
        
        tk.Label(frame, text="Результат:").pack(anchor=tk.W, padx=20)
        self.result_rc5 = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.result_rc5.pack(padx=20, pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Зашифровать", width=15,
                 command=self.encode_rc5).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Расшифровать", width=15,
                 command=self.decode_rc5).pack(side=tk.LEFT, padx=5)
    
    def encode_rc5(self):
        text = self.text_rc5.get('1.0', tk.END).strip()
        cipher = RC5()
        key = cipher.random_key()
        self.key_rc5.delete(0, tk.END)
        self.key_rc5.insert(0, key)
        
        result = cipher.encode(text, key)
        self.result_rc5.delete('1.0', tk.END)
        self.result_rc5.insert('1.0', result)
    
    def decode_rc5(self):
        text = self.text_rc5.get('1.0', tk.END).strip()
        key = self.key_rc5.get().strip()
        
        cipher = RC5()
        result = cipher.decode(text, key)
        self.result_rc5.delete('1.0', tk.END)
        self.result_rc5.insert('1.0', result)
    
    def create_stream_frame(self):
                # БЫСТРЫЕ НАСТРОЙКИ ЦВЕТОВ
        FRAME_BG = 'white'
        TEXT_BG = '#f9f9f9'
        TEXT_FG = '#333333'
        BUTTON_GREEN = '#4CAF50'
        BUTTON_BLUE = '#2196F3'
        TITLE_BG = '#2196F3'
        TITLE_FG = 'white'
        
        frame = tk.Frame(self.root, bg=FRAME_BG)
        frame = tk.Frame(self.root)
        self.frames["streamCipher"] = frame
        
        tk.Label(frame, text="Поточный шифр", font=('Constantia', 14, 'bold')).pack(pady=10)
        
        tk.Label(frame, text="Текст:").pack(anchor=tk.W, padx=20)
        self.text_stream = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.text_stream.pack(padx=20, pady=5)
        self.text_stream.insert('1.0', "Watermelon its a good fruit. You eat, you drink, you wash your face")
        
        tk.Label(frame, text="Ключ (авто):").pack(anchor=tk.W, padx=20)
        self.key_stream = tk.Entry(frame, width=50)
        self.key_stream.pack(padx=20, pady=5)
        
        tk.Label(frame, text="Результат:").pack(anchor=tk.W, padx=20)
        self.result_stream = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.result_stream.pack(padx=20, pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Зашифровать", width=15,
                 command=self.encode_stream).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Расшифровать", width=15,
                 command=self.decode_stream).pack(side=tk.LEFT, padx=5)
    
    def encode_stream(self):
        text = self.text_stream.get('1.0', tk.END).strip()
        cipher = StreamCipherWithRC5()
        rc5 = RC5()
        key = rc5.random_key()
        self.key_stream.delete(0, tk.END)
        self.key_stream.insert(0, key)
        
        result = cipher.encode(text, key)
        self.result_stream.delete('1.0', tk.END)
        self.result_stream.insert('1.0', result)
    
    def decode_stream(self):
        text = self.text_stream.get('1.0', tk.END).strip()
        key = self.key_stream.get().strip()
        
        cipher = StreamCipherWithRC5()
        result = cipher.decode(text, key)
        self.result_stream.delete('1.0', tk.END)
        self.result_stream.insert('1.0', result)
    
    def create_elgamal_frame(self):    # БЫСТРЫЕ НАСТРОЙКИ ЦВЕТОВ
        FRAME_BG = 'white'
        TEXT_BG = '#f9f9f9'
        TEXT_FG = '#333333'
        BUTTON_GREEN = '#4CAF50'
        BUTTON_BLUE = '#2196F3'
        TITLE_BG = '#2196F3'
        TITLE_FG = 'white'
        
        frame = tk.Frame(self.root, bg=FRAME_BG)
        frame = tk.Frame(self.root)
        self.frames["ElGamal"] = frame
        
        tk.Label(frame, text="Цифровая подпись Эль-Гамаля", font=('Constantia', 14, 'bold')).pack(pady=10)
        
        tk.Label(frame, text="Текст:").pack(anchor=tk.W, padx=20)
        self.text_elgamal = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.text_elgamal.pack(padx=20, pady=5)
        self.text_elgamal.insert('1.0', "Watermelon its a good fruit. You eat, you drink, you wash your face")
        
        tk.Label(frame, text="Ключ открытый (авто):").pack(anchor=tk.W, padx=20)
        self.key_elgamal = tk.Entry(frame, width=50)
        self.key_elgamal.pack(padx=20, pady=5)
        
        tk.Label(frame, text="Результат:").pack(anchor=tk.W, padx=20)
        self.result_elgamal = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.result_elgamal.pack(padx=20, pady=5)
        
        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Зашифровать", width=15,
                 command=self.encode_elgamal).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Расшифровать", width=15,
                 command=self.decode_elgamal).pack(side=tk.LEFT, padx=5)
    
    def encode_elgamal(self):
        text = self.text_elgamal.get('1.0', tk.END).strip()
        cipher = ElGamal()
        keys = cipher.generate_keys()
        cipher.set_private_key(keys['privateKey'])
        cipher.set_public_key(keys['publicKey'])
        
        key_str = f"y = {keys['publicKey']['y']}, p = {keys['publicKey']['p']}, g = {keys['publicKey']['g']}"
        self.key_elgamal.delete(0, tk.END)
        self.key_elgamal.insert(0, key_str)
        
        result = cipher.encode_text(text)
        self.result_elgamal.delete('1.0', tk.END)
        self.result_elgamal.insert('1.0', result)
    
    def decode_elgamal(self):
        text = self.text_elgamal.get('1.0', tk.END).strip()
        cipher = ElGamal()
        
        result = cipher.decode_text(text)
        self.result_elgamal.delete('1.0', tk.END)
        self.result_elgamal.insert('1.0', result)
    
    def create_hash_frame(self):
                # БЫСТРЫЕ НАСТРОЙКИ ЦВЕТОВ
        FRAME_BG = 'white'
        TEXT_BG = '#f9f9f9'
        TEXT_FG = '#333333'
        BUTTON_GREEN = '#4CAF50'
        BUTTON_BLUE = '#2196F3'
        TITLE_BG = '#2196F3'
        TITLE_FG = 'white'
        
        frame = tk.Frame(self.root, bg=FRAME_BG)
        frame = tk.Frame(self.root)
        self.frames["Hash"] = frame
        
        tk.Label(frame, text="Хэширование", font=('Constantia', 14, 'bold')).pack(pady=10)
        
        tk.Label(frame, text="Текст:").pack(anchor=tk.W, padx=20)
        self.text_hash = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.text_hash.pack(padx=20, pady=5)
        self.text_hash.insert('1.0', "Watermelon its a good fruit. You eat, you drink, you wash your face")
        
        tk.Label(frame, text="Результат:").pack(anchor=tk.W, padx=20)
        self.result_hash = scrolledtext.ScrolledText(frame, width=100, height=8)
        self.result_hash.pack(padx=20, pady=5)
        
        tk.Button(frame, text="Захэшировать", width=15,
                 command=self.encode_hash).pack(pady=10)
    
    def encode_hash(self):
        text = self.text_hash.get('1.0', tk.END).strip()
        result = hash(text)
        self.result_hash.delete('1.0', tk.END)
        self.result_hash.insert('1.0', result)
    
    def show_frame(self, frame_id):
        if self.current_frame:
            self.current_frame.pack_forget()
        
        self.current_frame = self.frames[frame_id]
        self.current_frame.pack(fill=tk.BOTH, expand=True)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
    