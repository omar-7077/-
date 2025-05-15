from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import datetime

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"  # استبدل هذا بالتوكن الخاص بك

# القوائم الرئيسية والفرعية
main_menu = [["موعد المكافأة", "أرقام التواصل"],
             ["الأسئلة الشائعة", "تقييم الدكاترة"],
             ["منظومة الجامعة", "البلاك بورد"],
             ["موقع الطلاب", "موقع الطالبات"],
             ["حفل التخرج"]]

faq_menu = [["كيف أسجل المواد؟"],
            ["كيف أستعيد كلمة المرور؟"],
            ["كيف أستخدم البلاك بورد؟"],
            ["رجوع"]]

reply_main = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
reply_faq = ReplyKeyboardMarkup(faq_menu, resize_keyboard=True)

# دالة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك في البوت الجامعي!\nاختر من الأزرار:", reply_markup=reply_main)

# دالة التعامل مع الرسائل
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "موعد المكافأة":
        today = datetime.datetime.today()
        bonus_day = datetime.datetime(today.year, today.month, 26)
        if today.day > 26:
            if today.month == 12:
                bonus_day = datetime.datetime(today.year + 1, 1, 26)
            else:
                bonus_day = datetime.datetime(today.year, today.month + 1, 26)
        remaining_days = (bonus_day - today).days
        formatted_date = bonus_day.strftime('%d/%m/%Y')
        await update.message.reply_text(f"موعد صرف المكافأة: {formatted_date}\nالمتبقي: {remaining_days} يوم")

    elif msg == "أرقام التواصل":
        await update.message.reply_text("رقم الجامعة: 920002122")
    
    elif msg == "تقييم الدكاترة":
        await update.message.reply_text("رابط تقييم الدكاترة:\nhttps://t.me/tudoctors")
    
    elif msg == "منظومة الجامعة":
        await update.message.reply_text("رابط منظومة الجامعة:\nhttps://edugate.tu.edu.sa")
    
    elif msg == "البلاك بورد":
        await update.message.reply_text("رابط البلاك بورد:\nhttps://lms.tu.edu.sa")
    
    elif msg == "موقع الطلاب":
        await update.message.reply_text("موقع الجامعة للطلاب:\nhttps://maps.app.goo.gl/SJ2vYZt9wiqQYkx89")
    
    elif msg == "موقع الطالبات":
        await update.message.reply_text("موقع الجامعة للطالبات:\nhttps://maps.app.goo.gl/BPwmcoQ7T16CT2FX8")
    
    elif msg == "حفل التخرج":
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo="https://www2.0zz0.com/2025/05/15/07/864959598.jpeg",
            caption="صورة حفل التخرج"
        )
    
    elif msg == "الأسئلة الشائعة":
        await update.message.reply_text("اختر سؤالاً:", reply_markup=reply_faq)
    
    elif msg == "كيف أسجل المواد؟":
        await update.message.reply_text("من خلال بوابة الطالب ثم تسجيل المقررات.", reply_markup=reply_faq)
    
    elif msg == "كيف أستعيد كلمة المرور؟":
        await update.message.reply_text("عبر خيار (نسيت كلمة المرور) في بوابة الدخول.", reply_markup=reply_faq)
    
    elif msg == "كيف أستخدم البلاك بورد؟":
        await update.message.reply_text("سجّل دخولك عبر https://lms.tu.edu.sa ثم اختر المقررات.", reply_markup=reply_faq)
    
    elif msg == "رجوع":
        await update.message.reply_text("عدنا للقائمة الرئيسية:", reply_markup=reply_main)
    
    else:
        await update.message.reply_text("يرجى اختيار زر من القائمة.", reply_markup=reply_main)

# تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()
