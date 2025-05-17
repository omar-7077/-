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

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"  # ضع هنا توكن البوت الخاص بك

main_menu = [
    ["موعد المكافأة", "أرقام التواصل"],
    ["الأسئلة الشائعة", "تقييم الدكاترة"],
    ["منظومة الجامعة", "البلاك بورد"],
    ["موقع جامعة الطلاب", "موقع جامعة الطالبات"],
    ["حفل التخرج", "قروب بيع الكتب"],
    ["قروب الفصل الصيفي", "قروبات الكليات"],
    ["قروبات الفروع", "دليل التخصصات"],
    ["التقويم الأكاديمي", "حساب المعدل الفصلي"],
    ["ابحث عن دكتورك"],  # زر البحث عن دكتورك
]

reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# قروبات الكليات
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

# قروبات الفروع
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلًا بك، اختر من القائمة:", reply_markup=reply_markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.strip()
    msg_l = msg.lower()
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
    data = query.data

    # كليات
    if data.startswith("college_"):
        idx = int(data.split("_")[1])
        name, link = colleges[idx]
        await query.answer()
        await query.edit_message_text(f"قروب {name}:\n{link}\n\n↩️ للرجوع للقائمة السابقة اضغط على الزر بالأسفل.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ رجوع", callback_data="back_colleges")]]))

    # فروع
    elif data.startswith("branch_"):
        idx = int(data.split("_")[1])
        name, link = branches[idx]
        await query.answer()
        await query.edit_message_text(f"قروب {name}:\n{link}\n\n↩️ للرجوع للقائمة السابقة اضغط على الزر بالأسفل.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️ رجوع", callback_data="back_branches")]]))

    # الرجوع من زر الكليات الفرعي
    elif data == "back_colleges":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"college_{i}")]
            for i, (name, _) in enumerate(colleges)
        ]
        keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_to_main")])
        await query.edit_message_text("اختر الكلية:", reply_markup=InlineKeyboardMarkup(keyboard))

    # الرجوع من زر الفروع الفرعي
    elif data == "back_branches":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"branch_{i}")]
            for i, (name, _) in enumerate(branches)
        ]
        keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="back_to_main")])
        await query.edit_message_text("اختر الفرع:", reply_markup=InlineKeyboardMarkup(keyboard))

    # الرجوع للقائمة الرئيسية
    elif data == "back_to_main":
        await query.edit_message_text("أهلًا بك، اختر من القائمة:", reply_markup=reply_markup)

    # الأكاديمي وغيره كما هو...
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

