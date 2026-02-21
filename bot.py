from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import os

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

keywords = ["ترک", "انصراف", "راضی نیستم", "مشکل داریم", "بی فایده", "استاد خراب"]

group_stats = {}

async def monitor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text
        group_name = update.effective_chat.title
        user = update.effective_user.full_name

        if group_name not in group_stats:
            group_stats[group_name] = {"negative": 0, "leave": 0}

        for word in keywords:
            if word in text:
                group_stats[group_name]["negative"] += 1
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"⚠️ پیام منفی در {group_name}\nکاربر: {user}\nپیام:\n{text}"
                )
                break

async def member_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.left_chat_member:
        group_name = update.effective_chat.title
        user = update.message.left_chat_member.full_name

        if group_name not in group_stats:
            group_stats[group_name] = {"negative": 0, "leave": 0}

        group_stats[group_name]["leave"] += 1
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🚪 {user} گروه {group_name} را ترک کرد."
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, monitor))
app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, member_left))

app.run_polling()
