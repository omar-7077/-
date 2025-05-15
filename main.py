import logging
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"
PDF_PATH = "دليل التخصصات١٤٤٦هـ.pdf"
GRAD_IMAGE_URL = "https://www2.0zz0.com/2025/05/15/07/864959598.jpeg"

logging.basicConfig(level=logging.INFO)

# حساب الأيام المتبقية للمكافأة
def get_bonus_days_remaining():
    today = datetime.datetime.now()
    bonus_day = 26
    if today.day > bonus_day:
        next_month = today.replace(day=1) + datetime.timedelta(days=32)
        bonus_date = next_month.replace(day=bonus_day)
    else:
        bonus_date = today.replace(day=bonus_day)
    days_left = (bonus_date - today).days
    return f"موعد صرف المكافأة: {bonus_date.date()}، المتبقي: {days_left} يوم"

# التقويم الأكاديمي
academic_events = [
    ("طلب إعادة القيد", "2025-01-05", "2025-01-18"),
    ("تأجيل الدراسة", "2025-01-05", "2025-01-14"),
    ("استقبال طلبات الزيارة", "2025-01-05", "2025-01-16"),
    ("بداية الدراسة", "2025-01-12", "2025-06-26"),
    ("الاعتذار عن الدراسة", "2025-01-19", "2025-05-10"),
    ("تقديم أعذار الاختبارات", "2025-01-19", "2025-02-20"),
    ("يوم التأسيس", "2025-02-23", "2025-02-23"),
    ("إجازة منتصف الفصل الثاني", "2025-02-24", "2025-03-01"),
    ("بداية الدراسة بعد الإجازة", "2025-03-02", "2025-03-13"),
    ("إجازة عيد الفطر", "2025-03-13", "2025-04-05"),
    ("الدراسة بعد عيد الفطر", "2025-04-06", "2025-06-26"),
    ("الاعتذار عن مقرر دراسي", "2025-04-13", "2025-04-17"),
    ("الاختبارات البديلة", "2025-04-20", "2025-04-24"),
    ("الاختبارات النهائية", "2025-05-18", "2025-05-26"),
    ("تغيير التخصص", "2025-05-25", "2025-06-30"),
    ("إجازة عيد الأضحى", "2025-05-26", "2025-06-14"),
    ("الدراسة بعد عيد الأضحى", "2025-06-15", "2025-06-26"),
    ("استكمال الاختبارات بعد العيد", "2025-06-15", "2025-06-24"),
    ("اعتماد النتائج", "2025-06-25", "2025-06-25"),
    ("إجازة نهاية العام", "2025-06-26", "2025-08-23"),
]

def get_event_status(start, end):
    today = datetime.datetime.now().date()
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
    if today < start_date:
        return "⏳", f"يبدأ بعد {(start_date - today).days} يوم"
    elif start_date <= today <= end_date:
        return "✅", f"جاري حتى {end_date}"
    else:
        return "❌", "انتهى"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("موعد المكافأة", callback_data="mokafa"),
         InlineKeyboardButton("أرقام التواصل", callback_data="contact")],
        [InlineKeyboardButton("الأسئلة الشائعة", callback_data="faq"),
         InlineKeyboardButton("تقييم الدكاترة", url="https://t.me/tudoctors")],
        [InlineKeyboardButton("منظومة الجامعة", url="https://edugate.tu.edu.sa"),
         InlineKeyboardButton("البلاك بورد", url="https://lms.tu.edu.sa/")],
        [InlineKeyboardButton("موقع جامعة الطلاب", url="https://maps.app.goo.gl/SJ2vYZt9wiqQYkx89"),
         InlineKeyboardButton("موقع جامعة الطالبات", url="https://maps.app.goo.gl/BPwmcoQ7T16CT2FX8")],
        [InlineKeyboardButton("حفل التخرج", callback_data="graduation")],
        [InlineKeyboardButton("دليل التخصصات", callback_data="majors")],
        [InlineKeyboardButton("التقويم الجامعي", callback_data="calendar")],
        [InlineKeyboardButton("قروب بيع الكتب", url="https://t.me/bookTaifUniversity")],
        [InlineKeyboardButton("قروب الفصل الصيفي", url="https://t.me/summerTaifUniversity")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("ضعت؟ ما لقيت احد يرد عليك؟ ولا يهمك\nانا هنا عشانك", reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "mokafa":
        await query.edit_message_text(get_bonus_days_remaining())
    elif query.data == "contact":
        await query.edit_message_text("للتواصل مع الجامعة:\nالهاتف: 920002122\nالإيميل: info@tu.edu.sa")
    elif query.data == "faq":
        keyboard = [
            [InlineKeyboardButton("كيف أسجل المواد؟", callback_data="faq_register")],
        ]
        await query.edit_message_text("الأسئلة الشائعة:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "faq_register":
        answer = ("المنظومة > التسجيل الإلكتروني\n"
                  "إذا لم تحذف مادة: تسجيل المجموعات الإلكترونية.\n"
                  "إذا حذفت أو حملت مادة: الحذف والإضافة يدويًا.")
        await query.edit_message_text(answer)
    elif query.data == "calendar":
        buttons = []
        for i, (name, start, end) in enumerate(academic_events):
            status_icon, _ = get_event_status(start, end)
            buttons.append([InlineKeyboardButton(f"{status_icon} {name}", callback_data=f"cal_{i}")])
        buttons.append([InlineKeyboardButton("❌ = منتهي | ✅ = جاري | ⏳ = قادم", callback_data="none")])
        await query.edit_message_text("التقويم الأكاديمي:", reply_markup=InlineKeyboardMarkup(buttons))
    elif query.data.startswith("cal_"):
        index = int(query.data.split("_")[1])
        name, start, end = academic_events[index]
        _, details = get_event_status(start, end)
        await query.edit_message_text(f"{name}\nمن {start} إلى {end}\n{details}")
    elif query.data == "graduation":
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=GRAD_IMAGE_URL)
    elif query.data == "majors":
        await context.bot.send_document(chat_id=query.message.chat_id, document=open(PDF_PATH, "rb"))
    elif query.data == "none":
        pass

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ضعت؟ ما لقيت احد يرد عليك؟ ولا يهمك\nانا هنا عشانك\nاختار من القائمة تحت")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()