# ============ البحث عن دكتورك "كلية الطب" ===============
faculty_medicine = [
    {"name": "مجتبى فاروقرانا محمد فاروق", "email": "drmujtabarana@tu.edu.sa"},
    {"name": "حاتم علي الشيخ النور", "email": "helsheikh@tu.edu.sa"},
    {"name": "عويض محمد عويض المالكي", "email": "oalmalki@tu.edu.sa"},
    {"name": "سعيد كامل محمد بلال", "email": "sbelal@tu.edu.sa"},
    {"name": "محمد عبدالرحمن عبدالعزيز البليهد", "email": "mabulihd@tu.edu.sa"},
    {"name": "شادي عبدالحميد بهاء الدين تمر", "email": "shaditamur@tu.edu.sa"},
    {"name": "فيصل خالد حميان الحمياني", "email": "f.alhomayani@tu.edu.sa"},
    {"name": "ايمن المغاوري القناوى علي", "email": "elkenawy@tu.edu.sa"},
    {"name": "يحيى أحمد بكر فقيه", "email": "yahya@tu.edu.sa"},
    {"name": "عبد الحميد سعد محمد الغامدي", "email": "ghamdi@tu.edu.sa"},
    {"name": "حسام الدين حسين عثمان إبراهيم", "email": "h.hussein@tu.edu.sa"},
    {"name": "علي حسن صحفان الزهراني", "email": "alisahfan@tu.edu.sa"},
    {"name": "اشرف يحي عبود البركاتي", "email": "a.albrakati@tu.edu.sa"},
    {"name": "عبد الله عائد محمد الحارثي", "email": "aaharthi@tu.edu.sa"},
    {"name": "غاليه عبيد فالح النفيعي", "email": "ghaliah.o@tu.edu.sa"},
    {"name": "هاشم عبد الرحيم هاشم بخاري", "email": "h.abdulrahim@tu.edu.sa"},
    {"name": "احمد سعد احمد الزهراني", "email": "as.alzahrani@tu.edu.sa"},
    {"name": "انوار مصطفى محمود شمس", "email": "a.shams@tu.edu.sa"},
    {"name": "عدنان عبد الله عطاالله الطويرقي", "email": "a.altwerqi@tu.edu.sa"},
    {"name": "اكرم عبد العزيز عطية الله الصحفي", "email": "ak.alsahafi@tu.edu.sa"},
    {"name": "عوض سمير عوض الصبان", "email": "awsabban@tu.edu.sa"},
    {"name": "مصطفى محمد فرج دسوقي", "email": "mmfarag@tu.edu.sa"},
    {"name": "فاطمه سمير حسن عرابي", "email": "fatimah.s@tu.edu.sa"},
    {"name": "سعد سالم مسفر الزهراني", "email": "salzahrani@tu.edu.sa"},
    {"name": "عزه حسن عبد الرحمن حسين", "email": "dr.azza@tu.edu.sa"},
    {"name": "منال شعراوي حسين محمد", "email": "m_sharaway@tu.edu.sa"},
    {"name": "عماد عزمي عوضين محمد ابراهيم", "email": "imadmohamed@tu.edu.sa"},
    {"name": "ايمن رجب بيومي عبد السيد", "email": "aymanr@tu.edu.sa"},
    {"name": "احمد حسن عبد الرحمن حسن الرشيدي", "email": "a.elrashedy@tu.edu.sa"},
    {"name": "ايمن كمال عبد الحميد اسماعيل", "email": "aymanka@tu.edu.sa"},
    {"name": "طلال عبدالرحمن مبروك الثمالي", "email": "tthomali@tu.edu.sa"},
    {"name": "احمد سيد عبدالمنعم سيد", "email": "asa@tu.edu.sa"},
    {"name": "سوزان عطية مصطفى السيد", "email": "s.atia@tu.edu.sa"},
    {"name": "عبد الله علي مرشد الحسني الزهراني", "email": "abdullazahrani@tu.edu.sa"},
    {"name": "احمد عبد الباسط محمد قرقني بخاري", "email": "abukhari@tu.edu.sa"},
    {"name": "ابراهيم يوسف عبد الله ياسين", "email": "iyaseen@tu.edu.sa"},
    {"name": "رائد علي محمد الثبيتي", "email": "t.raed@tu.edu.sa"},
    {"name": "عبير ناصر محمد الغالبي", "email": "abeer.n@tu.edu.sa"},
    {"name": "نهى نبيل عبد الله فلفلان", "email": "nn.abdullah@tu.edu.sa"},
    {"name": "سلطان عبد الله احمد العاصمي المالكي", "email": "sultanab@tu.edu.sa"},
    {"name": "مريم سعود خلاوي الجعيد", "email": "maryam@tu.edu.sa"},
    {"name": "بلال عمر عبد الرحمن الجفري", "email": "b.aljiffry@tu.edu.sa"},
    {"name": "عبد الله محمد نور عبد الله خياط", "email": "khayatam@tu.edu.sa"},
    {"name": "جمال عبدالله صالح البشري", "email": "j.beshri@tu.edu.sa"},
    {"name": "ندى حسن محمد احمد", "email": "h.nada@tu.edu.sa"},
    {"name": "عبدالمجيد مسفر صالح القثامي", "email": "a.gethami@tu.edu.sa"},
    {"name": "خالد محمد غازي الحمياني", "email": "k.homayani@tu.edu.sa"},
    {"name": "خالد محمد احمد الزهراني", "email": "dr.k.al_zahrani@tu.edu.sa"},
    {"name": "محمد سالم محمد السعيد", "email": "m.alsaeed@tu.edu.sa"},
    {"name": "دلال محي الدين محمدعلي نمنقاني", "email": "d.nemenqani@tu.edu.sa"},
    {"name": "اماني محمود احمد عبداللطيف", "email": "amany.m@tu.edu.sa"},
    {"name": "امال ابراهيم الصديق محمد نور", "email": "a.ibraheem@tu.edu.sa"},
    {"name": "ضيف الله محمد عوين العبود", "email": "d.alaboud@tu.edu.sa"},
    {"name": "محمد حاتم إبراهيم خيري عوض الله", "email": "m.hatem@tu.edu.sa"},
    {"name": "هشام عبد الباسط محمد قرقني بخاري", "email": "h.bokhari@tu.edu.sa"},
    {"name": "علي خير الله علي الزهراني", "email": "a.zahrani@tu.edu.sa"},
    {"name": "علاء عصام اسماعيل يونس", "email": "aeyounes@tu.edu.sa"},
    {"name": "نسرين خالد عارف البزره", "email": "dr.nisreen@tu.edu.sa"},
    {"name": "علا احمد شوقي فرغلي", "email": "o.erfan@tu.edu.sa"},
    {"name": "ايمان علي محمد خليفة", "email": "e.khalifa@tu.edu.sa"},
    {"name": "احمد محمد محمد محمد", "email": "a.mohamed@tu.edu.sa"},
    {"name": "ياسر عواض سعيد الطويرقي", "email": "y.tuwairaqi@tu.edu.sa"},
    {"name": "لطفي فهمي محمد عيسى", "email": "l.issa@tu.edu.sa"},
    {"name": "طارق محمد علي محمد حسين", "email": "t.hussien@tu.edu.sa"},
    {"name": "علي نعمان علي النواوي", "email": "a.nawawy@tu.edu.sa"},
    {"name": "عواطف المحمدي فرج ادريس", "email": "a.edrees@tu.edu.sa"},
    {"name": "فاطمة صفي الدين محمد صادق محمود", "email": "fatimah.m@tu.edu.sa"},
    {"name": "عدنان علي أبوطالب مباركي", "email": "a.mubaraki@tu.edu.sa"},
    {"name": "أحمد فهد عطيه الثبيتي", "email": "ah.althobity@tu.edu.sa"},
    {"name": "سحر محمد عبدالله النفيعي", "email": "sahar.m@tu.edu.sa"},
    {"name": "الاء عبدالرحمن يوسف اسماعيل", "email": "alaa.s@tu.edu.sa"},
    {"name": "أحمد محمد حميد النمري", "email": "amnemari@tu.edu.sa"},
    {"name": "يسري عبدالحميد حواش الصباغ", "email": "y.hawash@tu.edu.sa"},
    {"name": "مني جمعه محمد عامر", "email": "mona.g@tu.edu.sa"},
    {"name": "باسم حسن حسين العيسوي", "email": "b.elesawy@tu.edu.sa"},
    {"name": "نهاد احمد محمد النشار", "email": "nihad.a@tu.edu.sa"},
    {"name": "نسرين محمد سعيد المرجوشي", "email": "nesrien.m@tu.edu.sa"},
    {"name": "امال عبد الرسول سليمان الحصري", "email": "amalelhosary@tu.edu.sa"},
    {"name": "محمد فهد عطيه الثبيتي", "email": "m.althobity@tu.edu.sa"},
    {"name": "حماد طفيل شودري", "email": "h.hammad@tu.edu.sa"},
    {"name": "عزه علي عبدالعطيم طه", "email": "azzaali@tu.edu.sa"},
    {"name": "عبدالله معيوض سالم الصواط", "email": "a.alsowat@tu.edu.sa"},
    {"name": "عبدالرحمن غرم الله سعيد الحربي المالكي", "email": "ag.almalki@tu.edu.sa"},
    {"name": "عبدالعزيز محمد علي العميري الشهري", "email": "ashehri@tu.edu.sa"},
    {"name": "خالد عبدالله عبادل السواط", "email": "k.alswat@tu.edu.sa"},
    {"name": "ايمن عبدالباقي أحمد عطاالله", "email": "dr.ayman@tu.edu.sa"},
    {"name": "تامر محمد عبدالرحمن عبدالعاطي", "email": "t.tamer@tu.edu.sa"},
    {"name": "رحاب أحمد كرم عبدالفتاح محمد عطا", "email": "Rehab.A@tu.edu.sa"},
    {"name": "نهى السيد حسن فرج", "email": "nohafarag@tu.edu.sa"},
    {"name": "فرزانا رضوان أرائين شاهد", "email": "farzana.r@tu.edu.sa"},
    {"name": "اريج احمد تلودي تركستاني", "email": "areeg.a@tu.edu.sa"},
    {"name": "ماجد عبد ربه وصل المورقي", "email": "mourgi@tu.edu.sa"},
    {"name": "عبدالمحسن محمد سراج بكر احمد جي", "email": "ahmadjee@tu.edu.sa"},
    {"name": "ابراهيم عبدالعزيز ابراهيم الغامدي", "email": "Iaghamdi@tu.edu.sa"},
    {"name": "ياسر حسين حسن النفيعي", "email": "y.alnofaiey@tu.edu.sa"},
    {"name": "عبدالرحمن ناصر زاهر الغامدي", "email": "alghamdi.a@tu.edu.sa"},
    {"name": "محمدعيد محمود ابراهيم محفوظ", "email": "m.mahfouz@tu.edu.sa"},
    {"name": "منال احمد محمد النشار", "email": "m.elnashar@tu.edu.sa"},
    {"name": "ريحاب شعبان عبدالمقصود السيد", "email": "shaaban.y@tu.edu.sa"},
    {"name": "هاني احمد ابراهيم ابو زيد", "email": "h.abozaid@tu.edu.sa"},
    {"name": "منذر عبدالله سفر الشهراني", "email": "m.shahrani@tu.edu.sa"},
    {"name": "رشا حسن سليمان على", "email": "y.soliman@tu.edu.sa"},
    {"name": "ضيف الله معيد رداد المنصوري", "email": "d.almansouri@tu.edu.sa"},
    {"name": "شذى هلال عبدالله الزيادي", "email": "shatha.h@tu.edu.sa"},
    {"name": "توفيق زهير عبدالله ال ليلح", "email": "ta.alshehri@tu.edu.sa"},
    {"name": "ابرار سعد نافع السلمي", "email": "abrar.s@tu.edu.sa"},
    {"name": "احمد عبدالله عبادل السواط", "email": "a.alsuuat@tu.edu.sa"},
    {"name": "نايف عيضه سعود العميري", "email": "n.edah@tu.edu.sa"},
    {"name": "يحيى عبدالله موسى الزهراني", "email": "y.mousa@tu.edu.sa"},
    {"name": "سماء ابوالفتوح طه محمد سالم", "email": "sama.m@tu.edu.sa"},
    {"name": "اسماء فرغلي حسن محمد", "email": "assma.f@tu.edu.sa"},
    {"name": "اعتماد عبدالجليل عبدالخالق علي", "email": "eetmad.a@tu.edu.sa"},
    {"name": "ايمان محي ابراهيم يوسف", "email": "emyoussef@tu.edu.sa"},
    {"name": "سمير احمد حسن بدر", "email": "s.badr@tu.edu.sa"},
    {"name": "سالم محسن سالم الزهراني", "email": "sa.mohsen@tu.edu.sa"},
    {"name": "فهد ابراهيم علي الجعيد", "email": "f.aljuaid@tu.edu.sa"},
    {"name": "هايل تركي لافي الحارثي", "email": "h.t.alharthi@tu.edu.sa"},
    {"name": "سامي سعود غزاي العضياني الحارثي", "email": "s.s.alharthi@tu.edu.sa"},
    {"name": "محمد ابراهيم جابر الجعيد العتيبي", "email": "m.jaber@tu.edu.sa"},
    {"name": "هيفاء عويض عمار العتيبي", "email": "a.haifa@tu.edu.sa"},
    {"name": "انعام محمد علي جمال جنينه", "email": "anam.m@tu.edu.sa"},
    {"name": "حسن علي حسن الشهري", "email": "hshehri@tu.edu.sa"},
    {"name": "أفنان مسفر ناجم الدهاسي العتيبي", "email": "amotaiby@tu.edu.sa"},
    {"name": "منى محمد علي محمد", "email": "mamohamed@tu.edu.sa"},
    {"name": "امين عطاالمنان الامين المكي", "email": "amakki@tu.edu.sa"},
    {"name": "خالد ابراهيم حسن ابراهيم", "email": "kebraheem@tu.edu.sa"},
    {"name": "ايمان سعد محمد بيومي", "email": "esbayoumy@tu.edu.sa"},
    {"name": "منال المطري محمد البشير", "email": "mebasher@tu.edu.sa"},
    {"name": "عفت عمران عمران نذير", "email": "imnazir@tu.edu.sa"},
    {"name": "هنوف حسن محمد الحسيكي الحارثي", "email": "hmharthy@tu.edu.sa"},
    {"name": "ناهد ابراهيم محمد جمعة", "email": "nigomaa@tu.edu.sa"},
    {"name": "امنه فضل بشير فضل", "email": "affadl@tu.edu.sa"},
    {"name": "حنان احمد فتحي عبد الموجود شلبي", "email": "hashalaby@tu.edu.sa"},
    {"name": "لبنى احمد متولي محمد", "email": "lamohomed@tu.edu.sa"},
    {"name": "محمد فتحي عباس محمد", "email": "mfabbas@tu.edu.sa"},
    {"name": "نادر محمد محمد محمد اسماعيل", "email": "n.nader@tu.edu.sa"},
    {"name": "غادة حسين عبد الله الحسن", "email": "ghelhassan@tu.edu.sa"},
    {"name": "علي مسفر سفير عيدان الخثعمي", "email": "a.alkhathami@tu.edu.sa"},
]

