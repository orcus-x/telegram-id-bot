from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import logging
import sys

# Configure more detailed logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,  # Changed to DEBUG level to see more detailed logs
    handlers=[
        logging.StreamHandler(sys.stdout)  # Explicitly log to stdout
    ]
)

# Get the root logger to ensure all logs are captured
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Set httpx logging to INFO to reduce noise
logging.getLogger("httpx").setLevel(logging.INFO)

# Replace with your bot token
BOT_TOKEN = '7826696571:AAG5Se4B8zUd1DpCF3AtqgwZw09lAh4E9LA'

# ----- Regular Chat Commands -----

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued in regular chats."""
    if not update.message:
        return
    
    user = update.effective_user
    chat = update.effective_chat
    
    welcome_message = (
        f"Hi {user.first_name if user else 'there'}! 👋\n\n"
        "I'm an ID Bot. I can help you get various Telegram IDs.\n"
        "Here are my commands:\n"
        "/id - Get your user ID\n"
        "/chatid - Get the current chat ID\n"
        "/info - Get detailed information about this chat"
    )
    await update.message.reply_text(welcome_message)
    
    logger.debug(f"START command used in {chat.type} {chat.id} by user {user.id if user else 'unknown'}")

async def get_user_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send user their Telegram ID in regular chats."""
    if not update.message:
        return
    
    user = update.effective_user
    chat = update.effective_chat
    
    await update.message.reply_text(f"Your Telegram ID is: `{user.id}`", parse_mode='Markdown')
    logger.debug(f"ID command: User {user.id} requested their ID in {chat.type} {chat.id}")

async def get_chat_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the current chat ID in regular chats."""
    if not update.message:
        return
    
    user = update.effective_user
    chat = update.effective_chat
    
    await update.message.reply_text(f"Current chat ID is: `{chat.id}`", parse_mode='Markdown')
    logger.debug(f"CHATID command: Chat ID {chat.id} ({chat.type}) requested by user {user.id}")

async def get_info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send detailed information in regular chats."""
    if not update.message:
        return
    
    user = update.effective_user
    chat = update.effective_chat
    message = update.message
    
    try:
        # For private chats, groups, and supergroups
        info = [
            "👤 <b>User Information</b>",
            f"• ID: <code>{user.id}</code>",
            f"• First Name: {user.first_name}",
            f"• Last Name: {user.last_name if user.last_name else 'Not set'}"
        ]
        
        # Handle username
        if user.username:
            info.append(f"• Username: @{user.username}")
        else:
            info.append("• Username: Not set")
            
        info.append(f"• Language: {user.language_code if user.language_code else 'Not set'}")
        
        # Add chat information
        info.extend([
            "",
            "💬 <b>Chat Information</b>",
            f"• Chat ID: <code>{chat.id}</code>",
            f"• Chat Type: {chat.type}"
        ])
        
        if chat.type != "private":
            info.append(f"• Chat Title: {chat.title if chat.title else 'Not available'}")
        
        # Add message information
        info.extend([
            "",
            "📝 <b>Message Information</b>",
            f"• Message ID: <code>{message.message_id}</code>",
            f"• Date: {message.date}"
        ])
        
        # Join with newlines and send with HTML formatting
        await message.reply_text("\n".join(info), parse_mode='HTML')
        logger.debug(f"INFO command: Data requested in {chat.type} {chat.id} by user {user.id}")
        
    except Exception as e:
        # Log error and provide a simpler fallback
        logger.error(f"Error sending info: {str(e)}", exc_info=True)
        await message.reply_text("⚠️ Error retrieving information. Please try <code>/chatid</code> or <code>/id</code> instead.", parse_mode='HTML')
        logger.debug(f"INFO command: Error occurred in {chat.type} {chat.id}")

# ----- Channel Post Handlers -----

async def channel_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all commands in channels."""
    if not update.channel_post or not update.effective_chat:
        return
    
    message = update.channel_post
    chat = update.effective_chat
    command_text = message.text.split()[0].lower() if message.text else ""
    
    # Log the received channel command
    logger.debug(f"Received channel command: {command_text} in channel {chat.id}")
    
    try:
        if '/start' in command_text:
            # Handle /start in channel
            welcome_message = (
                "👋 Hi there!\n\n"
                "I'm an ID Bot. I can help you get various Telegram IDs.\n\n"
                "📋 Available commands for channels:\n\n"
                "💬 <code>/chatid</code> - Get the current channel ID\n"
                "ℹ️ <code>/info</code> - Get detailed information about this channel"
            )
            await message.reply_text(welcome_message, parse_mode='HTML')
            logger.debug(f"START command processed in channel {chat.id}")
            
        elif '/id' in command_text:
            # Handle /id in channel (limited functionality)
            await message.reply_text("⚠️ User IDs cannot be retrieved in channels. Try using <code>/chatid</code> instead.", parse_mode='HTML')
            logger.debug(f"ID command processed in channel {chat.id} - notified about limitations")
            
        elif '/chatid' in command_text:
            # Handle /chatid in channel
            await message.reply_text(f"📢 Channel ID: <code>{chat.id}</code>", parse_mode='HTML')
            logger.debug(f"CHATID command processed in channel {chat.id}")
            
        elif '/info' in command_text:
            # Handle /info in channel
            try:
                # Use HTML format for more reliable formatting and clickable commands
                info = [
                    "📢 <b>Channel Information</b>",
                    f"• Channel ID: <code>{chat.id}</code>",
                    f"• Channel Type: {chat.type}",
                    f"• Channel Title: {chat.title if chat.title else 'Not available'}",
                    "",
                    "📝 <b>Message Information</b>",
                    f"• Message ID: <code>{message.message_id}</code>",
                    f"• Date: {message.date}"
                ]
                await message.reply_text("\n".join(info), parse_mode='HTML')
                logger.debug(f"INFO command processed in channel {chat.id}")
            except Exception as e:
                logger.error(f"Error sending channel info: {str(e)}", exc_info=True)
                await message.reply_text(f"⚠️ Error displaying info. You can try <code>/chatid</code> instead.", parse_mode='HTML')
    
    except Exception as e:
        logger.error(f"Error processing channel command {command_text}: {str(e)}", exc_info=True)
        try:
            await message.reply_text(f"Error processing command: {str(e)}")
        except:
            logger.error("Could not send error message to channel")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.error(f'Update "{update}" caused error "{context.error}"', exc_info=True)

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add regular command handlers (for private chats, groups, etc.)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("id", get_user_id_command))
    application.add_handler(CommandHandler("chatid", get_chat_id_command))
    application.add_handler(CommandHandler("info", get_info_command))
    
    # Add special handler for ALL channel posts with commands
    application.add_handler(MessageHandler(
        filters.ChatType.CHANNEL & filters.COMMAND,
        channel_command_handler
    ))

    # Add error handler
    application.add_error_handler(error_handler)

    # Log that the bot is starting
    logger.info("===== ID Bot started. Listening for commands... =====")

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()