import telebot
import re
import string

TOKEN = '8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4'

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)


# Функция для обработки текста по правилам задания №2
def process_text(text):
    # Проверяем наличие знаков препинания
    punctuation_chars = set(string.punctuation)
    has_punctuation = any(char in punctuation_chars for char in text)

    # Проверяем наличие пробелов
    has_spaces = ' ' in text


    if not has_punctuation and not has_spaces:
        # Берем каждый третий символ, начиная с первого (индекс 0)
        result = text[0::3]  # каждый третий символ
        return result.lower()

    # Случай 2: Нет знаков препинания, НО есть пробелы
    elif not has_punctuation and has_spaces:
        # Разбиваем на слова и каждое слово пишем с большой буквы
        words = text.split()
        capitalized_words = [word.capitalize() for word in words]
        return ' '.join(capitalized_words)

    # Случай 3: Есть знаки препинания (с пробелами или без)
    else:
        # Берем половину строки (при нечетной длине - меньшую часть)
        half_length = len(text) // 2  # целочисленное деление дает меньшую часть для нечетной длины
        result = text[:half_length]  # берем первую половину
        return result.upper()


# Задание №1: Обработчик команды /start - приветствие пользователя по имени
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Получаем имя пользователя
    user_name = message.from_user.first_name
    if not user_name:
        user_name = message.from_user.username

    greeting = f"Привет, {user_name}! 👋\n\nЯ бот, который умеет обрабатывать сообщения через фильтры."
    bot.send_message(message.chat.id, greeting)


# Задание №1: Обработчик команды /rules - выводит правила общения
@bot.message_handler(commands=['rules'])
def handle_rules(message):
    rules_text = """📜 *Правила общения:*

1. Админа надо ########
2. Говоришь - мут
3. Дышишь - бан

Нарушение правил может привести к приезду тебе домой."""

    bot.send_message(message.chat.id, rules_text, parse_mode='Markdown')


# Задание №1: Обработчик команды /help - выводит список возможностей
@bot.message_handler(commands=['help'])
def handle_help(message):
    help_text = """🤖 *Мои возможности:*

*Команды:*
/start - Приветствие
/rules - Правила общения
/help - Список возможностей

*Обработка сообщений:*
Я автоматически обрабатываю любые текстовые сообщения по следующим правилам:

1️⃣ *Если текст без знаков препинания и пробелов*:
   Беру каждый третий символ и привожу к нижнему регистру
   Пример: `абвгдеёжз` → `аге`

2️⃣ *Если текст без знаков препинания, но с пробелами*:
   Каждое слово пишу с большой буквы
   Пример: `привет как дела` → `Привет Как Дела`

3️⃣ *Если текст содержит знаки препинания*:
   Беру половину строки (меньшую часть) и пишу заглавными буквами
   Пример: `Привет, как дела?` → `ПРИВЕТ,`

Отправьте мне любое сообщение, и я его обработаю! ✨"""

    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')


# Задание №2: Обработчик всех текстовых сообщений (меняет сообщение через фильтры)
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Получаем текст сообщения
    original_text = message.text

    # Обрабатываем текст по правилам
    processed_text = process_text(original_text)

    # Отправляем обработанное сообщение
    response = f"📝 *Исходное сообщение:*\n{original_text}\n\n🔄 *После обработки:*\n{processed_text}"

    bot.send_message(message.chat.id, response, parse_mode='Markdown')


# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    try:
        bot.polling(none_stop=True, interval=0, timeout=30)
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Попробуйте перезапустить бота")