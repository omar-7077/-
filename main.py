from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"  # Replace with your real bot token

# Start command with buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Bonus Date", "Contact"],
        ["FAQ", "Edugate", "Blackboard"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Welcome to the University Bot!\nPlease choose an option:",
        reply_markup=reply_markup
    )

# Handle button presses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Bonus Date":
        await update.message.reply_text("The bonus will be issued on: 26/05/2025\nRemaining: 10 days")
    elif text == "Contact":
        await update.message.reply_text("University Contact:\nPhone: 920000000\nEmail: info@tu.edu.sa")
    elif text == "FAQ":
        await update.message.reply_text("FAQ:\n1. How to reset password?\n2. Where to see GPA?\n3. How to access Blackboard?")
    elif text == "Edugate":
        await update.message.reply_text("Edugate link:\nhttps://edugate.tu.edu.sa")
    elif text == "Blackboard":
        await update.message.reply_text("Blackboard link:\nhttps://lms.tu.edu.sa")
    else:
        await update.message.reply_text("Please choose one of the available options.")

# Main function
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
