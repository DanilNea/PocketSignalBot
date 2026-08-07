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


    # ВЫБОР АКТИВА
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


    # ВАЛЮТЫ
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


    # ВЫБОР ВАЛЮТЫ
    elif text in [
        "EUR/USD",
        "GBP/USD",
        "USD/JPY",
        "AUD/USD",
        "USD/CAD",
        "USD/CHF"
    ]:

        context.user_data["asset"] = text
        context.user_data["page"] = "time"

        await update.message.reply_text(
            f"✅ Актив выбран:\n\n"
            f"💱 {text}\n\n"
            f"⏱ Теперь выберите время сделки:",
            reply_markup=show_menu([
                ["30 секунд"],
                ["1 минута"],
                ["3 минуты"],
                ["5 минут"],
                ["15 минут"],
                ["⬅️ Назад"]
            ])
        )


    # ВЫБОР ВРЕМЕНИ
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
            f"💱 Актив: {asset}\n"
            f"⏱ Время: {text}\n\n"
            f"📊 Теперь можно получать сигнал.",
            reply_markup=show_menu([
                ["📊 Получить сигнал"],
                ["📂 Изменить актив"],
                ["⏱ Изменить время"],
                ["⬅️ Назад"]
            ])
        )


    # ИЗМЕНИТЬ АКТИВ
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


    # ИЗМЕНИТЬ ВРЕМЯ
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


    # ПОЛУЧИТЬ СИГНАЛ
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
            f"💱 Актив: {asset}\n"
            f"⏱ Время: {trade_time}\n\n"
            f"⏳ Анализ рынка...\n\n"
            f"⚠️ Реальный сигнал пока не подключен."
        )


    # НАСТРОЙКИ
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
            f"💱 Актив: {asset}\n"
            f"⏱ Время: {trade_time}",
            reply_markup=show_menu([
                ["📂 Изменить актив"],
                ["⏱ Изменить время"],
                ["⬅️ Назад"]
            ])
        )


    # ГЛАВНОЕ МЕНЮ
    elif text == "🏠 Главное меню":

        context.user_data["page"] = "main"

        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )


    # НАЗАД
    elif text == "⬅️ Назад":

        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )


    # ИСТОРИЯ
    elif text == "📜 История":

        await update.message.reply_text(
            "📜 История сигналов пока пустая."
        )


    # ОСТАЛЬНЫЕ КНОПКИ
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
