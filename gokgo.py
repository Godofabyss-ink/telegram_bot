import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
from datetime import datetime, timedelta
import json

TOKEN = '8170013712:AAGIZc_Y7rQkB34ImHvnQB03RNT52pD5we4'

# Для хранения напоминаний
reminders = {}

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ваш личный ассистент. Используйте /напомни, чтобы создать напоминание.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Команды:\n /напомни — создать напоминание\n /список — список всех напоминаний")

async def напомни(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    args = context.args

    if len(args) < 2:
        await update.message.reply_text("Используйте формат:\n/напомни [через сколько минут] [текст напоминания]\nНапример: /напомни 10 Встать и сделать упражнения.")
        return

    try:
        minutes = int(args[0])
        text = ' '.join(args[1:])
        notify_time = datetime.now() + timedelta(minutes=minutes)

        # Сохраняем напоминание
        if user_id not in reminders:
            reminders[user_id] = []

        reminders[user_id].append({'time': notify_time.isoformat(), 'text': text})

        await update.message.reply_text(f"Напоминание запланировано на {notify_time.strftime('%H:%M:%S')}: {text}")

        # Запуск задачи для отправки напоминания
        asyncio.create_task(send_reminder_after(user_id, notify_time, text))
    except ValueError:
        await update.message.reply_text("Пожалуйста, укажите число минут как целое число.")

async def список(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_reminders = reminders.get(user_id, [])
    if not user_reminders:
        await update.message.reply_text("У вас пока нет напоминаний.")
        return

    msg = "Ваши напоминания:\n"
    for idx, rem in enumerate(user_reminders, 1):
        time_str = datetime.fromisoformat(rem['time']).strftime('%H:%M:%S')
        msg += f"{idx}. {time_str} — {rem['text']}\n"
    await update.message.reply_text(msg)

async def send_reminder_after(user_id, notify_time, text):
    # Ждём до времени напоминания
    now = datetime.now()
    delay = (notify_time - now).total_seconds()
    if delay > 0:
        await asyncio.sleep(delay)

    # Отправляем сообщение
    try:
        # Получение обновлений пользователя
        # Для этого нужен объект бота
        bot = application.bot
        await bot.send_message(chat_id=user_id, text=f"⏰ Напоминание: {text}")
        # Удалим напоминание после отправки
        if user_id in reminders:
            reminders[user_id] = [rem for rem in reminders[user_id] if rem['text'] != text]
    except Exception as e:
        logger.error(f"Ошибка при отправке напоминания: {e}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("напомни", напомни))
    application.add_handler(CommandHandler("список", список))

    print("Бот запущен")
    application.run_polling()
