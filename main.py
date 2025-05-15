from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"

# === الأسئلة الشائعة ===
faq_data = {
    "ما هي طريقة احتساب المعدل؟": "يتم احتساب المعدل بجمع النقاط وقسمتها على عدد الساعات.",
    "كيف أقدم اعتذار عن الترم؟": "من خلال بوابة الطالب - الخدمات الأكاديمية.",
    "هل يوجد فصل صيفي؟": "نعم، حسب إعلان الجامعة.",
}

# === الوظائف ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("موعد المكافأة", callback_data="mokafa")],
        [InlineKeyboardButton("أرقام التواصل", callback_data="contact")],
        [InlineKeyboardButton("الأسئلة الشائعة", callback_data="faq")],
        [InlineKeyboardButton("تقييم الدكاترة", url="https://t.me/tudoctors")],
        [InlineKeyboardButton("منظومة الجامعة", url="https://edugate.tu.edu.sa/")],
        [InlineKeyboardButton("رابط البلاك بورد", url="https://lms.tu.edu.sa/")],
        [InlineKeyboardButton("موقع الجامعة للطلاب", url="https://maps.app.goo.gl/SJ2vYZt9wiqQYkx89")],
        [InlineKeyboardButton("موقع الجامعة للطالبات", url="https://maps.app.goo.gl/BPwmcoQ7T16CT2FX8")],
        [InlineKeyboardButton("حفل التخرج", callback_data="graduation")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحباً بك، اختر أحد الخيارات:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "mokafa":
        await query.edit_message_text("موعد صرف المكافأة: 26/05/2025\nالمتبقي: 10 أيام", reply_markup=back_button())
    elif data == "contact":
        await query.edit_message_text("للتواصل مع الجامعة:\nالهاتف: 920002122", reply_markup=back_button())
    elif data == "graduation":
        photo_url = "https://raw.githubusercontent.com/omar-7077/unibot/main/graduation.jpg"
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url)
    elif data == "faq":
        keyboard = [[InlineKeyboardButton(q, callback_data=f"faq_{i}")] for i, q in enumerate(faq_data)]
        keyboard.append([InlineKeyboardButton("رجوع", callback_data="back")])
        await query.edit_message_text("اختر سؤالًا:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data.startswith("faq_"):
        index = int(data.split("_")[1])
        question = list(faq_data.keys())[index]
        answer = faq_data[question]
        await query.edit_message_text(f"{question}\n\n{answer}", reply_markup=back_button())
    elif data == "back":
        await start(update, context)

def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back")]])

# === التشغيل ===
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()

if __name__ == "__main__":
    main()
