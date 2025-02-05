import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import ttk
from analizer.word_analizer import WordAnalyzer
from entity.noun import Noun
from entity.verb import Verb
from entity.pronoun import Pronoun

# Сопоставление классов частей речи с их строковыми значениями
POS_TAGS = {
    'Noun': 'Noun',
    'Verb': 'Verb',
    'Adjective': 'Adjective',
    'Adverb': 'Adverb',
    'Pronoun': 'Pronoun',
    'Preposition': 'Preposition',
    'Conjunction': 'Conjunction',
    'Interjection': 'Interjection',
    'Determiner': 'Determiner',
    'Particle': 'Particle'
}

class TextAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Analyzer")
        self.root.geometry("800x600")

        self.analyzer = WordAnalyzer()  # Создаем объект анализатора

        # Кнопка для выбора файла
        self.btn_open = tk.Button(root, text="Select File", command=self.open_file)
        self.btn_open.pack(pady=10)

        # Настройка таблицы для вывода результатов
        self.tree = ttk.Treeview(root, columns=("Word", "Part of Speech", "Action"), show="headings", height=20)
        self.tree.heading("Word", text="Word")
        self.tree.heading("Part of Speech", text="Part of Speech")
        self.tree.heading("Action", text="Action")
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def open_file(self):
        """ Открывает диалог выбора файла, анализирует текст и выводит результат в таблицу """
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        if not file_path:
            return  # Если файл не выбран, ничего не делаем

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            analyzed_words = self.analyzer.analyze_text(text)  # Анализируем текст

            # Очищаем таблицу перед выводом новых данных
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Заполнение таблицы результатами анализа
            for word in analyzed_words:
                word_class = word.__class__.__name__
                pos = POS_TAGS.get(word_class, "Unknown")  # Получаем строковое представление части речи

                # Добавление кнопки для каждого слова
                button = ttk.Button(self.tree, text="Show Details", command=lambda w=word: self.show_word_details(w))

                self.tree.insert("", tk.END, values=(word.base, pos), tags=(word.base,))
                self.tree.set(self.tree.selection()[0], "Action", button)

        except Exception as e:
            messagebox.showerror("Error", f"Error reading the file: {e}")

    def show_word_details(self, word):
        """ Показывает подробности о слове в новом окне """
        word_class = word.__class__.__name__

        # Создаем окно для отображения деталей
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Details for {word.base}")
        details_window.geometry("300x300")

        # Заголовок с названием слова
        tk.Label(details_window, text=f"Details for '{word.base}'", font=("Helvetica", 14)).pack(pady=10)

        # Выводим формы слова в зависимости от его части речи
        if isinstance(word, Noun):
            # Пример использования: генерируем формы для существительного
            number = tk.StringVar(value="singular")
            case = tk.StringVar(value="nominative")

            # Параметры для генерации
            tk.Label(details_window, text="Number:").pack(pady=5)
            tk.Radiobutton(details_window, text="Singular", variable=number, value="singular").pack()
            tk.Radiobutton(details_window, text="Plural", variable=number, value="plural").pack()

            tk.Label(details_window, text="Case:").pack(pady=5)
            tk.Radiobutton(details_window, text="Nominative", variable=case, value="nominative").pack()
            tk.Radiobutton(details_window, text="Possessive", variable=case, value="possessive").pack()

            def generate_noun():
                word_form = word.generate_word_form({"number": number.get(), "case": case.get()})
                tk.Label(details_window, text=f"Generated Noun: {word_form}").pack(pady=10)

            tk.Button(details_window, text="Generate Noun", command=generate_noun).pack(pady=10)

        elif isinstance(word, Verb):
            # Пример для глагола
            verb_form = tk.StringVar(value="present_third_singular")
            tk.Label(details_window, text="Verb Form:").pack(pady=5)
            tk.Radiobutton(details_window, text="Present Third Singular", variable=verb_form, value="present_third_singular").pack()
            tk.Radiobutton(details_window, text="Gerund", variable=verb_form, value="gerund").pack()
            tk.Radiobutton(details_window, text="Past Participle", variable=verb_form, value="past_participle").pack()

            def generate_verb():
                word_form = word.generate_word_form({"verb_form": verb_form.get()})
                tk.Label(details_window, text=f"Generated Verb: {word_form}").pack(pady=10)

            tk.Button(details_window, text="Generate Verb", command=generate_verb).pack(pady=10)

        elif isinstance(word, Pronoun):
            # Пример для местоимений
            case = tk.StringVar(value="nominative")
            tk.Label(details_window, text="Case:").pack(pady=5)
            tk.Radiobutton(details_window, text="Nominative", variable=case, value="nominative").pack()
            tk.Radiobutton(details_window, text="Accusative", variable=case, value="accusative").pack()
            tk.Radiobutton(details_window, text="Genitive", variable=case, value="genitive").pack()

            def generate_pronoun():
                word_form = word.generate_word_form({"case": case.get()})
                tk.Label(details_window, text=f"Generated Pronoun: {word_form}").pack(pady=10)

            tk.Button(details_window, text="Generate Pronoun", command=generate_pronoun).pack(pady=10)

        else:
            # Для всех других типов слов, выводим базовую форму
            tk.Label(details_window, text=f"Word Form: {word.base}").pack(pady=10)


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = TextAnalyzerApp(root)
    root.mainloop()
