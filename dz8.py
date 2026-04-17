import pickle
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

heroes = {
    'Супермен': [0.1, 0.9, 0.0],   
    'Бэтмен': [0.2, 0.8, 0.1],
    'Человек-паук': [0.3, 0.7, 0.2]
}

def start(update, context):
    update.message.reply_text("Привет! Введите имя супергероя, чтобы я определил цвет его костюма.")

def handle_message(update, context):
    hero_name = update.message.text.strip()
    if hero_name in heroes:
        input_data = [heroes[hero_name]]  
        predicted_color = model.predict(input_data)[0]
        update.message.reply_text(f"Цвет костюма {hero_name}: {predicted_color}")
    else:
        update.message.reply_text("Я не знаю этого героя. Попробуйте другого.")

def main():
    updater = Updater("8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
