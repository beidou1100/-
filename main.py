import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import openai
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("提问", callback_data='ask')],
        [InlineKeyboardButton("帮助", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = "🎉 欢迎使用AI智能助手，点击按钮开始提问！"
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'ask':
        await query.message.reply_text("请直接输入你的问题，我会帮你回答。")
    elif data == 'help':
        await query.message.reply_text("直接输入问题，机器人会基于 OpenAI GPT-3.5 帮你回答。")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_context:
        user_context[user_id] = []

    user_context[user_id].append({"role": "user", "content": text})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=user_context[user_id],
            temperature=0.7,
            max_tokens=1500
        )
        answer = response['choices'][0]['message']['content'].strip()
        user_context[user_id].append({"role": "assistant", "content": answer})

        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"出错了：{e}")

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
