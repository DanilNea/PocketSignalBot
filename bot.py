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


def asset_categories_menu():
    return show_menu([
        ["💱 Валюты"],
        ["₿ Криптовалюты"],
        ["🥇 Сырьевые товары"],
        ["🏢 Акции"],
        ["📈 Индексы"],
        ["⬅️ Назад"]
    ])


def forex_menu():
    return show_menu([
        ["EUR/USD"],
        ["GBP/USD"],
        ["USD/JPY"],
        ["AUD/USD"],
        ["USD/CAD"],
        ["USD/CHF"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


def crypto_menu():
    return show_menu([
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


def commodities_menu():
    return show_menu([
        ["🥇 Gold XAU/USD"],
        ["🥈 Silver XAG/USD"],
        ["🛢 Oil WTI"],
        ["🛢 Oil Brent"],
        ["🔥 Natural Gas"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


def stocks_menu():
    return show_menu([
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


def indexes_menu():
    return show_menu([
        ["NASDAQ"],
        ["S&P 500"],
        ["Dow Jones"],
        ["DAX"],
        ["FTSE 100"],
        ["Nikkei 225"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
    ])


def time_menu():
    return show_menu([
        ["30 секунд"],
        ["1 минута"],
        ["3 минуты"],
        ["5 минут"],
        ["15 минут"],
        ["⬅️ Назад"],
        ["🏠 Главное меню"]
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
    page = context.user_data.get("page", "main")


    # =========================
    # ГЛАВНОЕ МЕНЮ
    # =========================

    if text == "🏠 Главное меню":

        context.user_data["page"] = "main"

        await update.message.reply_text(
            "🏠 Главное меню:",
            reply_markup=main_menu()
        )

        return


    # =========================
    # ВЫБОР АКТИВА
    # =========================

    if text == "📂 Выбрать актив" or text == "📂 Изменить актив":

        context.user_data["page"] = "assets"

        await update.message.reply_text(
            "📂 Выберите раздел:",
            reply_markup=asset_categories_menu()
        )

        return


    # =========================
    # ВАЛЮТЫ
    # =========================

    if text == "💱 Валюты":

        context.user_data["page"] = "forex"

        await update.message.reply_text(
            "💱 Выберите валютную пару:",
            reply_markup=forex_menu()
        )

        return


    # =========================
    # КРИПТОВАЛЮТЫ
    # =========================

    if text == "₿ Криптовалюты":

        context.user_data["page"] = "crypto"

        await update.message.reply_text(
            "₿ Выберите криптовалюту:",
            reply_markup=crypto_menu()
        )

        return


    # =========================
    # СЫРЬЕ
    # =========================

    if text == "🥇 Сырьевые товары":

        context.user_data["page"] = "commodities"

        await update.message.reply_text(
            "🥇 Выберите сырьевой товар:",
            reply_markup=commodities_menu()
        )

        return


    # =========================
    # АКЦИИ
    # =========================

    if text == "🏢 Акции":

        context.user_data["page"] = "stocks"

        await update.message.reply_text(
            "🏢 Выберите акцию:",
            reply_markup=stocks_menu()
        )

        return


    # =========================
    # ИНДЕКСЫ
    # =========================

    if text == "📈 Индексы":

        context.user_data["page"] = "indexes"

        await update.message.reply_text(
            "📈 Выберите индекс:",
            reply_markup=indexes_menu()
        )

        return


    # =========================
    # ВЫБОР АКТИВА
    # =========================

    assets = [
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
    ]

    if text in assets:

        context.user_data["asset"] = text
        context.user_data["previous_page"] = page
        context.user_data["page"] = "time"

        await update.message.reply_text(
            f"✅ Актив выбран:\n\n"
            f"📊 {text}\n\n"
            f"⏱ Выберите время сделки:",
            reply_markup=time_menu()
        )

        return


    # =========================
    # ВЫБОР ВРЕМЕНИ
    # =========================

    times = [
        "30 секунд",
        "1 минута",
        "3 минуты",
        "5 минут",
        "15 минут"
    ]

    if text in times:

        context.user_data["time"] = text

        asset = context.user_data.get(
            "asset",
            "не выбран"
        )

        context.user_data["page"] = "selected"

        await update.message.reply_text(
            f"✅ Настройки сохранены!\n\n"
            f"📊 Актив: {asset}\n"
            f"⏱ Время: {text}\n\n"
            f"📊 Теперь можно получать сигнал.",
            reply_markup=show_menu([
                ["📊 Получить сигнал"],
                ["📂 Изменить актив"],
                ["⏱ Изменить время"],
                ["⬅️ Назад"],
                ["🏠 Главное меню"]
            ])
        )

        return


    # =========================
    # ИЗМЕНИТЬ ВРЕМЯ
    # =========================

    if text == "⏱ Время сделки" or text == "⏱ Изменить время":

        context.user_data["previous_page"] = page
        context.user_data["page"] = "time"

        await update.message.reply_text(
            "⏱ Выберите время сделки:",
            reply_markup=time_menu()
        )

        return


    # =========================
    # НАСТРОЙКИ
    # =========================

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
            reply_markup=show_menu([
                ["📂 Изменить актив"],
                ["⏱ Изменить время"],
                ["⬅️ Назад"],
                ["🏠 Главное меню"]
            ])
        )

        return


    # =========================
    # ПОЛУЧИТЬ СИГНАЛ
    # =========================

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
            f"📊 Параметры сигнала:\n\n"
            f"📊 Актив: {asset}\n"
            f"⏱ Время: {trade_time}\n\n"
            f"⏳ Анализ рынка...\n\n"
            f"⚠️ Реальный сигнал пока не подключен."
        )

        return


    # =========================
    # ИСТОРИЯ
    # =========================

    if text == "📜 История":

        await update.message.reply_text(
            "📜 История сигналов пока пустая.",
            reply_markup=show_menu([
                ["⬅️ Назад"],
                ["🏠 Главное меню"]
            ])
        )

        return


    # =========================
    # НАЗАД
    # =========================

    if text == "⬅️ Назад":

        if page == "forex":
            context.user_data["page"] = "assets"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=asset_categories_menu()
            )

        elif page == "crypto":
            context.user_data["page"] = "assets"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=asset_categories_menu()
            )

        elif page == "commodities":
            context.user_data["page"] = "assets"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=asset_categories_menu()
            )

        elif page == "stocks":
            context.user_data["page"] = "assets"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=asset_categories_menu()
            )

        elif page == "indexes":
            context.user_data["page"] = "assets"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=asset_categories_menu()
            )

        elif page == "time":

            previous_page = context.user_data.get(
                "previous_page",
                "assets"
            )

            if previous_page == "forex":
                context.user_data["page"] = "forex"

                await update.message.reply_text(
                    "💱 Выберите валютную пару:",
                    reply_markup=forex_menu()
                )

            elif previous_page == "crypto":
                context.user_data["page"] = "crypto"

                await update.message.reply_text(
                    "₿ Выберите криптовалюту:",
                    reply_markup=crypto_menu()
                )

            elif previous_page == "commodities":
                context.user_data["page"] = "commodities"

                await update.message.reply_text(
                    "🥇 Выберите сырьевой товар:",
                    reply_markup=commodities_menu()
                )

            elif previous_page == "stocks":
                context.user_data["page"] = "stocks"

                await update.message.reply_text(
                    "🏢 Выберите акцию:",
                    reply_markup=stocks_menu()
                )

            elif previous_page == "indexes":
                context.user_data["page"] = "indexes"

                await update.message.reply_text(
                    "📈 Выберите индекс:",
                    reply_markup=indexes_menu()
                )

            else:
                context.user_data["page"] = "assets"

                await update.message.reply_text(
                    "📂 Выберите раздел:",
                    reply_markup=asset_categories_menu()
                )

        elif page == "assets":
            context.user_data["page"] = "main"

            await update.message.reply_text(
                "🏠 Главное меню:",
                reply_markup=main_menu()
            )

        else:
            context.user_data["page"] = "main"

            await update.message.reply_text(
                "🏠 Главное меню:",
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
