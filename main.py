from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"

main_menu = [
    ["موعد المكافأة", "أرقام التواصل"],
    ["الأسئلة الشائعة", "تقييم الدكاترة"],
    ["منظومة الجامعة", "البلاك بورد"],
    ["موقع جامعة الطلاب", "موقع جامعة الطالبات"],
    ["حفل التخرج", "دليل التخصصات"],
    ["قروب بيع الكتب", "قروب الفصل الصيفي"],
    ["قروبات الكليات", "قروبات فروع الجامعة"],
    ["التقويم الأكاديمي"]
]

reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
shown_welcome = set()

academic_events = [
    ("طلب إعادة القيد", "2025-01-05", "2025-01-18"),
    ("تأجيل الدراسة", "2025-01-05", "2025-01-14"),
    ("استقبال طلبات الزيارة", "2025-01-05", "2025-01-16"),
    ("بداية الدراسة للفصل الدراسي الثاني", "2025-01-12", "2025-06-26"),
    ("الإعتذار عن الدراسة", "2025-01-19", "2025-05-10"),
    ("تقديم أعذار الاختبارات", "2025-01-19", "2025-02-20"),
    ("يوم التأسيس", "2025-02-23", "2025-02-23"),
    ("إجازة منتصف الفصل الثاني", "2025-02-24", "2025-03-01"),
    ("بداية الدراسة بعد إجازة منتصف الفصل", "2025-03-02", "2025-03-13"),
    ("بداية إجازة عيد الفطر", "2025-03-13", "2025-04-05"),
    ("بداية الدراسة بعد إجازة عيد الفطر", "2025-04-06", "2025-06-26"),
    ("الاعتذار عن مقرر دراسي", "2025-04-13", "2025-04-17"),
    ("الاختبارات البديلة", "2025-04-20", "2025-04-24"),
    ("الاختبارات النهائية", "2025-05-18", "2025-05-26"),
    ("إدخال رغبات تغيير التخصص", "2025-05-25", "2025-06-30"),
    ("إجازة عيد الأضحى", "2025-05-26", "2025-06-14"),
    ("بداية الدراسة بعد عيد الأضحى", "2025-06-15", "2025-06-26"),
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

def calendar_keyboard():
    keyboard = []
    for i, (title, start, end) in enumerate(academic_events):
        icon = get_status_icon(start, end)
        text = f"{icon} {title} ({start} → {end})"
        keyboard.append([InlineKeyboardButton(text, callback_data=f"event_{i}")])
    keyboard.append([InlineKeyboardButton("شرح الرموز", callback_data="legend")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in shown_welcome:
        await update.message.reply_text("ضعت؟ ما لقيت احد يرد عليك؟ ولا يهمك\nانا هنا عشانك", reply_markup=reply_markup)
        shown_welcome.add(uid)
    else:
        await update.message.reply_text("اختر من القائمة:", reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "موعد المكافأة":
        today = datetime.today()
        bonus = datetime(today.year + (today.month == 12 and today.day > 26), (today.month % 12) + 1 if today.day > 26 else today.month, 26)
        left = (bonus - today).days
        await update.message.reply_text(f"موعد المكافأة: {bonus.date()}\nالمتبقي: {left} يوم")

    elif msg == "أرقام التواصل":
        await update.message.reply_text("الهاتف: 920002122\nالإيميل: info@tu.edu.sa")

    elif msg == "قروبات فروع الجامعة":
        await update.message.reply_text("اختر الفرع:", reply_markup=ReplyKeyboardMarkup([
            ["فرع تربة", "فرع الخرمة", "فرع رنية"], ["رجوع"]
        ], resize_keyboard=True))
    elif msg == "فرع تربة":
        await update.message.reply_text("https://t.me/+LTvqFqmbNhU3Nzg0")
    elif msg == "فرع الخرمة":
        await update.message.reply_text("https://t.me/+TI4sw9271iJhNDU0")
    elif msg == "فرع رنية":
        await update.message.reply_text("https://t.me/+LhI_BEwURHNlNGZk")

    elif msg == "قروبات الكليات":
        await update.message.reply_text("اختر الكلية:", reply_markup=ReplyKeyboardMarkup([
            ["كلية التربية", "الكلية التطبيقية"],
            ["دبلوم المناولة الأرضية", "كلية العلوم"],
            ["كلية الهندسة", "كلية الحاسبات"],
            ["كلية التصاميم", "كلية الشريعة"],
            ["كلية إدارة الأعمال", "كلية التقنية"],
            ["كلية الطب", "كلية طب الأسنان"],
            ["التمريض", "كلية الصيدلة"],
            ["العلاج الطبيعي", "علوم الأشعة"],
            ["المختبرات الإكلينيكية"], ["رجوع"]
        ], resize_keyboard=True))

    college_links = {
        "كلية التربية": "https://t.me/educationTaifUniversity",
        "الكلية التطبيقية": "https://t.me/appliedstudiesTaifUniversity",
        "دبلوم المناولة الأرضية": "https://t.me/aviationTaifUniversity",
        "كلية العلوم": "https://t.me/TaifUnivierstiy1",
        "كلية الهندسة": "https://t.me/engineeringTaifUniversity",
        "كلية الحاسبات": "https://t.me/computersTaifUniversity",
        "كلية التصاميم": "https://t.me/designsTaifUniversity",
        "كلية الشريعة": "https://t.me/+TKCYp3jPayCyUgSw",
        "كلية إدارة الأعمال": "https://t.me/+na12acQgxzxkZTZk",
        "كلية التقنية": "https://t.me/tvtcVocationalTaifCorporation",
        "كلية الطب": "https://t.me/medicine_Tu",
        "كلية طب الأسنان": "https://t.me/Dentistry_TU",
        "كلية الصيدلة": "https://t.me/Pharma_DTU33",
        "التمريض": "https://t.me/nursstudent",
        "العلاج الطبيعي": "https://t.me/Physical_therapyTU",
        "علوم الأشعة": "https://t.me/RadiologySciences",
        "المختبرات الإكلينيكية": "https://t.me/labrotary_Tu"
    }

    if msg in college_links:
        await update.message.reply_text(college_links[msg])

    elif msg == "شرح الرموز":
        await update.message.reply_text("✅ = جاري\n❌ = منتهي\n⏳ = لم يبدأ بعد", reply_markup=ReplyKeyboardMarkup([["رجوع"]], resize_keyboard=True))

    elif msg == "رجوع":
        await start(update, context)

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
    elif msg == "قروب بيع الكتب":
        await update.message.reply_text("https://t.me/bookTaifUniversity")
    elif msg == "قروب الفصل الصيفي":
        await update.message.reply_text("https://t.me/summerTaifUniversity")
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
    elif msg == "الأسئلة الشائعة":
        await update.message.reply_text("اختر سؤال:", reply_markup=ReplyKeyboardMarkup([
            ["كيف أسجل المواد؟"], ["رجوع"]
        ], resize_keyboard=True))
    elif msg == "كيف أسجل المواد؟":
        await update.message.reply_text(
            "المنظومة > التسجيل الإلكتروني\n\n"
            "- إذا لم تحذف مادة: تسجيل المجموعات الإلكترونية.\n"
            "- إذا حذفت أو حملت مادة: الحذف والإضافة يدويًا."
        )
    elif msg == "التقويم الأكاديمي":
        await update.message.reply_text("التقويم الأكاديمي:", reply_markup=calendar_keyboard())
    else:
        await update.message.reply_text("اختر من القائمة:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "legend":
        await query.edit_message_text("✅ = جاري\n❌ = منتهي\n⏳ = لم يبدأ بعد", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("رجوع", callback_data="calendar_back")]
        ]))
    elif data == "calendar_back":
        await query.edit_message_text("التقويم الأكاديمي:", reply_markup=calendar_keyboard())
    elif data.startswith("event_"):
        index = int(data.split("_")[1])
        title, start, end = academic_events[index]
        today = datetime.today().date()
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if today < start_date:
            msg = f"{title} يبدأ بعد {(start_date - today).days} يوم."
        elif start_date <= today <= end_date:
            msg = f"{title} جاري، ينتهي بعد {(end_date - today).days} يوم."
        else:
            msg = f"{title} انتهى."
        await query.edit_message_text(msg, reply_markup=calendar_keyboard())

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.add_handler(CallbackQueryHandler(handle_callback))
app.run_polling()
