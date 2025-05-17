from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

# قائمة الأزرار الرئيسية (حُذف زر "الأسئلة الشائعة" وأُضيف "دليل التحويل من التخصصات")
main_menu = [
    ["موعد المكافأة", "أرقام التواصل"],
    ["تقييم الدكاترة", "منظومة الجامعة"],
    ["البلاك بورد", "موقع جامعة الطلاب"],
    ["موقع جامعة الطالبات", "حفل التخرج"],
    ["قروب بيع الكتب", "قروب الفصل الصيفي"],
    ["قروبات الكليات", "قروبات الفروع"],
    ["دليل التخصصات", "التقويم الأكاديمي"],
    ["حساب المعدل الفصلي", "ابحث عن دكتورك"],
    ["دليل التحويل من التخصصات"]
]
reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# ... تعريف بقية القوائم والمتغيرات كما في كودك ...

colleges = [
    ("كلية الآداب", "https://t.me/aladabTaifUniversity"),
    ("كلية التربية", "https://t.me/educationTaifUniversity"),
    ("الكلية التطبيقية (الدبلوم)", "https://t.me/appliedstudiesTaifUniversity"),
    ("دبلوم المناولة الأرضية للطيران", "https://t.me/aviationTaifUniversity"),
    ("كلية العلوم", "https://t.me/TaifUnivierstiy1"),
    ("كلية الهندسة", "https://t.me/engineeringTaifUniversity"),
    ("كلية الحاسبات وتقنية المعلومات", "https://t.me/computersTaifUniversity"),
    ("كلية التصاميم والفنون التطبيقية", "https://t.me/designsTaifUniversity"),
    ("كلية الشريعة والأنظمة", "https://t.me/+TKCYp3jPayCyUgSw"),
    ("كلية ادارة الأعمال", "https://t.me/+na12acQgxzxkZTZk"),
    ("كلية التقنية", "https://t.me/tvtcVocationalTaifCorporation"),
    ("كلية الطب", "https://t.me/medicine_Tu"),
    ("كلية طب الأسنان", "https://t.me/Dentistry_TU"),
    ("كلية الصيدلة", "https://t.me/Pharma_DTU33"),
    ("التمريض", "https://t.me/nursstudent"),
    ("العلاج الطبيعي", "https://t.me/Physical_therapyTU"),
    ("علوم الأشعة", "https://t.me/RadiologySciences"),
    ("المختبرات الاكلينيكية", "https://t.me/labrotary_Tu"),
]

branches = [
    ("فرع تربة", "https://t.me/+LTvqFqmbNhU3Nzg0"),
    ("فرع الخرمة", "https://t.me/+TI4sw9271iJhNDU0"),
    ("فرع رنية", "https://t.me/+LhI_BEwURHNlNGZk"),
]

grade_to_gpa = {
    "A+": 4.0, "A": 3.75, "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0
}

GPA_WAITING_INPUT = range(1)

BOOKS_GROUP = "https://t.me/bookTaifUniversity"
SUMMER_GROUP = "https://t.me/summerTaifUniversity"

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

medical_colleges = [
    ("منسوبي كلية الطب", "https://www.tu.edu.sa/Ar/كلية-الطب/92/Staff"),
    ("منسوبي كلية طب الأسنان", "https://www.tu.edu.sa/Ar/كلية-طب-الأسنان/209/Staff"),
    ("منسوبي كلية الصيدلة", "https://www.tu.edu.sa/Ar/كلية-الصيدلة/96/Staff"),
    ("منسوبي كلية العلوم الطبية التطبيقية", "https://www.tu.edu.sa/Ar/كلية-العلوم-الطبية-التطبيقية/99/Staff"),
    ("منسوبي كلية التمريض", "https://www.tu.edu.sa/Ar/كلية-التمريض/355/Staff"),
]

humanities_colleges = [
    ("منسوبي كلية التربية", "https://www.tu.edu.sa/Ar/كلية-التربية/94/Staff"),
    ("منسوبي كلية الآداب", "https://www.tu.edu.sa/Ar/كلية-الآداب/93/Staff"),
    ("منسوبي الكلية التطبيقية", "https://www.tu.edu.sa/Ar/الكلية-التطبيقية/216/Staff"),
]

sharia_colleges = [
    ("منسوبي كلية الشريعة والأنظمة", "https://www.tu.edu.sa/Ar/كلية-الشريعة-والأنظمة/95/Staff"),
    ("منسوبي كلية إدارة الأعمال", "https://www.tu.edu.sa/Ar/كلية-إدارة-الاعمال/98/Staff"),
]

scientific_colleges = [
    ("منسوبي كلية العلوم", "https://www.tu.edu.sa/Ar/كلية-العلوم/97/Staff"),
    ("منسوبي كلية الهندسة", "https://www.tu.edu.sa/Ar/كلية-الهندسة/103/Staff"),
    ("منسوبي كلية الحاسبات وتقنية المعلومات", "https://www.tu.edu.sa/Ar/كلية-الحاسبات-وتقنية-المعلومات/174/Staff"),
    ("منسوبي كلية التصاميم والفنون التطبيقية", "https://www.tu.edu.sa/Ar/كلية-التصاميم-والفنون-التطبيقية/176/Staff"),
]

main_categories = [
    ("الكليات الطبية", "main_medical"),
    ("كليات العلوم الإنسانية والتربوية", "main_humanities"),
    ("الكليات الشرعية والإدارية", "main_sharia"),
    ("الكليات العلمية والهندسية", "main_scientific"),
]

user_ids = set()
user_last_timer = {}

