from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ConversationHandler
from datetime import datetime

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"  # ضع هنا توكن البوت الخاص بك

# القائمة الرئيسية مع زر حساب المعدل الفصلي
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
    ("تقديم أعذار الاختبارات", "2025-01-19", "2025-02-20"),
    ("يوم التأسيس", "2025-02-23", "2025-02-23"),
    ("إجازة منتصف الفصل الثاني", "2025-02-24", "2025-03-01"),
    ("الدراسة بعد إجازة منتصف الفصل", "2025-03-02", "2025-03-13"),
    ("إجازة عيد الفطر", "2025-03-13", "2025-04-05"),
    ("بداية الدراسة بعد عيد الفطر", "2025-04-06", "2025-06-26"),
    ("الاعتذار عن مقرر دراسي", "2025-04-13", "2025-04-17"),
    ("الاختبارات البديلة", "2025-04-20", "2025-04-24"),
    ("الاختبارات النهائية", "2025-05-18", "2025-05-26"),
    ("إدخال رغبات تغيير التخصص", "2025-05-25", "2025-06-30"),
    ("إجازة عيد الأضحى", "2025-05-26", "2025-06-14"),
    ("الدراسة بعد عيد الأضحى", "2025-06-15", "2025-06-26"),
    ("استكمال الاختبارات بعد العيد", "2025-06-15", "2025-06-24"),
    ("اعتماد النتائج", "2025-06-25", "2025-06-25"),
    ("إجازة نهاية العام", "2025-06-26", "2025-08-23")
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

# جدول تحويل الرموز إلى نقاط
grade_to_gpa = {
    "A+": 4.0,
    "A": 3.75,
    "B+": 3.5,
    "B": 3.0,
    "C+": 2.5,
    "C": 2.0,
    "D+": 1.5,
    "D": 1.0,
    "F": 0.0
}

# --- حساب المعدل ConversationHandler states ---
GPA_WAITING_INPUT = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا بك، اختر من القائمة:", reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    msg_l = msg.lower()
    # فقط عند /start أو start تظهر الأزرار
    if msg_l == "start" or msg_l == "/start":
        await update.message.reply_text("أهلًا بك، اختر من القائمة:", reply_markup=reply_markup)
        return

    if msg == "موعد المكافأة":
        today = datetime.today()
        target_day = 26
        if today.day > target_day:
            if today.month == 12:
                bonus = datetime(today.year + 1, 1, target_day)
            else:
                bonus = datetime(today.year, today.month + 1, target_day)
        else:
            bonus = datetime(today.year, today.month, target_day)
        left = (bonus - today).days
        await update.message.reply_text(f"موعد المكافأة: {bonus.date()}\nالمتبقي: {left} يوم")

    elif msg == "التقويم الأكاديمي":
        await update.message.reply_text("التقويم الأكاديمي:", reply_markup=build_calendar_keyboard())

    elif msg == "أرقام التواصل":
        await update.message.reply_text("الهاتف: 920002122")

    elif msg == "تقييم الدكاترة":
        await update.message.reply_text("https://t.me/tudoctors")

    elif msg == "منظومة الجامعة":
        await update.message.reply_text("https://edugate.tu.edu.sa")

    elif msg == "البلاك بورد":
        await update.message.reply_text("https://lms.tu.edu.sa")

    elif msg == "موقع جامعة الطلاب":
        await update.message.reply_text("https://maps.app.goo.gl/SJ2vYZt9wiqQYkx89")

    elif msg == "موقع جامعة الطالبات":
        await update.message.reply_text("https://maps.app.goo.gl/BPwmcoQ7T16CT2FX8")

    elif msg == "حفل التخرج":
        await update.message.reply_photo("https://www2.0zz0.com/2025/05/15/07/864959598.jpeg")

    elif msg == "دليل التخصصات":
        for img in [
            "https://www2.0zz0.com/2025/05/15/09/898187191.jpeg",
            "https://www2.0zz0.com/2025/05/15/09/940232684.jpeg",
            "https://www2.0zz0.com/2025/05/15/09/275392642.jpeg",
            "https://www2.0zz0.com/2025/05/15/09/316519082.jpeg",
            "https://www2.0zz0.com/2025/05/15/09/409568913.jpeg"
        ]:
            await update.message.reply_photo(img)

    elif msg == "حساب المعدل الفصلي":
        await update.message.reply_text(
            "أدخل رموز التقدير وعدد الساعات لكل مادة بهذا الشكل (الرمز ثم مسافة ثم ساعات، وبين كل مادة فاصلة):\n"
            "مثال: A+ 3, B 2, C+ 3\n"
            "الرموز المقبولة: A+, A, B+, B, C+, C, D+, D, F\n"
            "المعدل سيُحسب على النظام الرباعي (من 4) حسب النظام الجامعي."
        )
        return GPA_WAITING_INPUT

async def gpa_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        pairs = [pair.strip() for pair in text.split(",") if pair.strip()]
        total_points = 0
        total_hours = 0
        details = []
        for pair in pairs:
            grade, hours = pair.split()
            grade = grade.upper()
            hours = float(hours)
            if grade not in grade_to_gpa:
                await update.message.reply_text(f"الرمز غير صحيح: {grade}\nالرموز المقبولة: {', '.join(grade_to_gpa.keys())}")
                return ConversationHandler.END
            gpa = grade_to_gpa[grade]
            total_points += gpa * hours
            total_hours += hours
            details.append(f"الرمز: {grade} ← النقاط: {gpa} × الساعات: {hours} = {gpa*hours}")
        if total_hours == 0:
            await update.message.reply_text("عدد الساعات لا يمكن أن يكون صفرًا.")
            return ConversationHandler.END
        gpa_final = total_points / total_hours
        msg = "\n".join(details)
        await update.message.reply_text(f"{msg}\n\nمعدلك الفصلي هو: {gpa_final:.2f} من 4")
    except Exception:
        await update.message.reply_text("هناك خطأ في التنسيق. أعد المحاولة بشكل صحيح مثل: A 3, B+ 2, C+ 3")
    return ConversationHandler.END

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data == "legend":
        await query.edit_message_text("✅ = جاري\n❌ = منتهي\n⏳ = لم يبدأ بعد")
    elif data.startswith("event_"):
        index = int(data.split("_")[1])
        title, start, end = academic_events[index]
        today = datetime.today().date()
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if today < start_date:
            await query.edit_message_text(f"{title} سيبدأ بعد {(start_date - today).days} يوم.", reply_markup=build_calendar_keyboard())
        elif start_date <= today <= end_date:
            await query.edit_message_text(f"{title} جاري، سينتهي بعد {(end_date - today).days} يوم.", reply_markup=build_calendar_keyboard())
        else:
            await query.edit_message_text(f"{title} انتهى.", reply_markup=build_calendar_keyboard())

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# ConversationHandler لإدخال المعدل الفصلي
gpa_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^حساب المعدل الفصلي$"), handle_text)],
    states={
        GPA_WAITING_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpa_input)]
    },
    fallbacks=[],
)
app.add_handler(gpa_conv_handler)

app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()
