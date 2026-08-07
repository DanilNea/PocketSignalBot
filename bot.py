import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")


def menu():
    keyboard = [
        ["📊 Получить сигнал"],
        ["📂 Выбрать актив"],
        ["⏱ Время сделки"],
        ["⚙️ Настройки"],
        ["📜 История"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Pocket Signal Bot\n\nГлавное меню:",
        reply_markup=menu()
    )


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📂 Выбрать актив":
        keyboard = [
            ["💱 Валюты Forex"],
            ["₿ Криптовалюты"],
            ["🥇 Сырьевые товары"],
            ["📈 Индексы"],
            ["⬅️ Назад"],
            ["🏠 Главное меню"]
        ]

        await update.message.reply_text(
            "📂 Выберите раздел:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )


    elif text == "⏱ Время сделки":
        keyboard = [
            ["30 секунд"],
            ["1 минута"],
            ["3 минуты"],
            ["5 минут"],
            ["15 минут"],
            ["⬅️ Назад"],
            ["🏠 Главное меню"]
        ]

        await update.message.reply_text(
            "⏱ Выберите время сделки:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )


    elif text == "⚙️ Настройки":
        keyboard = [
            ["💱 Сменить актив"],
            ["⏱ Изменить время"],
            ["📊 Стиль анализа"],
            ["🔔 Уведомления"],
            ["🌐 Язык"],
            ["⬅️ Назад"],
            ["🏠 Главное меню"]
        ]

        await update.message.reply_text(
            "⚙️ Настройки:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )


    elif text == "🏠 Главное меню":
        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=menu()
        )


    elif text == "⬅️ Назад":
        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=menu()
        )


    else:
        await update.message.reply_text(
            f"Вы выбрали: {text}\n\nФункция будет добавлена."
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handler))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
