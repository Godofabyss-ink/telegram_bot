import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data_str = update.message.web_app_data.data
        data = json.loads(data_str)
        data_type = data.get('data_type')

        if data_type == "user_sub":
            user_name = data.get('data_name', 'Неизвестно')
            user_email = data.get('data_email', 'нет email')
            user_tel = data.get('data_tel', 'нет телефона')
            msg = (
                f"👤 Регистрация:\n"
                f"Имя: {user_name}\n"
                f"Email: {user_email}\n"
                f"Телефон: {user_tel}"
            )
        elif data_type == "buy_item":
            article_name = data.get('data_name', 'Товар не выбран')
            msg = f"🛒 Вы хотите купить товар: {article_name}!"
        else:
            msg = "⚠️ Неизвестный тип данных!"
    except Exception as e:
        msg = f"Произошла ошибка!\n{e}"

    await update.message.reply_text(msg)

async def main():
    app = ApplicationBuilder().token("8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4").build()

    app.add_handler(MessageHandler(filters.UpdateType.WEB_APP_DATA, handle_webapp_data))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
