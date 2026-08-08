import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")


def menu(buttons):
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def main_menu():
    return menu([
        ["📊 Получить сигнал"],
        ["📂 Выбрать актив"],
        ["⏱ Время сделки"],
        ["⚙️ Настройки"],
        ["📜 История"]
    ])


def categories():
    return menu([
        ["💱 Валюты"],
        ["₿ Криптовалюты"],
        ["🥇 Сырьевые товары"],
        ["🏢 Акции"],
        ["📈 Индексы"],
        ["⬅️ Назад"]
    ])


def forex():
    return menu([
        ["EUR/USD"],
        ["GBP/USD"],
        ["USD/JPY"],
        ["AUD/USD"],
        ["USD/CAD"],
        ["USD/CHF"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


def crypto():
    return menu([
        ["BTC/USDT"],
        ["ETH/USDT"],
        ["BNB/USDT"],
        ["SOL/USDT"],
        ["XRP/USDT"],
        ["ADA/USDT"],
        ["DOGE/USDT"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


def commodities():
    return menu([
        ["🥇 Gold XAU/USD"],
        ["🥈 Silver XAG/USD"],
        ["🛢 Oil WTI"],
        ["🛢 Oil Brent"],
        ["🔥 Natural Gas"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


def stocks():
    return menu([
        ["Apple"],
        ["Tesla"],
        ["Microsoft"],
        ["Amazon"],
        ["Google"],
        ["NVIDIA"],
        ["Meta"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


def indexes():
    return menu([
        ["NASDAQ"],
        ["S&P 500"],
        ["Dow Jones"],
        ["DAX"],
        ["FTSE 100"],
        ["Nikkei 225"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


def times():
    return menu([
        ["30 секунд"],
        ["1 минута"],
        ["3 минуты"],
        ["5 минут"],
        ["15 минут"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()
    context.user_data["page"] = "main"

    await update.message.reply_text(
        "🤖 Pocket Signal Bot\n\n🏠 Главное меню",
        reply_markup=main_menu()
    )


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    page = context.user_data.get("page", "main")


    # Главное меню
    if text == "🏠 Главное меню":

        context.user_data["page"] = "main"

        await update.message.reply_text(
            "🏠 Главное меню",
            reply_markup=main_menu()
        )

        return


    # Выбор актива
    if text == "📂 Выбрать актив" or text == "📂 Изменить актив":

        context.user_data["page"] = "categories"

        await update.message.reply_text(
            "📂 Выберите раздел:",
            reply_markup=categories()
        )

        return


    # Валюты
    if text == "💱 Валюты":

        context.user_data["page"] = "forex"

        await update.message.reply_text(
            "💱 Выберите валютную пару:",
            reply_markup=forex()
        )

        return


    # Криптовалюты
    if text == "₿ Криптовалюты":

        context.user_data["page"] = "crypto"

        await update.message.reply_text(
            "₿ Выберите криптовалюту:",
            reply_markup=crypto()
        )

        return


    # Сырьевые товары
    if text == "🥇 Сырьевые товары":

        context.user_data["page"] = "commodities"

        await update.message.reply_text(
            "🥇 Выберите сырьевой товар:",
            reply_markup=commodities()
        )

        return


    # Акции
    if text == "🏢 Акции":

        context.user_data["page"] = "stocks"

        await update.message.reply_text(
            "🏢 Выберите акцию:",
            reply_markup=stocks()
        )

        return


    # Индексы
    if text == "📈 Индексы":

        context.user_data["page"] = "indexes"

        await update.message.reply_text(
            "📈 Выберите индекс:",
            reply_markup=indexes()
        )

        return


    # Все активы
    assets = [
        "EUR/USD", "GBP/USD", "USD/JPY",
        "AUD/USD", "USD/CAD", "USD/CHF",

        "BTC/USDT", "ETH/USDT", "BNB/USDT",
        "SOL/USDT", "XRP/USDT", "ADA/USDT",
        "DOGE/USDT",

        "🥇 Gold XAU/USD", "🥈 Silver XAG/USD",
        "🛢 Oil WTI", "🛢 Oil Brent", "🔥 Natural Gas",

        "Apple", "Tesla", "Microsoft", "Amazon",
        "Google", "NVIDIA", "Meta",

        "NASDAQ", "S&P 500", "Dow Jones",
        "DAX", "FTSE 100", "Nikkei 225"
    ]


    # Выбрали актив
    if text in assets:

        context.user_data["asset"] = text

        # Очень важно: запоминаем предыдущий экран
        context.user_data["previous_page"] = page

        context.user_data["page"] = "time"

        await update.message.reply_text(
            f"✅ Актив выбран:\n\n"
            f"📊 {text}\n\n"
            f"⏱ Выберите время сделки:",
            reply_markup=times()
        )

        return


    # Выбрали время
    if text in [
        "30 секунд",
        "1 минута",
        "3 минуты",
        "5 минут",
        "15 минут"
    ]:

        context.user_data["time"] = text
        context.user_data["page"] = "selected"

        asset = context.user_data.get(
            "asset",
            "не выбран"
        )

        await update.message.reply_text(
            f"✅ Настройки сохранены!\n\n"
            f"📊 Актив: {asset}\n"
            f"⏱ Время: {text}\n\n"
            f"📊 Можно получать сигнал.",
            reply_markup=menu([
                ["📊 Получить сигнал"],
                ["📂 Изменить актив"],
                ["⏱ Изменить время"],
                ["⬅️ Назад"],
                ["🏠 Главное меню"]
            ])
        )

        return


    # Время сделки из главного меню
    if text == "⏱ Время сделки" or text == "⏱ Изменить время":

        context.user_data["page"] = "time"

        await update.message.reply_text(
            "⏱ Выберите время:",
            reply_markup=times()
        )

        return


    # Получить сигнал
    if text == "📊 Получить сигнал":

        asset = context.user_data.get(
            "asset",
            "не выбран"
        )

        trade_time = context.user_data.get(
            "time",
            "не выбрано"
        )

        await update.message.reply_text(
            f"📊 Параметры:\n\n"
            f"📊 Актив: {asset}\n"
            f"⏱ Время: {trade_time}\n\n"
            f"⏳ Анализ рынка...\n\n"
            f"⚠️ Реальный сигнал пока не подключён."
        )

        return


    # Настройки
    if text == "⚙️ Настройки":

        asset = context.user_data.get(
            "asset",
            "не выбран"
        )

        trade_time = context.user_data.get(
            "time",
            "не выбрано"
        )

        context.user_data["page"] = "settings"

        await update.message.reply_text(
            f"⚙️ Настройки\n\n"
            f"📊 Актив: {asset}\n"
            f"⏱ Время: {trade_time}",
            reply_markup=menu([
                ["📂 Изменить актив"],
                ["⏱ Изменить время"],
                ["⬅️ Назад"],
                ["🏠 Главное меню"]
            ])
        )

        return


    # История
    if text == "📜 История":

        await update.message.reply_text(
            "📜 История сигналов пока пустая.",
            reply_markup=menu([
                ["⬅️ Назад"],
                ["🏠 Главное меню"]
            ])
        )

        return


    # =========================
    # НАЗАД
    # =========================

    if text == "⬅️ Назад":

        # Если были на выборе времени
        if page == "time":

            previous = context.user_data.get(
                "previous_page",
                "categories"
            )

            if previous == "forex":

                context.user_data["page"] = "forex"

                await update.message.reply_text(
                    "💱 Выберите валютную пару:",
                    reply_markup=forex()
                )

            elif previous == "crypto":

                context.user_data["page"] = "crypto"

                await update.message.reply_text(
                    "₿ Выберите криптовалюту:",
                    reply_markup=crypto()
                )

            elif previous == "commodities":

                context.user_data["page"] = "commodities"

                await update.message.reply_text(
                    "🥇 Выберите сырьевой товар:",
                    reply_markup=commodities()
                )

            elif previous == "stocks":

                context.user_data["page"] = "stocks"

                await update.message.reply_text(
                    "🏢 Выберите акцию:",
                    reply_markup=stocks()
                )

            elif previous == "indexes":

                context.user_data["page"] = "indexes"

                await update.message.reply_text(
                    "📈 Выберите индекс:",
                    reply_markup=indexes()
                )

            else:

                context.user_data["page"] = "categories"

                await update.message.reply_text(
                    "📂 Выберите раздел:",
                    reply_markup=categories()
                )

            return


        # После выбора времени
        if page == "selected":

            previous = context.user_data.get(
                "previous_page",
                "forex"
            )

            context.user_data["page"] = "time"

            await update.message.reply_text(
                "⏱ Выберите время:",
                reply_markup=times()
            )

            return


        # Валюты → категории
        if page == "forex":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        # Криптовалюты → категории
        if page == "crypto":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        # Сырьё → категории
        if page == "commodities":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        # Акции → категории
        if page == "stocks":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        # Индексы → категории
        if page == "indexes":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        # Категории → главное меню
        if page == "categories":

            context.user_data["page"] = "main"

            await update.message.reply_text(
                "🏠 Главное меню",
                reply_markup=main_menu()
            )

            return


        # В остальных случаях
        context.user_data["page"] = "main"

        await update.message.reply_text(
            "🏠 Главное меню",
            reply_markup=main_menu()
        )

        return


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
