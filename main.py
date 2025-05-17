from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"

# القائمة الرئيسية
main_menu = [
    ["موعد المكافأة", "أرقام التواصل"],
    ["الأسئلة الشائعة", "تقييم الدكاترة"],
    ["منظومة الجامعة", "البلاك بورد"],
    ["موقع جامعة الطلاب", "موقع جامعة الطالبات"],
    ["حفل التخرج", "قروب بيع الكتب"],
    ["قروب الفصل الصيفي", "قروبات الكليات"],
    ["قروبات الفروع", "دليل التخصصات"],
    ["التقويم الأكاديمي", "حساب المعدل الفصلي"]
]

reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# أحداث التقويم الأكاديمي
academic_events = [
    ("طلب إعادة القيد", "2025-01-05", "2025-01-18"),
    ("تأجيل الدراسة", "2025-01-05", "2025-01-14"),
    ("استقبال طلبات الزيارة", "2025-01-05", "2025-01-16"),
    ("بداية الدراسة للفصل الدراسي الثاني", "2025-01-12", "2025-06-26"),
    ("الإعتذار عن الدراسة", "2025-01-19", "2025-05-10"),
    ("إجازة عيد الفطر", "2025-03-13", "2025-04-05"),
    ("الاختبارات النهائية", "2025-05-18", "2025-05-26"),
    ("إجازة عيد الأضحى", "2025-05-26", "2025-06-14")
]

def get_status_icon(start_str, end_str):
    today = datetime.today().date()
    start = datetime.strptime(start_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_str, "%Y-%m-%d").date()
    if today < start:
        return "⏳"
    elif start <= today <= end:
        return "✅"
    else:
        return "❌"

def build_calendar_keyboard():
    keyboard = []
    for i, (title, start, end) in enumerate(academic_events):
        icon = get_status_icon(start, end)
        keyboard.append([InlineKeyboardButton(f"{icon} {title}", callback_data=f"event_{i}")])
    keyboard.append([InlineKeyboardButton("شرح الرموز", callback_data="legend")])
    return InlineKeyboardMarkup(keyboard)

# نقاط الدرجات
GRADE_POINTS = {
    "A+": 4.0, "A": 3.75, "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا بك، اختر من القائمة:", reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "موعد المكافأة":
        today = datetime.today()
        bonus_date = datetime(today.year, today.month, 26) if today.day <= 26 else datetime(today.year, today.month + 1, 26)
        remaining_days = (bonus_date - today).days
        await update.message.reply_text(f"موعد المكافأة: {bonus_date.date()}\nالمتبقي: {remaining_days} يوم")

    elif msg == "حفل التخرج":
        await update.message.reply_photo("https://www2.0zz0.com/2025/05/15/07/864959598.jpeg")

    elif msg == "دليل التخصصات":
        images = [
            "https://www2.0zz0.com/2025/05/15/09/898187191.jpeg",
            "https://www2.0zz0.com/2025/05/15/09/940232684.jpeg",
            "https://www2.0zz0.com/2025/05/15/09/275392642.jpeg",
            "https://www2.0zz0.com/2025/05/15/09/316519082.jpeg",
            "https://www2.0zz0.com/2025/05/15/09/409568913.jpeg"
        ]
        for img in images:
            await update.message.reply_photo(img)

    elif msg == "قروبات الكليات":
        await update.message.reply_text(
            "إليك روابط قروبات الكليات:\n\n"
            "- كلية الهندسة: https://t.me/engineering_group\n"
            "- كلية العلوم: https://t.me/science_group\n"
            "- كلية إدارة الأعمال: https://t.me/business_group\n"
            "- كلية الطب: https://t.me/medicine_group\n"
            "- كلية التربية: https://t.me/education_group"
        )

    elif msg == "التقويم الأكاديمي":
        await update.message.reply_text("التقويم الأكاديمي:", reply_markup=build_calendar_keyboard())

    elif msg == "حساب المعدل الفصلي":
        context.user_data["gpa_entries"] = []
        await update.message.reply_text(
            "أرسل المواد بصيغة: `عدد الساعات/الدرجة` مثل: `3/A+ 4/B`.\n"
            "بعد الانتهاء، أرسل *حساب* لحساب المعدل أو *إلغاء* للخروج.",
            parse_mode="Markdown"
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "legend":
        await query.edit_message_text("✅ = جاري\n❌ = منتهي\n⏳ = لم يبدأ بعد")

    elif data.startswith("event_"):
        index = int(data.split("_")[1])
        title, start, end = academic_events[index]
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        today = datetime.today().date()

        if today < start_date:
            msg = f"{title} سيبدأ في {start_date}."
        elif start_date <= today <= end_date:
            msg = f"{title} جاري حتى {end_date}."
        else:
            msg = f"{title} انتهى في {end_date}."

        await query.edit_message_text(msg, reply_markup=build_calendar_keyboard())

# إعداد البوت
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()
