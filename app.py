import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from utils.youtube import search_youtube, download_youtube_video
from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send /search <query> or /download <YouTube_URL>")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        return await update.message.reply_text("Please provide a search query.")
    
    results = search_youtube(query)
    keyboard = [[InlineKeyboardButton(res['title'], url=res['url'])] for res in results]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Top 20 search results:", reply_markup=reply_markup)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = ' '.join(context.args)
    if not url:
        return await update.message.reply_text("Please provide a YouTube URL.")
    
    video_path = download_youtube_video(url, '1080p')
    with open(video_path, 'rb') as f:
        await update.message.reply_video(video=f)

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("download", download))

if __name__ == "__main__":
    app.run_polling()