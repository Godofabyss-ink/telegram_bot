import pickle
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


with open('multi_hero_model.pkl', 'rb') as f:
    model = pickle.load(f)

heroes_dict = {
    'Супермен': [1, 0, 0],
    'Бэтмен': [0, 1, 0],
    'Человек-паук': [0, 0, 1],
    'Женщина-кошка': [1, 1, 0],
    'Флэш': [0, 1, 1]
}

def start(update, context):
    update.message.reply_text("Введите имена героев через запятую (например, 'Супермен, Флэш'):")

def handle_message(update, context):
    input_text = update.message.text.strip()
    heroes_list = [h.strip() for h in input_text.split(',')]
    results = ""
    for hero in heroes_list:
        if hero in heroes_dict:
            features = [heroes_dict[hero]]
            color_pred = model.predict(features)[0]
            results += f"{hero}: {color_pred}\n"
        else:
            results += f"{hero}: не найден\n"
    update.message.reply_text(results)

def main():
    updater = Updater("8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
