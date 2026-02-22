import tkinter as tk
from tkinter import messagebox, filedialog
import os

class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифровальщик текста")
        self.root.geometry("850x650")
        self.root.configure(bg='#f0f0f0')
        
        # Русский алфавит
        self.russian = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        
        # Заголовок
        title = tk.Label(self.root, text="ПРОГРАММА ШИФРОВАНИЯ ТЕКСТА", 
                        font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#333')
        title.pack(pady=10)
        
        # Рамка с алгоритмами
        algo_frame = tk.LabelFrame(self.root, text=" Выберите алгоритм шифрования ", 
                                  font=('Arial', 10, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        algo_frame.pack(fill='x', padx=10, pady=5)
        
        self.algo = tk.StringVar(value="eng")
        
        tk.Radiobutton(algo_frame, text="1. Столбцовый метод (улучшенный) - для английского текста", 
                      variable=self.algo, value="eng", bg='#f0f0f0', 
                      font=('Arial', 10), anchor='w').pack(fill='x', pady=2)
        
        tk.Radiobutton(algo_frame, text="2. Алгоритм Виженера (с самогенерирующимся ключом) - для русского текста", 
                      variable=self.algo, value="rus", bg='#f0f0f0',
                      font=('Arial', 10), anchor='w').pack(fill='x', pady=2)
        
        # Рамка с ключом
        key_frame = tk.LabelFrame(self.root, text=" Ключ шифрования ", 
                                 font=('Arial', 10, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        key_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(key_frame, text="Введите ключ:", bg='#f0f0f0', font=('Arial', 10)).pack(side='left')
        self.key_entry = tk.Entry(key_frame, width=50, font=('Arial', 10))
        self.key_entry.pack(side='left', padx=10)
        
        tk.Label(key_frame, text="(только буквы)", bg='#f0f0f0', font=('Arial', 9), fg='gray').pack(side='left')
        
        # Рамка с исходным текстом
        input_frame = tk.LabelFrame(self.root, text=" Исходный текст ", 
                                   font=('Arial', 10, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        input_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.input_text = tk.Text(input_frame, height=6, font=('Courier', 11))
        self.input_text.pack(fill='both', expand=True)
        
        # Кнопки действий
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.encrypt_btn = tk.Button(btn_frame, text="🔐 ЗАШИФРОВАТЬ", 
                                    bg='#4CAF50', fg='white',
                                    font=('Arial', 11, 'bold'), 
                                    width=20, height=2,
                                    command=self.encrypt)
        self.encrypt_btn.pack(side='left', padx=5)
        
        self.decrypt_btn = tk.Button(btn_frame, text="🔓 РАСШИФРОВАТЬ", 
                                    bg='#2196F3', fg='white',
                                    font=('Arial', 11, 'bold'), 
                                    width=20, height=2,
                                    command=self.decrypt)
        self.decrypt_btn.pack(side='left', padx=5)
        
        # Рамка с результатом
        output_frame = tk.LabelFrame(self.root, text=" Результат ", 
                                    font=('Arial', 10, 'bold'), bg='#f0f0f0', padx=10, pady=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.output_text = tk.Text(output_frame, height=6, font=('Courier', 11))
        self.output_text.pack(fill='both', expand=True)
        
        # Нижняя панель
        bottom_frame = tk.Frame(self.root, bg='#f0f0f0')
        bottom_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(bottom_frame, text="📂 Загрузить файл", 
                 command=self.load_file, bg='#e0e0e0',
                 font=('Arial', 10), width=15).pack(side='left', padx=2)
        
        tk.Button(bottom_frame, text="💾 Сохранить результат", 
                 command=self.save_file, bg='#e0e0e0',
                 font=('Arial', 10), width=15).pack(side='left', padx=2)
        
        tk.Button(bottom_frame, text="🗑 Очистить всё", 
                 command=self.clear, bg='#e0e0e0',
                 font=('Arial', 10), width=15).pack(side='left', padx=2)
        
        tk.Button(bottom_frame, text="ℹ О программе", 
                 command=self.show_about, bg='#e0e0e0',
                 font=('Arial', 10), width=15).pack(side='right', padx=2)
        
        # Статус
        self.status = tk.Label(self.root, text="✓ Готов к работе", 
                              bg='#f0f0f0', anchor='w', font=('Arial', 9))
        self.status.pack(fill='x', padx=10, pady=2)
    
    # ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
    def filter_eng(self, text):
        """Фильтрует только английские буквы A-Z"""
        return ''.join(c.upper() for c in text if c.isalpha() and 'A' <= c.upper() <= 'Z')
    
    def filter_rus(self, text):
        """Фильтрует только русские буквы А-Я и Ё"""
        result = []
        for c in text.upper():
            if c in self.russian:
                result.append(c)
        return ''.join(result)
    
    # ===== СТОЛБЦОВЫЙ МЕТОД (ИСПРАВЛЕННЫЙ) =====
    def column_encrypt(self, text, key):
        """Шифрование столбцовым методом"""
        # Фильтруем текст и ключ
        text = self.filter_eng(text)
        key = self.filter_eng(key)
        
        if not key:
            messagebox.showerror("Ошибка", "Ключ должен содержать английские буквы!")
            return ""
        if not text:
            messagebox.showerror("Ошибка", "Текст не содержит английских букв!")
            return ""
        
        cols = len(key)
        rows = (len(text) + cols - 1) // cols
        
        # Создаем таблицу и заполняем по строкам
        table = [['' for _ in range(cols)] for _ in range(rows)]
        for i, ch in enumerate(text):
            row = i // cols
            col = i % cols
            table[row][col] = ch
        
        # Сортируем столбцы по ключу с сохранением порядка для одинаковых букв
        key_with_index = [(key[i], i) for i in range(cols)]
        key_with_index.sort(key=lambda x: (x[0], x[1]))
        
        # Получаем порядок столбцов для чтения
        col_order = [idx for _, idx in key_with_index]
        
        # Читаем по столбцам в отсортированном порядке
        result = []
        for col in col_order:
            for row in range(rows):
                if table[row][col]:
                    result.append(table[row][col])
        
        return ''.join(result)
    
    def column_decrypt(self, text, key):
        """Дешифрование столбцовым методом"""
        # Фильтруем текст и ключ
        text = self.filter_eng(text)
        key = self.filter_eng(key)
        
        if not key:
            messagebox.showerror("Ошибка", "Ключ должен содержать английские буквы!")
            return ""
        if not text:
            messagebox.showerror("Ошибка", "Текст не содержит английских букв!")
            return ""
        
        cols = len(key)
        rows = (len(text) + cols - 1) // cols
        
        # Определяем размеры столбцов
        # Полных строк в таблице
        full_rows = len(text) // cols
        remainder = len(text) % cols
        
        # Размеры столбцов: первые remainder столбцов имеют размер full_rows + 1, остальные - full_rows
        col_sizes = [full_rows + 1 if i < remainder else full_rows for i in range(cols)]
        
        # Сортируем ключ для определения порядка столбцов
        key_with_index = [(key[i], i) for i in range(cols)]
        key_with_index.sort(key=lambda x: (x[0], x[1]))
        
        # Получаем исходные индексы столбцов в отсортированном порядке
        sorted_indices = [idx for _, idx in key_with_index]
        
        # Создаем таблицу для восстановления
        table = [['' for _ in range(cols)] for _ in range(rows)]
        
        # Заполняем таблицу по столбцам в соответствии с отсортированным порядком
        pos = 0
        for sorted_idx, original_col in enumerate(sorted_indices):
            # Определяем размер этого столбца
            col_size = col_sizes[original_col]
            
            # Заполняем столбец
            for row in range(col_size):
                if pos < len(text):
                    table[row][original_col] = text[pos]
                    pos += 1
        
        # Читаем по строкам для получения исходного текста
        result = []
        for row in range(rows):
            for col in range(cols):
                if table[row][col]:
                    result.append(table[row][col])
        
        return ''.join(result)
    
    # ===== АЛГОРИТМ ВИЖЕНЕРА =====
    def vigenere_encrypt(self, text, key):
        """Шифрование Виженером с самогенерирующимся ключом"""
        text = self.filter_rus(text)
        key = self.filter_rus(key)
        
        if not key:
            messagebox.showerror("Ошибка", "Ключ должен содержать русские буквы!")
            return ""
        if not text:
            messagebox.showerror("Ошибка", "Текст не содержит русских букв!")
            return ""
        
        # Генерируем ключ
        generated_key = key
        while len(generated_key) < len(text):
            # Добавляем букву из исходного текста
            next_char = text[len(generated_key) - len(key)]
            generated_key += next_char
        
        # Шифруем
        result = []
        for i, ch in enumerate(text):
            text_idx = self.russian.index(ch)
            key_idx = self.russian.index(generated_key[i])
            enc_idx = (text_idx + key_idx) % 33
            result.append(self.russian[enc_idx])
        
        return ''.join(result)
    
    def vigenere_decrypt(self, text, key):
        """Дешифрование Виженера с самогенерирующимся ключом"""
        text = self.filter_rus(text)
        key = self.filter_rus(key)
        
        if not key:
            messagebox.showerror("Ошибка", "Ключ должен содержать русские буквы!")
            return ""
        if not text:
            messagebox.showerror("Ошибка", "Текст не содержит русских букв!")
            return ""
        
        # Генерируем ключ
        generated_key = key
        decrypted = []
        
        for i, ch in enumerate(text):
            if i >= len(generated_key):
                # Добавляем расшифрованную букву
                generated_key += decrypted[i - len(key)]
            
            text_idx = self.russian.index(ch)
            key_idx = self.russian.index(generated_key[i])
            dec_idx = (text_idx - key_idx + 33) % 33
            decrypted.append(self.russian[dec_idx])
        
        return ''.join(decrypted)
    
    # ===== ОБРАБОТЧИКИ СОБЫТИЙ =====
    def encrypt(self):
        """Обработчик кнопки шифрования"""
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для шифрования!")
            return
        
        if not key:
            messagebox.showwarning("Предупреждение", "Введите ключ!")
            return
        
        result = ""
        if self.algo.get() == "eng":
            result = self.column_encrypt(text, key)
            if result:
                self.status.config(text="✓ Текст зашифрован (Столбцовый метод, английский)")
        else:
            result = self.vigenere_encrypt(text, key)
            if result:
                self.status.config(text="✓ Текст зашифрован (Виженер, русский)")
        
        if result:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
    
    def decrypt(self):
        """Обработчик кнопки дешифрования"""
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        
        if not text:
            messagebox.showwarning("Предупреждение", "Введите текст для дешифрования!")
            return
        
        if not key:
            messagebox.showwarning("Предупреждение", "Введите ключ!")
            return
        
        result = ""
        if self.algo.get() == "eng":
            result = self.column_decrypt(text, key)
            if result:
                self.status.config(text="✓ Текст расшифрован (Столбцовый метод, английский)")
        else:
            result = self.vigenere_decrypt(text, key)
            if result:
                self.status.config(text="✓ Текст расшифрован (Виженер, русский)")
        
        if result:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
    
    def load_file(self):
        """Загрузка текста из файла"""
        filename = filedialog.askopenfilename(
            title="Выберите текстовый файл",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)
                self.status.config(text=f"✓ Загружен файл: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
    
    def save_file(self):
        """Сохранение результата в файл"""
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Предупреждение", "Нет текста для сохранения!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status.config(text=f"✓ Сохранен файл: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
    
    def clear(self):
        """Очистка всех полей"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)
        self.key_entry.delete(0, tk.END)
        self.status.config(text="✓ Поля очищены")
    
    def show_about(self):
        """Информация о программе"""
        about = """ПРОГРАММА ШИФРОВАНИЯ ТЕКСТА

Реализованные алгоритмы:

1. СТОЛБЦОВЫЙ МЕТОД (УЛУЧШЕННЫЙ)
   • Для текста на английском языке
   • Сортировка столбцов по алфавиту ключа
   • Корректная обработка повторяющихся букв в ключе
   • Игнорируются все символы кроме A-Z

2. АЛГОРИТМ ВИЖЕНЕРА 
   (с самогенерирующимся ключом)
   • Для текста на русском языке
   • Ключ дополняется символами исходного текста
   • Поддерживается буква Ё
   • Игнорируются все символы кроме А-Я

Возможности:
   • Загрузка текста из файла
   • Сохранение результата в файл
   • Работа с текстом любого размера

Автор: Учебная программа
Версия: 3.1 для Windows (исправлена работа столбцового метода)"""
        
        messagebox.showinfo("О программе", about)

if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()