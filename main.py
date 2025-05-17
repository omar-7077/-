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
    ["التقويم الأكاديمي", "حساب المعدل الفصلي"]  # أضفت هنا زر حساب المعدل
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

async def welcome_if_needed(update: Update):
    uid = update.effective_user.id
    if uid not in shown_welcome:
        shown_welcome.add(uid)
        await update.message.reply_text("ضعت؟ ما لقيت احد يرد عليك؟ ولا يهمك\nانا هنا عشانك", reply_markup=reply_markup)
        return True
    return False

# قاموس درجات مع النقاط لحساب المعدل من 4
GRADE_POINTS = {
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await welcome_if_needed(update)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await welcome_if_needed(update):
        return

    msg = update.message.text.strip()

    # هنا بدأنا إضافة دعم حساب المعدل
    if msg == "حساب المعدل الفصلي":
        context.user_data["gpa_entries"] = []
        await update.message.reply_text(
            "حياك! 🚀 جاهز لحساب معدلك الفصلي؟\n"
            "أرسل المواد بصيغة:\n"
            "عدد الساعات/الدرجة مثل:\n"
            "`3/A+ 4/B 2/C+`\n\n"
            "بعد ما تخلص، أرسل *حساب* لحساب المعدل، أو *إلغاء* للخروج.",
            parse_mode="Markdown"
        )
        return

    if "gpa_entries" in context.user_data:
        if msg.lower() == "حساب":
            entries = context.user_data.get("gpa_entries", [])
            if not entries:
                await update.message.reply_text("❌ ما أدخلت أي مواد، أرسل المواد أولاً.")
                return
            # عرض المواد للتأكيد
            text = "هذه المواد التي أدخلتها:\n"
            for i, (hours, grade) in enumerate(entries, start=1):
                text += f"{i}. {hours} ساعات - الدرجة: {grade}\n"
            text += "\nهل تريد حساب المعدل الآن؟"
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("حساب", callback_data="gpa_calculate"),
                    InlineKeyboardButton("إعادة إدخال", callback_data="gpa_reset"),
                    InlineKeyboardButton("إلغاء", callback_data="gpa_cancel")
                ]
            ])
            await update.message.reply_text(text, reply_markup=keyboard)
            return
        elif msg.lower() == "إلغاء":
            context.user_data.pop("gpa_entries", None)
            await update.message.reply_text("تم إلغاء حساب المعدل.", reply_markup=reply_markup)
            return
        else:
            # محاولة تحليل الإدخال بصيغة "عدد الساعات/الدرجة"
            try:
                parts = msg.split()
                for part in parts:
                    hours_str, grade = part.split("/")
                    hours = int(hours_str.strip())
                    grade = grade.strip().upper()
                    if grade not in GRADE_POINTS:
                        await update.message.reply_text(f"❌ الدرجة '{grade}' غير صحيحة. جرب مرة ثانية.")
                        return
                    context.user_data["gpa_entries"].append((hours, grade))
                await update.message.reply_text(
                    "✅ تم إضافة المواد. أرسل المزيد أو أرسل *حساب* للحساب، أو *إلغاء* للخروج.",
                    parse_mode="Markdown"
                )
            except Exception:
                await update.message.reply_text(
                    "❌ صيغة الإدخال غير صحيحة. استعمل الصيغة: `عدد الساعات/الدرجة` مثل `3/A+`.",
                    parse_mode="Markdown"
                )
            return

    # --- هنا تضع باقي أوامرك الأصلية ---
    if msg == "موعد المكافأة":
        today = datetime.today()
        bonus = datetime(today.year + (today.month == 12 and today.day > 26), (today.month % 12) + 1 if today.day > 26 else today.month, 26)
        left = (bonus - today).days
        await update.message.reply_text(f"موعد المكافأة: {bonus.date()}\nالمتبقي: {left} يوم")

    elif msg == "أرقام التواصل":
        await update.message.reply_text("الهاتف: 920002122\nالإيميل: info@tu.edu.sa")

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
