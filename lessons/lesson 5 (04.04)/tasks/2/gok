from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    # reply клавиатура с кнопкой
    reply_keyboard = [['Показать кнопки']]  
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text(
        f"Привет, {user.first_name}! Нажми кнопку ниже, чтобы увидеть пример.",
        reply_markup=markup
    )


def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text == 'Показать кнопки':
        # inline клавиатура с callback кнопками и url кнопку
        keyboard = [
            [
                InlineKeyboardButton("Кнопка callback 1", callback_data='callback_1'),
                InlineKeyboardButton("Кнопка callback 2", callback_data='callback_2')
            ],
            [InlineKeyboardButton("Перейти на сайт", url='https://example.com')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(
            "Это пример inline клавиатуры с callback и url кнопками:",
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text("Я получил ваше сообщение!")

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'callback_1':
        query.edit_message_text(text="Вы нажали кнопку callback 1")
    elif data == 'callback_2':
        query.edit_message_text(text="Вы нажали кнопку callback 2")

def main():
    TOKEN = '8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4'  # вставьте ваш токен
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрация обработчиков
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
