import logging
import os # 👈 የደህንነትን ለማረጋገጥ አስፈላጊ!
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 🔐 BOT_TOKENን ከ Render Environment Variables ላይ ያነባል
BOT_TOKEN = os.environ.get("BOT_TOKEN") 

# ሎግግንግ ማዘጋጀት
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 1. /start ኮማንድን የሚቆጣጠር ተግባር ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start ኮማንድ ሲመጣ የእንኳን ደህና መጣችሁ መልዕክት ይልካል።"""
    
    user_name = update.effective_user.first_name if update.effective_user else "ውድ ተጠቃሚ"
    
    welcome_message = (
        f"ሰላም {user_name}! 👋\n\n"
        "ወደ ቦታችን እንኳን ደህና መጡ። እባክዎ መልዕክትዎን ያስቀምጡ።\n\n"
        "📩 አስተያየትዎን ወይም ጥያቄዎን በጻፉ ቁጥር መልዕክቱ በቀጥታ ወደ አስተዳዳሪው (Admin) ይደርሳል።"
    )
    
    await update.message.reply_text(welcome_message)

# --- 2. መደበኛ መልዕክቶችን የሚቆጣጠር ተግባር ---

async def post_init(application: ApplicationBuilder) -> None:
    """Sets up the Webhook URL when the application starts."""
    url = os.environ.get("RENDER_EXTERNAL_URL")
    if url:
        await application.bot.set_webhook(url=url)
    """ከተጠቃሚው የመጣውን መልዕክት ተቀብሎ አድሚኑ በቅርቡ ምላሽ እንደሚሰጥ ይናገራል።"""
    
    text_received = update.message.text
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name if update.effective_user else "Unknown"
    
    logger.info(f"New Message from {user_name} ({chat_id}): {text_received}")
    
    # ለተጠቃሚው የሚመለሰው ምላሽ
    response_message = (
        "መልዕክትዎን ተቀብለናል። ✅\n\n"
        "አስተዳዳሪው (Admin) ጥያቄዎን/አስተያየትዎን በቅርቡ አይቶ ምላሽ ይሰጥዎታል። በትዕግስት ስለጠበቁን እናመሰግናለን።"
    )
    
    await update.message.reply_text(response_message)


# --- 3. የቦቱን ማሄጃ ዋና ተግባር ---

def main_run():
    """Initializes and runs the bot in Webhook mode for Render."""
    
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set. Check your Render Environment Variables.")
        return
        
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers መጨመር
    application.add_handler(CommandHandler("start", start))
    
    # ኮማንድ ያልሆኑ የጽሁፍ መልዕክቶችን ብቻ እንዲቀበል
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # ቦቱን ማሄድ ይጀምራል
    logger.info("Bot Started and Polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main_run()
