import telebot
import re
import string
import random

TOKEN = '8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4'
bot = telebot.TeleBot(TOKEN)

# ------------------- Часть 1: Логика обработки текста ------------------- #
def process_text(text):
    punctuation_chars = set(string.punctuation)
    has_punctuation = any(char in punctuation_chars for char in text)
    has_spaces = ' ' in text

    if not has_punctuation and not has_spaces:
        result = text[0::3]
        return result.lower()
    elif not has_punctuation and has_spaces:
        words = text.split()
        capitalized_words = [word.capitalize() for word in words]
        return ' '.join(capitalized_words)
    else:
        half_length = len(text) // 2
        return text[:half_length].upper()

# ------------------  Часть 2: Морской бой (10x10) ------------------- #
# Пример: создание поля для игры
def create_battlefield():
    return [['~' for _ in range(10)] for _ in range(10)]  # '~' - вода

# Глобальная переменная для поля (примитивное хранение)
battlefield = create_battlefield()

# ------------------  Часть 3: Игра "Виселица" ------------------- #
# Простая логика виселицы
hangman_words = ['компьютер', 'программа', 'телефон', 'машина', 'книга']
current_word = ''
display_word = ''
wrong_guesses = set()
max_attempts = 6

def start_hangman():
    global current_word, display_word, wrong_guesses
    current_word = random.choice(hangman_words)
    display_word = '_' * len(current_word)
    wrong_guesses = set()

# Обработка команды /start — запуск бота
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name or message.from_user.username
    greeting = f"Привет, {user_name}!"
    bot.send_message(message.chat.id, greeting)

# Обработка команды /rules
@bot.message_handler(commands=['rules'])
def handle_rules(message):
    rules_text = """📜 *Правила общения:*

1. Админа надо ########
2. Говоришь - мут
3. Дышишь - бан

Нарушение правил может привести к приезду тебе домой."""
    bot.send_message(message.chat.id, rules_text, parse_mode='Markdown')

# Обработка команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    help_text = """🤖 *Мои возможности:*

*Команды:*
/start - Приветствие
/rules - Правила общения
/help - Список возможностей
/sea_battle - Начать игру Морской бой
/hangman - Начать игру Виселица

*Обработка сообщений:*
Я автоматически обрабатываю любые текстовые сообщения по правилам выше."""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')


# ------------------  Игра "Морской бой" ------------------- #
# Обработка команды /sea_battle для начала игры
@bot.message_handler(commands=['sea_battle'])
def start_battle(message):
    global battlefield
    battlefield = create_battlefield()
    bot.send_message(message.chat.id, "Начинаем новую игру Морской бой! Поле 10x10, подготовлено.")
    # Можно добавить вывод поля или инструкцию

# Обработка сообщений, связанных с морским боем (например, координаты выстрела)
@bot.message_handler(func=lambda message: message.text and message.text.startswith('/shot'))
def handle_shot(message):
    # пример: /shot 3 5
    parts = message.text.split()
    if len(parts) != 3:
        bot.send_message(message.chat.id, "Используйте команду: /shot <строка> <столбец> (от 0 до 9)")
        return
    try:
        row = int(parts[1])
        col = int(parts[2])
        if 0 <= row < 10 and 0 <= col < 10:
            # тут логика обработки выстрела
            result = battlefield[row][col]
            bot.send_message(message.chat.id, f"Выстрел в ({row}, {col}): {result}")
        else:
            bot.send_message(message.chat.id, "Координаты вне диапазона 0-9")
    except:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректные числа.")


# ------------------  Игра "Виселица" ------------------- #
@bot.message_handler(commands=['hangman'])
def start_hangman_game(message):
    start_hangman()
    bot.send_message(message.chat.id, f"Давайте сыграем в Виселицу!\n\n{display_word}\n\nОтгадвайте буквы или слово полностью.")

# Обработка сообщений для виселицы
@bot.message_handler(func=lambda message: True)
def handle_any_message(message):
    global display_word, current_word, wrong_guesses
    text = message.text.strip()

    if text.lower().startswith('/shot'):
        # уже есть обработчик /shot
        return

    if text.lower() == '/hangman':
        # запуск игры виселицы
        start_hangman_game(message)
        return

    # Обработка при игре в виселицу
    if current_word:
        # Проверка, что пользователь вводит одну букву или слово
        guess = text.lower()
        if len(guess) == 1:
            if guess in wrong_guesses or guess in display_word.lower():
                bot.send_message(message.chat.id, "Эту букву уже пробовали.")
                return
            if guess in current_word:
                # Обновить display_word
                new_display = list(display_word)
                for i, ch in enumerate(current_word):
                    if ch == guess:
                        new_display[i] = guess
                display_word = ''.join(new_display)
                if '_' not in display_word:
                    bot.send_message(message.chat.id, f"Поздравляю! Вы выиграли! Загадано слово: {current_word}")
                    current_word = ''
                else:
                    bot.send_message(message.chat.id, f"Отлично! В слове: {display_word}")
            else:
                wrong_guesses.add(guess)
                attempts_left = max_attempts - len(wrong_guesses)
                if attempts_left <= 0:
                    bot.send_message(message.chat.id, f"Игра окончена! Вы проиграли. Загаданное слово: {current_word}")
                    current_word = ''
                else:
                    bot.send_message(message.chat.id, f"Неверно! Осталось попыток: {attempts_left}\n{display_word}")
        elif len(guess) > 1:
            # пользователь вводит слово целиком
            if guess == current_word:
                bot.send_message(message.chat.id, f"Поздравляю! Вы правильно угадали слово: {current_word}")
                current_word = ''
            else:
                wrong_guesses.update(guess)
                attempts_left = max_attempts - len(wrong_guesses)
                if attempts_left <= 0:
                    bot.send_message(message.chat.id, f"Игра окончена! Вы проиграли. Загаданное слово: {current_word}")
                    current_word = ''
                else:
                    bot.send_message(message.chat.id, f"Неверно! Осталось попыток: {attempts_left}\n{display_word}")
    else:
        # Нет активной игры
        pass

# --------- Обработка любых сообщений для фильтров, как раньше --------- #
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    original_text = message.text

    # Проверка, есть ли команда или команда игры
    if original_text.startswith('/'):
        return  # команды уже обрабатываются отдельно

    # Обрабатываем текст по правилам
    processed_text = process_text(original_text)

    response = f"📝 *Исходное сообщение:*\n{original_text}\n\n🔄 *После обработки:*\n{processed_text}"
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


# --------- запуск бота ---------
if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
