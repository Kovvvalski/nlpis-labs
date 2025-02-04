import spacy
from transformers import pipeline

# Загружаем модель для английского языка из spaCy
nlp = spacy.load("en_core_web_sm")

# Используем HuggingFace для генерации текстов с помощью предобученной модели GPT-2
generator = pipeline('text-generation', model='gpt2')

def generate_all_word_forms(base_word):
    # Применяем nlp-пайплайн к слову
    doc = nlp(base_word)

    # Список для хранения всех возможных словоформ
    all_forms = []

    for token in doc:
        lemma = token.lemma_
        pos = token.pos_

        # Генерация словоформ для существительных
        if pos == "NOUN":
            plural_form = lemma + "s"
            possessive_form = lemma + "'s"

            all_forms.append({
                "form": lemma,
                "number": "singular",
                "case": "nominative",
                "description": "Base form (singular, nominative)"
            })
            all_forms.append({
                "form": plural_form,
                "number": "plural",
                "case": "nominative",
                "description": "Plural form (nominative)"
            })
            all_forms.append({
                "form": possessive_form,
                "number": "singular",
                "case": "possessive",
                "description": "Possessive form (singular)"
            })
            all_forms.append({
                "form": plural_form + "'s",
                "number": "plural",
                "case": "possessive",
                "description": "Possessive form (plural)"
            })

        # Генерация словоформ для глаголов
        elif pos == "VERB":
            if lemma == "go":
                all_forms.append({
                    "form": "went",
                    "tense": "past",
                    "description": "Past tense (irregular)"
                })
                all_forms.append({
                    "form": "gone",
                    "tense": "past participle",
                    "description": "Past participle (irregular)"
                })
            else:
                # Для регулярных глаголов добавляем "ed"
                all_forms.append({
                    "form": lemma,
                    "tense": "present",
                    "description": "Present tense"
                })
                all_forms.append({
                    "form": lemma + "ed",
                    "tense": "past",
                    "description": "Past tense (regular)"
                })

            # Использование модели GPT-2 для генерации форм
            prompt = f"Generate forms for the verb '{lemma}': "
            generated_text = generator(prompt, max_length=50, num_return_sequences=1)[0]['generated_text']
            all_forms.append({
                "form": generated_text,
                "tense": "generated (using GPT-2)",
                "description": "Generated using GPT-2 model"
            })

        # Для прилагательных
        elif pos == "ADJ":
            all_forms.append({
                "form": lemma,
                "degree": "positive",
                "description": "Positive degree"
            })
            all_forms.append({
                "form": lemma + "er",
                "degree": "comparative",
                "description": "Comparative degree"
            })
            all_forms.append({
                "form": lemma + "est",
                "degree": "superlative",
                "description": "Superlative degree"
            })

    return all_forms


def print_word_forms(base_word):
    word_forms = generate_all_word_forms(base_word)
    if not word_forms:
        print(f"No forms found for the word '{base_word}'")
        return

    print(f"Word forms for '{base_word}':\n")
    for form in word_forms:
        print(f"Form: {form['form']}")
        print(f"Description: {form['description']}")
        if 'number' in form:
            print(f"Number: {form['number']}")
        if 'case' in form:
            print(f"Case: {form['case']}")
        if 'tense' in form:
            print(f"Tense: {form['tense']}")
        if 'degree' in form:
            print(f"Degree: {form['degree']}")
        print("-" * 30)


# Пример: Генерация и вывод всех форм для неправильного глагола "go"
print_word_forms("go")

# Пример: Генерация и вывод всех форм для регулярного глагола "work"
print_word_forms("work")
