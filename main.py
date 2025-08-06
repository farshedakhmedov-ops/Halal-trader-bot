import time
import logging
from pybit.unified_trading import HTTP
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import threading

API_KEY = 'oUMxDkey4FWWF9vu60'
API_SECRET = 'FRRo5SAHkMLDKK7huL63woGCTNOGkbKDxrkU'

TG_TOKEN = '8218238899:AAFN85RALXYURWHb2EVyQN0TkJ8A8LyhDjw'

client = HTTP(api_key=API_KEY, api_secret=API_SECRET)
trading_active = False

def get_balance():
    try:
        response = client.get_wallet_balance(accountType="UNIFIED")
        balance = response['result']['list'][0]['totalWalletBalance']
        return float(balance)
    except Exception as e:
        return f"❌ Ошибка получения баланса: {e}"

def run_trading_logic():
    while trading_active:
        print("💡 Торговая логика выполняется...")
        time.sleep(10)

def start_trading(update: Update, context: CallbackContext):
    global trading_active
    if not trading_active:
        trading_active = True
        update.message.reply_text("✅ Бот успешно запущен! Халяльная торговля активирована.")
        threading.Thread(target=run_trading_logic).start()
    else:
        update.message.reply_text("⚠️ Торговля уже запущена.")

def stop_trading(update: Update, context: CallbackContext):
    global trading_active
    trading_active = False
    update.message.reply_text("🛑 Торговля остановлена.")

def balance(update: Update, context: CallbackContext):
    bal = get_balance()
    update.message.reply_text(f"💰 Баланс: {bal} USDT")

def main():
    updater = Updater(TG_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_trading))
    dp.add_handler(CommandHandler("stop", stop_trading))
    dp.add_handler(CommandHandler("balance", balance))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
