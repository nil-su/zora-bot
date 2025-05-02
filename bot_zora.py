import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = 'YourBOTAPI'
COVALENT_API_KEY = 'YOURCOVALENTAPI'

ZORA_CONTRACT = "0x1111111111166b7FE7bd91427724B487980aFc69"
CHAIN_ID = "8453"  # Base Mainnet

async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan: /cek <alamat_wallet>")
        return

    address = context.args[0]
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{address}/balances_v2/?key={COVALENT_API_KEY}"

    response = requests.get(url)
    if response.status_code != 200:
        await update.message.reply_text("Gagal mengambil data token.")
        return

    data = response.json()
    tokens = data.get("data", {}).get("items", [])

    zora = next((t for t in tokens if t["contract_address"].lower() == ZORA_CONTRACT.lower()), None)
    if zora:
        balance = int(zora["balance"]) / (10 ** 18)
        await update.message.reply_text(f"Wallet {address} memiliki {balance:.4f} ZORA.")
    else:
        await update.message.reply_text(f"Tidak ada token ZORA di wallet {address}.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("cek", cek))
    app.run_polling()
