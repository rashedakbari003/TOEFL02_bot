from telegram import Update, Message
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from textblob import TextBlob
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

KEYWORDS = [
    "نارضایتی", "استاد", "کورس", "ضعیف", "مشکل",
    "کیفیت پایین", "تاخیر", "عدم یادگیری", "اشتباه", "کند",
    "آکادمی تافل بدرد نمیخوره", "استاد ما یاد نداره", "ضعیف هست",
    "اداره اخلاق نداره", "مدیریت ضعیف هست", "صنف ما خراب هست",
    "ما امروز نمیاییم همه ما", "ما رخصتی میخواهیم",
    "ترک", "بیرون", "عوض", "رخصت", "قوی", "آرام"
]

def monitor(update: Update, context: CallbackContext):
    message: Message = update.message
    if not message:
        return

    text = message.text or message.caption
    if not text:
        return

    keyword_found = any(word in text for word in KEYWORDS)
    negative_sentiment = TextBlob(text).sentiment.polarity < 0

    if keyword_found or negative_sentiment:
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"پیام منفی یا کلیدی شناسایی شد:\n{text}\nاز گروه: {message.chat.title}"
        )

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.caption, monitor))

updater.start_polling()
updater.idle()
