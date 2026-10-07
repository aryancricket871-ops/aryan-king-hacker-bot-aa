#!/usr/bin/env python3
# OSINT Number Info Bot — Telegram
# API: geniushacker.vercel.app
# Developed by Aryan 

import requests
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

BOT_TOKEN = "8913474132:AAHErPxzvyDLRhciyZEsR0DtzDdy1ewRWdQ"
API_BASE = "https://geniushacker.vercel.app/api/number/ADITYA-D2-FREE-51DOJ55R"


def get_number_info(number):
    try:
        url = f"{API_BASE}?number={number}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return data
        return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None


def clean_data(data):
    """Remove unwanted fields like developer, youtube, credit."""
    if not data:
        return data

    unwanted_keys = ['developer', 'youtube', 'credit', 'telegram', 'channel', 'api_info']
    for key in unwanted_keys:
        if key in data:
            del data[key]

    # Per-record unwanted fields
    if 'data' in data and isinstance(data['data'], dict):
        unwanted_record_keys = ['id', 'alt_number']
        for key in unwanted_record_keys:
            if key in data['data']:
                del data['data'][key]

    return data


async def start(update, context):
    await update.message.reply_text(
        "OSINT NUMBER INFO BOT\n\n"
        "Send 10-digit mobile number to get JSON data.\n\n"
        "Example: 9876543210\n\n"
        "Developed by aryan "
    )


async def handle_number(update, context):
    number = update.message.text.strip()

    if not number.isdigit() or len(number) != 10:
        await update.message.reply_text("Send exactly 10 digits.")
        return

    msg = await update.message.reply_text("Searching...")
    data = get_number_info(number)

    if data:
        clean_data(data)
        result = json.dumps(data, indent=2, ensure_ascii=False)

        if len(result) > 4000:
            result = result[:4000] + "\n... (truncated)"

        await msg.edit_text(f"<b>JSON</b>\n<pre>{result}</pre>", parse_mode='HTML')
    else:
        await msg.edit_text("No data found.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    print("OSINT Number Info Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()