async def doctor_search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=cb)]
        for name, cb in main_categories
    ]
    keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_to_main")])
    await update.message.reply_text(
        "اختر تصنيف الكلية:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def doctor_search_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category):
    colleges_list = []
    if category == "main_medical":
        colleges_list = medical_colleges
    elif category == "main_humanities":
        colleges_list = humanities_colleges
    elif category == "main_sharia":
        colleges_list = sharia_colleges
    elif category == "main_scientific":
        colleges_list = scientific_colleges

    keyboard = [
        [InlineKeyboardButton(name, url=link)]
        for name, link in colleges_list
    ]
    keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_doctor_categories")])
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "اختر الكلية:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def doctor_search_back_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=cb)]
        for name, cb in main_categories
    ]
    keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_to_main")])
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "اختر تصنيف الكلية:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send_afk_joke(application, user_id):
    await asyncio.sleep(10)
    if user_last_timer.get(user_id, None) == "waiting":
        try:
            await application.bot.send_message(chat_id=user_id, text="وين رحت؟ لاتطول علينا 😂")
        except Exception as e:
            print(f"فشل إرسال المزحة للمستخدم {user_id}: {e}")
        user_last_timer.pop(user_id, None)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ids.add(user_id)
    await update.message.reply_text("أهلًا بك، اختر من القائمة:", reply_markup=reply_markup)
    user_last_timer[user_id] = "waiting"
    asyncio.create_task(send_afk_joke(context.application, user_id))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_ids.add(user_id)
    msg = update.message.text.strip()
    msg_l = msg.lower()

    user_last_timer[user_id] = "waiting"
    asyncio.create_task(send_afk_joke(context.application, user_id))

    if msg_l in ["start", "/start"]:
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

    elif msg == "قروب بيع الكتب":
        await update.message.reply_text("قروب بيع أو طلب الكتب لجميع تخصصات جامعة الطائف:\n" + BOOKS_GROUP)

    elif msg == "قروب الفصل الصيفي":
        await update.message.reply_text("قروب الفصل الصيفي | جامعة الطائف:\n" + SUMMER_GROUP)

    elif msg == "قروبات الكليات":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"college_{i}")]
            for i, (name, _) in enumerate(colleges)
        ]
        keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_to_main")])
        await update.message.reply_text("اختر الكلية:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif msg == "قروبات الفروع":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"branch_{i}")]
            for i, (name, _) in enumerate(branches)
        ]
        keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_to_main")])
        await update.message.reply_text("اختر الفرع:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif msg == "حساب المعدل الفصلي":
        await update.message.reply_text(
            "أدخل رموز التقدير وعدد الساعات لكل مادة بهذا الشكل (الرمز ثم مسافة ثم ساعات، وبين كل مادة فاصلة):\n"
            "مثال: A+ 3, B 2, C+ 3\n"
            "الرموز المقبولة: A+, A, B+, B, C+, C, D+, D, F\n"
            "المعدل سيُحسب على النظام الرباعي (من 4) حسب النظام الجامعي."
        )
        return GPA_WAITING_INPUT

    elif msg == "ابحث عن دكتورك":
        await doctor_search_start(update, context)
    
    elif msg == "دليل التحويل من التخصصات":
        await update.message.reply_photo("https://www2.0zz0.com/2025/05/17/23/580745112.jpeg")

async def gpa_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_last_timer[user_id] = "waiting"
    asyncio.create_task(send_afk_joke(context.application, user_id))

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
    data = query.data
    user_id = query.from_user.id
    user_last_timer[user_id] = "waiting"
    asyncio.create_task(send_afk_joke(context.application, user_id))

    if data.startswith("college_"):
        idx = int(data.split("_")[1])
        name, link = colleges[idx]
        await query.answer()
        await query.edit_message_text(f"قروب {name}:\n{link}\n\n↩️ للرجوع للقائمة السابقة اضغط على الزر بالأسفل.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ رجوع", callback_data="back_colleges")]]))

    elif data.startswith("branch_"):
        idx = int(data.split("_")[1])
        name, link = branches[idx]
        await query.answer()
        await query.edit_message_text(f"قروب {name}:\n{link}\n\n↩️ للرجوع للقائمة السابقة اضغط على الزر بالأسفل.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ رجوع", callback_data="back_branches")]]))

    elif data in ["main_medical", "main_humanities", "main_sharia", "main_scientific"]:
        await doctor_search_category(update, context, data)

    elif data == "back_doctor_categories":
        await doctor_search_back_categories(update, context)

    elif data == "back_colleges":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"college_{i}")]
            for i, (name, _) in enumerate(colleges)
        ]
        keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_to_main")])
        await query.edit_message_text("اختر الكلية:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "back_branches":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"branch_{i}")]
            for i, (name, _) in enumerate(branches)
        ]
        keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_to_main")])
        await query.edit_message_text("اختر الفرع:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "back_to_main":
        await query.edit_message_text("أهلًا بك، اختر من القائمة:", reply_markup=reply_markup)

    elif data == "legend":
        await query.answer()
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

async def reminder_callback(application):
    for user_id in user_ids:
        try:
            await application.bot.send_message(chat_id=user_id, text="وحشتنا! ماعندك سؤال؟")
        except Exception as e:
            print(f"فشل إرسال التذكير للمستخدم {user_id}: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY").build()
    app.add_handler(CommandHandler("start", start))
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

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        lambda: app.create_task(reminder_callback(app)),
        "interval",
        hours=3
    )
    scheduler.start()

    app.run_polling()
