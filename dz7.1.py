from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random


user_data = {}

def start(update, context):
    update.message.reply_text("Привет! Я игра 'Угадай число'. Выберите число от 1 до 100.")
    secret_number = random.randint(1, 100)
    user_id = update.message.chat_id
    user_data[user_id] = secret_number
    print(f"Загадано число для пользователя {user_id}: {secret_number}")  # Для отладки

def handle_message(update, context):
    user_id = update.message.chat_id
    if user_id not in user_data:
        update.message.reply_text("Пожалуйста, начните игру командой /start.")
        return
    try:
        guess = int(update.message.text)
    except ValueError:
        update.message.reply_text("Пожалуйста, введите число!")
        return

    secret_number = user_data[user_id]
    if guess == secret_number:
        update.message.reply_text("Поздравляю! Вы угадали!")
        # Новый раунд
        new_number = random.randint(1, 100)
        user_data[user_id] = new_number
        update.message.reply_text("Я загадал новое число! Попробуйте его угадать.")
    elif guess < secret_number:
        update.message.reply_text("Моё число больше.")
    else:
        update.message.reply_text("Моё число меньше.")

def main():
    updater = Updater("8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4", use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
