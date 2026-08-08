import os
import requests

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


TOKEN = os.getenv("BOT_TOKEN")
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")


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


# ==========================================
# ПОЛУЧЕНИЕ РЕАЛЬНОЙ ЦЕНЫ
# ==========================================

def get_price(symbol):

    url = "https://api.twelvedata.com/price"

    params = {
        "symbol": symbol,
        "apikey": TWELVE_DATA_API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        if "price" in data:

            return data["price"]

        return None

    except Exception as error:

        print("Ошибка получения цены:", error)

        return None


# ==========================================
# ПРЕОБРАЗОВАНИЕ НАЗВАНИЙ
# ==========================================

def convert_symbol(asset):

    symbols = {

        "EUR/USD": "EUR/USD",
        "GBP/USD": "GBP/USD",
        "USD/JPY": "USD/JPY",
        "AUD/USD": "AUD/USD",
        "USD/CAD": "USD/CAD",
        "USD/CHF": "USD/CHF",

        "BTC/USDT": "BTC/USD",
        "ETH/USDT": "ETH/USD",
        "BNB/USDT": "BNB/USD",
        "SOL/USDT": "SOL/USD",
        "XRP/USDT": "XRP/USD",
        "ADA/USDT": "ADA/USD",
        "DOGE/USDT": "DOGE/USD",

        "🥇 Gold XAU/USD": "XAU/USD",
        "🥈 Silver XAG/USD": "XAG/USD",

        "Apple": "AAPL",
        "Tesla": "TSLA",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL",
        "NVIDIA": "NVDA",
        "Meta": "META",

        "NASDAQ": "IXIC",
        "S&P 500": "SPX",
        "Dow Jones": "DJI",
        "DAX": "DAX",
        "FTSE 100": "FTSE",
        "Nikkei 225": "NI225"
    }

    return symbols.get(asset)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    context.user_data["page"] = "main"

    await update.message.reply_text(
        "🤖 Pocket Signal Bot\n\n"
        "🏠 Главное меню",
        reply_markup=main_menu()
    )


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    page = context.user_data.get(
        "page",
        "main"
    )


    # ==========================================
    # ГЛАВНОЕ МЕНЮ
    # ==========================================

    if text == "🏠 Главное меню":

        context.user_data["page"] = "main"

        await update.message.reply_text(
            "🏠 Главное меню",
            reply_markup=main_menu()
        )

        return


    # ==========================================
    # ВЫБОР АКТИВА
    # ==========================================

    if text == "📂 Выбрать актив" or text == "📂 Изменить актив":

        context.user_data["page"] = "categories"

        await update.message.reply_text(
            "📂 Выберите раздел:",
            reply_markup=categories()
        )

        return


    # ==========================================
    # ВАЛЮТЫ
    # ==========================================

    if text == "💱 Валюты":

        context.user_data["page"] = "forex"

        await update.message.reply_text(
            "💱 Выберите валютную пару:",
            reply_markup=forex()
        )

        return


    # ==========================================
    # КРИПТО
    # ==========================================

    if text == "₿ Криптовалюты":

        context.user_data["page"] = "crypto"

        await update.message.reply_text(
            "₿ Выберите криптовалюту:",
            reply_markup=crypto()
        )

        return


    # ==========================================
    # СЫРЬЕ
    # ==========================================

    if text == "🥇 Сырьевые товары":

        context.user_data["page"] = "commodities"

        await update.message.reply_text(
            "🥇 Выберите сырьевой товар:",
            reply_markup=commodities()
        )

        return


    # ==========================================
    # АКЦИИ
    # ==========================================

    if text == "🏢 Акции":

        context.user_data["page"] = "stocks"

        await update.message.reply_text(
            "🏢 Выберите акцию:",
            reply_markup=stocks()
        )

        return


    # ==========================================
    # ИНДЕКСЫ
    # ==========================================

    if text == "📈 Индексы":

        context.user_data["page"] = "indexes"

        await update.message.reply_text(
            "📈 Выберите индекс:",
            reply_markup=indexes()
        )

        return


    # ==========================================
    # АКТИВЫ
    # ==========================================

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
            reply_markup=times()
        )

        return


    # ==========================================
    # ВРЕМЯ
    # ==========================================

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


    # ==========================================
    # РЕАЛЬНАЯ ЦЕНА
    # ==========================================

    if text == "📊 Получить сигнал":

        asset = context.user_data.get(
            "asset"
        )

        trade_time = context.user_data.get(
            "time"
        )

        if not asset:

            await update.message.reply_text(
                "⚠️ Сначала выберите актив."
            )

            return

        symbol = convert_symbol(asset)

        if not symbol:

            await update.message.reply_text(
                "⚠️ Для этого актива пока нет подключения к котировкам."
            )

            return

        await update.message.reply_text(
            f"⏳ Получаю реальные данные...\n\n"
            f"📊 {asset}"
        )

        price = get_price(symbol)

        if price:

            await update.message.reply_text(
                f"📊 РЫНОЧНЫЕ ДАННЫЕ\n\n"
                f"Актив: {asset}\n"
                f"⏱ Время: {trade_time}\n\n"
                f"💰 Текущая цена:\n"
                f"{price}\n\n"
                f"✅ Данные получены успешно.\n\n"
                f"🔧 Следующий этап — анализ рынка."
            )

        else:

            await update.message.reply_text(
                "❌ Не удалось получить цену.\n\n"
                "Проверим API-ключ и доступность инструмента."
            )

        return


    # ==========================================
    # НАСТРОЙКИ
    # ==========================================

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


    # ==========================================
    # ИСТОРИЯ
    # ==========================================

    if text == "📜 История":

        await update.message.reply_text(
            "📜 История сигналов пока пустая.",
            reply_markup=menu([
                ["⬅️ Назад"],
                ["🏠 Главное меню"]
            ])
        )

        return


    # ==========================================
    # НАЗАД
    # ==========================================

    if text == "⬅️ Назад":

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


        if page == "selected":

            context.user_data["page"] = "time"

            await update.message.reply_text(
                "⏱ Выберите время:",
                reply_markup=times()
            )

            return


        if page == "forex":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        if page == "crypto":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        if page == "commodities":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        if page == "stocks":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        if page == "indexes":

            context.user_data["page"] = "categories"

            await update.message.reply_text(
                "📂 Выберите раздел:",
                reply_markup=categories()
            )

            return


        if page == "categories":

            context.user_data["page"] = "main"

            await update.message.reply_text(
                "🏠 Главное меню",
                reply_markup=main_menu()
            )

            return


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
