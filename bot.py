import time
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import feedparser

TOKEN = os.environ.get("BOT_TOKEN")

def get_news(category):
    feeds = {
        "sports": "https://www.espn.com/espn/rss/news",
        "tech": "https://feeds.arstechnica.com/arstechnica/index",
        "politics": "https://rss.cnn.com/rss/cnn_allpolitics.rss"
    }
    try:
        feed = feedparser.parse(feeds[category])
        text = ""
        for entry in feed.entries[:5]:
            text += f"📰 {entry.title}\n{entry.link}\n\n"
        return text
    except Exception as e:
        return f"خطا در دریافت خبر: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚽ ورزشی", callback_data="sports")],
        [InlineKeyboardButton("🏛 سیاسی", callback_data="politics")],
        [InlineKeyboardButton("💻 تکنولوژی", callback_data="tech")]
    ]
    await update.message.reply_text("دسته خبر رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    news = get_news(query.data)
    await query.edit_message_text(news)

try:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
except Exception as e:
    print("Crash:", e)
    time.sleep(10)  # جلوگیری از exit سریع برای Railway
