from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Put your bot token here
TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"

# Define buttons - one per line
keyboard = [
    ["موعد المكافأة"],
    ["أرقام التواصل"],
    ["الأسئلة الشائعة"],
    ["منظومة الجامعة"],
    ["البلاك بورد"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا بك في البوت الجامعي!\nاختر من الأزرار التالية:",
        reply_markup=reply_markup
    )

# Button handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "موعد المكافأة":
        await update.message.reply_text("موعد صرف المكافأة: 26/05/2025\nالمتبقي: 10 أيام")
    
    elif text == "أرقام التواصل":
        await update.message.reply_text("للتواصل مع الجامعة:\nالهاتف: 920000000\nالبريد الإلكتروني: info@tu.edu.sa")
    
    elif text == "الأسئلة الشائعة":
        await update.message.reply_text("الأسئلة الشائعة:\n1. كيف أسجل المواد؟\n2. كيف أستعيد كلمة المرور؟\n3. كيف أستخدم البلاك بورد؟")
    
    elif text == "منظومة الجامعة":
        await update.message.reply_text("رابط منظومة الجامعة: https://edugate.tu.edu.sa")

    elif text == "البلاك بورد":
        await update.message.reply_text("رابط البلاك بورد: https://lms.tu.edu.sa")

    else:
        await update.message.reply_text("الرجاء اختيار خيار من الأزرار فقط.")

# Launch bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("The bot is running...")
    app.run_polling()
