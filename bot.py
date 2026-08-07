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
        "🤖 Pocket Signal Bot\n\n"
        "🏠 Главное меню:",
        reply_markup=main_menu()
    )


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    # =========================
    # ВЫБОР АКТИВА
    # =========================

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


    # =========================
    # ВАЛЮТЫ
    # =========================

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


    # =========================
    # КРИПТОВАЛЮТЫ
    # =========================

    elif text == "₿ Криптовалюты":

        context.user_data["page"] = "crypto"

        await update.message.reply_text(
            "₿ Выберите криптовалюту:",
            reply_markup=show_menu([
                ["BTC/USDT"],
                ["ETH/USDT"],
                ["BNB/USDT"],
                ["SOL/USDT"],
                ["XRP/USDT"],
                ["ADA/USDT"],
                ["DOGE/USDT"],
                ["⬅️ Назад"]
            ])
        )


    # =========================
    # СЫРЬЕВЫЕ ТОВАРЫ
    # =========================

    elif text == "🥇 Сырьевые товары":

        context.user_data["page"] = "commodities"

        await update.message.reply_text(
            "🥇 Выберите сырьевой товар:",
            reply_markup=show_menu([
                ["🥇 Gold XAU/USD"],
                ["🥈 Silver XAG/USD"],
                ["🛢 Oil WTI"],
                ["🛢 Oil Brent"],
                ["🔥 Natural Gas"],
                ["⬅️ Назад"]
            ])
        )


    # =========================
    # АКЦИИ
    # =========================

    elif text == "🏢 Акции":

        context.user_data["page"] = "stocks"

        await update.message.reply_text(
            "🏢 Выберите акцию:",
            reply_markup=show_menu([
                ["Apple"],
                ["Tesla"],
                ["Microsoft"],
                ["Amazon"],
                ["Google"],
                ["NVIDIA"],
                ["Meta"],
                ["⬅️ Назад"]
            ])
        )


    # =========================
    # ИНДЕКСЫ
    # =========================

    elif text == "📈 Индексы":

        context.user_data["page"] = "indexes"

        await update.message.reply_text(
            "📈 Выберите индекс:",
            reply_markup=show_menu([
                ["NASDAQ"],
                ["S&P 500"],
                ["Dow Jones"],
                ["DAX"],
                ["FTSE 100"],
                ["Nikkei 225"],
                ["⬅️ Назад"]
            ])
        )


    # =========================
    # ВЫБОР КОНКРЕТНОГО АКТИВА
    # =========================

    elif text in [

        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "AUD/USD",
        "USD/CAD",
        "USD/CHF",

        "BTC/USDT",
        "ETH/USDT",
        "BNB/USDT",
        "SOL/USDT",
        "XRP/USDT",
        "ADA/USDT",
        "DOGE/USDT",

        "🥇 Gold XAU/USD",
        "🥈 Silver XAG/USD",
        "🛢 Oil WTI",
        "🛢 Oil Brent",
        "🔥 Natural Gas",

        "Apple",
        "Tesla",
        "Microsoft",
        "Amazon",
        "Google",
        "NVIDIA",
        "Meta",

        "NASDAQ",
        "S&P 500",
        "Dow Jones",
        "DAX",
        "FTSE 100",
        "Nikkei 225"

    ]:

        context.user_data["asset"] = text
        context.user_data["page"] = "time"

        await update.message.reply_text(
            f"✅ Актив выбран:\n\n"
            f"📊 {text}\n\n"
            f"⏱ Выберите время сделки:",
            reply_markup=show_menu([
                ["30 секунд"],
                ["1 минута"],
                ["3 минуты"],
                ["5 минут"],
                ["15 минут"],
                ["⬅️ Назад"]
            ])
        )


    # =========================
    # ВЫБОР ВРЕМЕНИ
    # =========================

    elif text in [

        "30 секунд",
        "1 минута",
        "3 минуты",
        "5 минут",
        "15 минут"

    ]:

        context.user_data["time"] = text

        asset = context.user_data.get(
            "asset",
            "не выбран"
        )

        await update.message.reply_text(
            f"✅ Настройки сохранены!\n\n"
            f"📊 Актив: {asset}\n"
            f"⏱ Время: {text}\n\n"
            f"📊 Теперь можно получать сигнал.",
            reply_markup=show_menu([
                ["📊 Получить сигнал"],
                ["📂 Изменить актив"],
                ["⏱ Изменить время"],
                ["⬅️ Назад"]
            ])
        )


    # =========================
    # ПОЛУЧИТЬ СИГНАЛ
    # =========================

    elif text == "📊 Получить сигнал":

        asset = context.user_data.get(
            "asset",
            "не выбран"
        )

        trade_time = context.user_data.get(
            "time",
            "не выбрано"
        )

        await update.message.reply_text(
            f"📊 Параметры сигнала:\n\n"
            f"📊 Актив: {asset}\n"
            f"⏱ Время: {trade_time}\n\n"
            f"⏳ Анализ рынка...\n\n"
            f"⚠️ Реальный сигнал пока не подключен."
        )


    # =========================
    # ИЗМЕНИТЬ АКТИВ
    # =========================

    elif text == "📂 Изменить актив":

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


    # =========================
    # ИЗМЕНИТЬ ВРЕМЯ
    # =========================

    elif text == "⏱ Изменить время":

        await update.message.reply_text(
            "⏱ Выберите новое время:",
            reply_markup=show_menu([
                ["30 секунд"],
                ["1 минута"],
                ["3 минуты"],
                ["5 минут"],
                ["15 минут"],
                ["⬅️ Назад"]
            ])
        )


    # =========================
    # НАСТРОЙКИ
    # =========================

    elif text == "⚙️ Настройки":

        asset = context.user_data.get(
            "asset",
            "не выбран"
        )

        trade_time = context.user_data.get(
            "time",
            "не выбрано"
        )

        await update.message.reply_text(
            f"⚙️ Настройки\n\n"
            f"📊 Актив: {asset}\n"
            f"⏱ Время: {trade_time}",
            reply_markup=show_menu([
                ["📂 Изменить актив"],
                ["⏱ Изменить время"],
                ["⬅️ Назад"]
            ])
        )


    # =========================
    # ИСТОРИЯ
    # =========================

    elif text == "📜 История":

        await update.message.reply_text(
            "📜 История сигналов пока пустая."
        )


    # =========================
    # ГЛАВНОЕ МЕНЮ
    # =========================

    elif text == "🏠 Главное меню":

        context.user_data["page"] = "main"

        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )


    # =========================
    # НАЗАД
    # =========================

    elif text == "⬅️ Назад":

        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )


    else:

        await update.message.reply_text(
            f"Вы выбрали: {text}"
        )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handler
        )
    )

    print("Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
