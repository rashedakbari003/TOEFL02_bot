from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from textblob import TextBlob
import os

# توکن و Admin ID از Environment Variables
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# لیست KEYWORDS که تو داده بودی
KEYWORDS = [
    "نارضایتی", "استاد", "کورس", "ضعیف", "مشکل", 
    "کیفیت پایین", "تاخیر", "عدم یادگیری", "اشتباه", "کند",
    "آکادمی تافل بدرد نمیخوره", "استاد ما یاد نداره", "ضعیف هست",
    "اداره اخلاق نداره", "مدیریت ضعیف هست", "صنف ما خراب هست",
    "ما امروز نمیاییم همه ما", "ما رخصتی میخواهیم",
    "ترک", "بیرون", "عوض", "رخصت", "قوی", "آرام"
]

def monitor(update: Update, context: CallbackContext):
    text = update.message.text
    
    # بررسی KEYWORDS
    keyword_found = any(word in text for word in KEYWORDS)
    
    # تحلیل احساسات با TextBlob
    analysis = TextBlob(text)
    negative_sentiment = analysis.sentiment.polarity < 0  # منفی
    
    # اگر یکی از دو حالت درست بود، پیام را به ادمین گزارش بده
    if keyword_found or negative_sentiment:
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"پیام منفی یا کلیدی شناسایی شد:\n{text}\nاز گروه: {update.message.chat.title}"
        )

# راه‌اندازی ربات
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), monitor))

updater.start_polling()
updater.idle()
