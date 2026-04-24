import telebot
from telebot.types import InlineQueryResultArticle, InputTextMessageContent

TOKEN = '8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4'
bot = telebot.TeleBot(TOKEN)

pizza_menu = [
    {'name': 'Маргарита', 'price': '300 ₽'},
    {'name': 'Пепперони', 'price': '400 ₽'},
    {'name': 'Гавайи', 'price': '350 ₽'},
    {'name': 'Четыре сыра', 'price': '450 ₽'}
]

@bot.inline_handler(lambda query: True)
def handle_inline(query):
    results = []
    for pizza in pizza_menu:
        result = InlineQueryResultArticle(
            id=pizza['name'],  
            title=pizza['name'],
            input_message_content=InputTextMessageContent(
                f"Вы выбрали пиццу: {pizza['name']}\nЦена: {pizza['price']}\n\nСпасибо за заказ!"
            ),
            description=f"{pizza['name']} - {pizza['price']}",
            thumb_url="https://pngimg.com/uploads/pizza/pizza_PNG44044.png"
        )
        results.append(result)
    bot.answer_inline_query(query.id, results)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Используйте инлайн введите @ваш_бот_имя и выберите пиццу!")

bot.polling()
