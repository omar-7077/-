from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# التوكن الخاص بك
TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"

# إنشاء الأزرار
def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("موعد المكافأة", callback_data="mokafa")],
        [InlineKeyboardButton("أرقام التواصل", callback_data="contact")],
        [InlineKeyboardButton("الأسئلة الشائعة", callback_data="faq")],
        [InlineKeyboardButton("منظومة الجامعة", callback_data="edugate")],
        [InlineKeyboardButton("رابط البلاك بورد", callback_data="blackboard")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("مرحباً بك في البوت الجامعي! اختر ما تريد:", reply_markup=reply_markup)

# الردود عند الضغط على الأزرار
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "mokafa":
        await query.edit_message_text("موعد صرف المكافأة: 26/05/2025\nالمتبقي: 10 أيام")
    elif query.data == "contact":
        await query.edit_message_text("للتواصل مع الجامعة:\nالهاتف: 920000000\nالبريد: info@tu.edu.sa")
    elif query.data == "faq":
        await query.edit_message_text("الأسئلة الشائعة:\n- كيف أعدل جدولي؟\n- متى تبدأ الاختبارات؟")
    elif query.data == "edugate":
        await query.edit_message_text("رابط منظومة الجامعة:\nhttps://edugate.tu.edu.sa")
    elif query.data == "blackboard":
        await query.edit_message_text("رابط البلاك بورد:\nhttps://lms.tu.edu.sa")

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.run_polling()

if __name__ == "__main__":
    main()
