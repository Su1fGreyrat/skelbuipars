# Ваш исходный кортеж
my_tuple = (2, 'Macbook', 'Компьютерия', 'Компьютеры', 'Vilnius')

# Предложение для проверки
sentence = "macbook icloud"

# Делим фразу и предложение на отдельные слова и преобразуем их к нижнему регистру
phrase_words = [word.lower() for word in my_tuple[1].split()]
sentence_words = [word.lower() for word in sentence.split()]

# Проверяем наличие нужных слов
if all(word in sentence_words for word in phrase_words):
    print("Все слова найдены в предложении.")
else:
    print("Не все слова найдены в предложении.")

