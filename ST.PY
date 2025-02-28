import telebot
import requests

bot = telebot.TeleBot("7967454931:AAHZqzf-6aYX5j-edqVtpMoIYVEQKOr5Gvg")  

def get_crypto_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
    response = requests.get(url).json()
    price = response.get(symbol.lower(), {}).get("usd", "نامشخص")
    return price
markup = telebot.types.InlineKeyboardMarkup()
cryptos = ["bitcoin", "ethereum", "ripple", "binancecoin", "solana", "dogecoin", "cardano", "litecoin"]

buttons = [telebot.types.InlineKeyboardButton(crypto.upper(), callback_data=crypto) for crypto in cryptos]
markup.add(*buttons)

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 سلام! لطفاً یک ارز را انتخاب کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    crypto_symbol = call.data  
    price = get_crypto_price(crypto_symbol)  
    bot.send_message(call.message.chat.id, f"💸 Price {crypto_symbol.upper()}: {price} USDT")

bot.infinity_polling()
