import telebot


TOKEN = '8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4'
bot = telebot.TeleBot(TOKEN)


questions = [
    {"question": "Столица России?", "options": ["Москва", "Санкт-Петербург", "Новосибирск"], "answer": "Москва"},
    {"question": "2+2= ?", "options": ["3", "4", "5"], "answer": "4"},
    {"question": "Кто создал Python?", "options": ["Гвидо ван Россам", "Билл Гейтс", "Джобс"], "answer": "Гвидо ван Россам"}
]

scores = {}
user_states = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    scores[user_id] = 0
    user_states[user_id] = {'current_q': 0}
    bot.send_message(message.chat.id, "Здравствуйте! Начнем контрольную. Ответьте на вопросы.")
    send_question(message.chat.id)

def send_question(chat_id):
    user_id = chat_id
    state = user_states[user_id]
    q_index = state['current_q']
    if q_index >= len(questions):
        score = scores[user_id]
        total = len(questions)
        grade = ''
        if score == total:
            grade = "Отлично!"
        elif score >= total/2:
            grade = "Зачет!"
        else:
            grade = "Неуд."
        bot.send_message(chat_id, f"Викторина окончена! Ваша оценка: {score}/{total}. {grade}")
        return
    q = questions[q_index]
    options = q["options"]
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for opt in options:
        markup.add(opt)
    bot.send_message(chat_id, q["question"], reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    chat_id = message.chat.id
    user_id = chat_id
    if user_id not in user_states:
        bot.send_message(chat_id, "Введите /start для начала.")
        return
    state = user_states[user_id]
    q_index = state['current_q']
    if q_index >= len(questions):
        return
    answer = message.text
    correct_answer = questions[q_index]["answer"]
    if answer == correct_answer:
        scores[user_id] += 1
    state['current_q'] += 1
    send_question(chat_id)

bot.polling()
