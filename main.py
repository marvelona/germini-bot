import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = '8052447480:AAG5KRGHVNRHn4D4GnPo07vCAUd03I1r97E'


# Gemini Pro API endpoint
GEMINI_API_URL = "https://geminipro.ukefuehatwo.workers.dev/?message="

# Function to get AI response from Gemini Pro
def get_gemini_response(user_message: str) -> str:
    try:
        response = requests.get(GEMINI_API_URL + user_message)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from Gemini Pro.")
        else:
            return "Failed to reach Gemini Pro. Please try again later."
    except Exception as e:
        return f"Error fetching response: {e}"

# /start command handler
async def start_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Hello! 👋 I'm the Gemini Pro AI Chatbot made by Marv Dani. Send me a message, and I'll provide an intelligent response. "
        "You can also use /help to see available commands."
    )

# /help command handler
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Here are the commands you can use:\n"
        "/start - Start the bot and get a welcome message.\n"
        "/help - Display this help message.\n"
        "/about - Learn more about Gemini Pro AI.\n"
        "You can also just send a message, and I'll reply with an AI-generated response."
    )

# /about command handler
async def about_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Gemini Pro is an advanced AI chatbot capable of real-time intelligent conversations. "
        "It's designed to provide instant, relevant, and engaging responses."
    )

# Message handler for processing user messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    ai_response = get_gemini_response(user_message)
    await update.message.reply_text(ai_response)
    
# Error handler
async def error_handler(update: Update, context: CallbackContext) -> None:
    # Log the error and notify the user
    print(f"An error occurred: {context.error}")
    if update:
        await update.message.reply_text("Oops! Something went wrong. Please try again later.")

def main() -> None:
    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('about', about_command))

    # Message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
