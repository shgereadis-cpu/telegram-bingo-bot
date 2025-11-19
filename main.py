import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 🔐 የቦትህን ቶከን እዚህ አስገባ
BOT_TOKEN = "8579925909:AAH43SvslBC-cPM47DqVodYa4hI5daP2nmk" 

# ሎግግንግ ማዘጋጀት
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- 1. /start ኮማንድን የሚቆጣጠር ተግባር ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start ኮማንድ ሲመጣ የእንኳን ደህና መጣችሁ መልዕክት ይልካል።"""
    
    # የተጠቃሚውን ስም ለመውሰድ መሞከር
    user_name = update.effective_user.first_name if update.effective_user else "ውድ ተጠቃሚ"
    
    welcome_message = (
        f"ሰላም {user_name}! 👋\n\n"
        "ወደ ቦታችን እንኳን ደህና መጡ። እባክዎ መልዕክትዎን ያስቀምጡ።\n\n"
        "📩 አስተያየትዎን ወይም ጥያቄዎን በጻፉ ቁጥር መልዕክቱ በቀጥታ ወደ አስተዳዳሪው (Admin) ይደርሳል።"
    )
    
    await update.message.reply_text(welcome_message)

# --- 2. መደበኛ መልዕክቶችን የሚቆጣጠር ተግባር ---

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ከተጠቃሚው የመጣውን መልዕክት ተቀብሎ አድሚኑ በቅርቡ ምላሽ እንደሚሰጥ ይናገራል።"""
    
    text_received = update.message.text
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name if update.effective_user else "Unknown"
    
    # መልዕክቱን ወደ ኮንሶል ወይም ሌላ ቦታ መመዝገብ (አድሚኑ እንዲያይ)
    logger.info(f"New Message from {user_name} ({chat_id}): {text_received}")
    
    # ለተጠቃሚው የሚመለሰው ምላሽ
    response_message = (
        "መልዕክትዎን ተቀብለናል። ✅\n\n"
        "አስተዳዳሪው (Admin) ጥያቄዎን/አስተያየትዎን በቅርቡ አይቶ ምላሽ ይሰጥዎታል። በትዕግስት ስለጠበቁን እናመሰግናለን።"
    )
    
    await update.message.reply_text(response_message)


# --- 3. የቦቱን ማሄጃ ዋና ተግባር ---

def main_run():
    """ቦቱን ለማስኬድ ዋናውን Application ይፈጥራል።"""
    
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