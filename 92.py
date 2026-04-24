import telebot

TOKEN = '8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4'
bot = telebot.TeleBot(TOKEN)

questions = [
    {
        "question": "Столица Франции?",
        "options": ["Париж", "Лондон", "Берлин"],
        "answer": "Париж",
        "fifty_fifty": ["Париж", "Лондон"]
    },
    {
        "question": "Кто написал 'Войну и мир'?",
        "options": ["Толстой", "Достоевский", "Пушкин"],
        "answer": "Толстой",
        "fifty_fifty": ["Толстой", "Пушкин"]
    },
    {
        "question": "Самый крупный океан?",
        "options": ["Тихий", "Атлантический", "Индийский"],
        "answer": "Тихий",
        "fifty_fifty": ["Тихий", "Индийский"]
    }
]

user_state = {}

@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id
    user_state[chat_id] = {
        'current': 0,
        'score': 0,
        'used_fifty': False
    }
    send_question(chat_id)

def send_question(chat_id):
    state = user_state[chat_id]
    q_index = state['current']
    if q_index >= len(questions):
        bot.send_message(chat_id, f"Игра окончена! Ваш результат: {state['score']} из {len(questions)}.")
        return
    q = questions[q_index]
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in q["options"]:
        markup.add(opt)
    markup.add('Помощь', '50/50')
    bot.send_message(chat_id, q["question"], reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_response(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        bot.send_message(chat_id, "Введите /start чтобы начать игру.")
        return
    state = user_state[chat_id]
    q = questions[state['current']]
    text = message.text

    if text == 'Помощь':
        bot.send_message(chat_id, f"Подсказка: правильный ответ — {q['answer']}")
        return
    elif text == '50/50':
        options = q['fifty_fifty']
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for opt in options:
            markup.add(opt)
        bot.send_message(chat_id, "50 на 50!", reply_markup=markup)
        state['used_fifty'] = True
        return
    else:
        if text == q["answer"]:
            state['score'] += 1
        state['current'] += 1
        send_question(chat_id)

bot.polling()
