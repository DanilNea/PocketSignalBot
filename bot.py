import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["📊 Получить сигнал"],
        ["📂 Выбрать актив"],
        ["📜 История"]
    ]

    await update.message.reply_text(
        "🤖 Pocket Signal Bot\n\nВыберите действие:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📂 Выбрать актив":

        keyboard = [
            ["💱 Валюты Forex"],
            ["₿ Криптовалюты"],
            ["🥇 Сырьевые товары"],
            ["📈 Индексы"],
            ["⬅️ Назад"]
        ]

        await update.message.reply_text(
            "Выберите раздел:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )


    elif text == "💱 Валюты Forex":

        keyboard = [
            ["EUR/USD"],
            ["GBP/USD"],
            ["USD/JPY"],
            ["⬅️ Назад"]
        ]

        await update.message.reply_text(
            "Выберите валютную пару:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )


    elif text == "₿ Криптовалюты":

        keyboard = [
            ["BTC/USDT"],
            ["ETH/USDT"],
            ["SOL/USDT"],
            ["⬅️ Назад"]
        ]

        await update.message.reply_text(
            "Выберите криптовалюту:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )


    elif text == "🥇 Сырьевые товары":

        keyboard = [
            ["🥇 Gold XAU/USD"],
            ["🛢 Oil WTI"],
            ["⬅️ Назад"]
        ]

        await update.message.reply_text(
            "Выберите товар:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True
            )
        )


    elif text in [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "BTC/USDT",
        "ETH/USDT",
        "SOL/USDT",
        "🥇 Gold XAU/USD",
        "🛢 Oil WTI"
    ]:

        context.user_data["asset"] = text

        await update.message.reply_text(
            f"✅ Вы выбрали: {text}\n\n"
            "Теперь можно получить сигнал 📊"
        )


    elif text == "📊 Получить сигнал":

        asset = context.user_data.get(
            "asset",
            "актив не выбран"
        )

        await update.message.reply_text(
            f"⏳ Анализируем: {asset}\n\n"
            "Сигнал будет добавлен следующим этапом."
        )


    elif text == "📜 История":

        await update.message.reply_text(
            "История сигналов пока пустая."
        )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(filters.TEXT, message_handler)
    )

    print("Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
