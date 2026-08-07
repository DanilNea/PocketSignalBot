import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")


def show_menu(buttons):
    return ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )


def main_menu():
    return show_menu([
        ["📊 Получить сигнал"],
        ["📂 Выбрать актив"],
        ["⏱ Время сделки"],
        ["⚙️ Настройки"],
        ["📜 История"]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["page"] = "main"

    await update.message.reply_text(
        "🤖 Pocket Signal Bot\n\n🏠 Главное меню:",
        reply_markup=main_menu()
    )


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "📂 Выбрать актив":

        context.user_data["page"] = "assets"

        await update.message.reply_text(
            "📂 Выберите раздел:",
            reply_markup=show_menu([
                ["💱 Валюты"],
                ["₿ Криптовалюты"],
                ["🥇 Сырьевые товары"],
                ["🏢 Акции"],
                ["📈 Индексы"],
                ["⬅️ Назад"]
            ])
        )


    elif text == "💱 Валюты":

        context.user_data["page"] = "forex"

        await update.message.reply_text(
            "💱 Выберите валютную пару:",
            reply_markup=show_menu([
                ["EUR/USD"],
                ["GBP/USD"],
                ["USD/JPY"],
                ["AUD/USD"],
                ["USD/CAD"],
                ["USD/CHF"],
                ["⬅️ Назад"]
            ])
        )


    elif text in [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "AUD/USD",
        "USD/CAD",
        "USD/CHF"
    ]:

        context.user_data["asset"] = text

        await update.message.reply_text(
            f"✅ Выбран актив:\n\n💱 {text}\n\n"
            "Следующий шаг — выбор времени сделки."
        )


    elif text == "⬅️ Назад":

        context.user_data["page"] = "main"

        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )


    elif text == "🏠 Главное меню":

        context.user_data["page"] = "main"

        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )


    else:

        await update.message.reply_text(
            f"Вы нажали: {text}\n\nФункция добавляется."
        )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(filters.TEXT, handler)
    )

    print("Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
