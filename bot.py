import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📊 Получить сигнал"],
        ["💱 Выбрать валюту"],
        ["📜 История"]
    ]

    reply = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🤖 Pocket Signal Bot\n\nВыберите действие:",
        reply_markup=reply
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📊 Получить сигнал":
        await update.message.reply_text(
            "⏳ Анализ рынка...\n\n"
            "Скоро здесь появится настоящий сигнал."
        )

    elif text == "💱 Выбрать валюту":
        await update.message.reply_text(
            "Выбор валюты будет добавлен следующим шагом."
        )

    elif text == "📜 История":
        await update.message.reply_text(
            "История сигналов пока пустая."
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))

    print("Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
