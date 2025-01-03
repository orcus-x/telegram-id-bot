from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
BOT_TOKEN = '7862840031:AAHjXIKRXrNv7FKBs8f6wQKVDdzlSBA9Zlw'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"Hi {user.first_name}! 👋\n\n"
        "I'm an ID Bot. I can help you get various Telegram IDs.\n"
        "Here are my commands:\n"
        "/id - Get your user ID\n"
        "/chatid - Get the current chat ID\n"
        "/info - Get detailed information about yourself"
    )
    await update.message.reply_text(welcome_message)

async def get_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send user their Telegram ID."""
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your Telegram ID is: `{user_id}`", parse_mode='Markdown')

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the current chat ID."""
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Current chat ID is: `{chat_id}`", parse_mode='Markdown')

async def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send detailed information about the user."""
    user = update.effective_user
    chat = update.effective_chat
    
    # Compile user information
    info = [
        f"👤 *User Information*",
        f"• ID: `{user.id}`",
        f"• First Name: {user.first_name}",
        f"• Last Name: {user.last_name if user.last_name else 'Not set'}",
        f"• Username: @{user.username if user.username else 'Not set'}",
        f"• Language: {user.language_code if user.language_code else 'Not set'}",
        f"\n💬 *Chat Information*",
        f"• Chat ID: `{chat.id}`",
        f"• Chat Type: {chat.type}",
        f"• Chat Title: {chat.title if chat.title else 'Not available in private chat'}"
    ]
    
    await update.message.reply_text("\n".join(info), parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("id", get_user_id))
    application.add_handler(CommandHandler("chatid", get_chat_id))
    application.add_handler(CommandHandler("info", get_user_info))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()