DOCTOR_SEARCH_FACULTY, DOCTOR_SEARCH_DOCTOR = range(2)

async def start_doctor_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("كلية الطب", callback_data="faculty_medicine")]
    ]
    await update.message.reply_text(
        "اختر الكلية:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return DOCTOR_SEARCH_FACULTY

async def select_faculty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton(doc["name"], callback_data=f"doctor_{i}")]
        for i, doc in enumerate(faculty_medicine)
    ]
    await query.answer()
    await query.edit_message_text(
        "اختر الدكتور:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return DOCTOR_SEARCH_DOCTOR

async def select_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    idx = int(query.data.replace("doctor_", ""))
    doctor = faculty_medicine[idx]
    name = doctor["name"]
    email = doctor["email"]
    msg = f"👤 {name}\n📧 {email}"
    await query.answer()
    await query.edit_message_text(msg)
    return ConversationHandler.END

doctor_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^ابحث عن دكتورك$"), start_doctor_search)],
    states={
        DOCTOR_SEARCH_FACULTY: [CallbackQueryHandler(select_faculty, pattern="^faculty_medicine$")],
        DOCTOR_SEARCH_DOCTOR: [CallbackQueryHandler(select_doctor, pattern="^doctor_")],
    },
    fallbacks=[],
)

# ================= إقلاع التطبيق ===============
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
gpa_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^حساب المعدل الفصلي$"), handle_text)],
    states={
        GPA_WAITING_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpa_input)]
    },
    fallbacks=[],
)
app.add_handler(doctor_conv_handler)
app.add_handler(gpa_conv_handler)
app.add_handler(MessageHandler(filters.TEXT, handle_text))
app.add_handler(CallbackQueryHandler(handle_callback))

app.run_polling()
