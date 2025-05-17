from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"

# قائمة الأزرار مع callback_data مخصصة
main_menu_buttons = [
    [("موعد المكافأة", "bonus"), ("أرقام التواصل", "contact")],
    [("الأسئلة الشائعة", "faq"), ("تقييم الدكاترة", "doctors_rating")],
    [("منظومة الجامعة", "university_system"), ("البلاك بورد", "blackboard")],
    [("موقع جامعة الطلاب", "male_students_map"), ("موقع جامعة الطالبات", "female_students_map")],
    [("حفل التخرج", "graduation"), ("دليل التخصصات", "majors_guide")],
    [("قروب بيع الكتب", "books_group"), ("قروب الفصل الصيفي", "summer_sem_group")],
    [("قروبات الكليات", "colleges_groups"), ("قروبات فروع الجامعة", "branches_groups")],
    [("التقويم الأكاديمي", "academic_calendar"), ("حساب المعدل الفصلي", "gpa_calc")]
]

def get_main_menu_markup():
    keyboard = []
    for row in main_menu_buttons:
        keyboard.append([InlineKeyboardButton(text, callback_data=data) for text, data in row])
    return InlineKeyboardMarkup(keyboard)

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
    uid = update.effective_user.id
    shown_welcome.add(uid)
    await update.message.reply_text("أهلًا! هذه هي القائمة الرئيسية، اختر أحد الخيارات:", reply_markup=get_main_menu_markup())

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # هنا ممكن تضيف وظائف لكل callback_data
    if data == "bonus":
        today = datetime.today()
        bonus = datetime(today.year + (today.month == 12 and today.day > 26), (today.month % 12) + 1 if today.day > 26 else today.month, 26)
        left = (bonus - today).days
        await query.edit_message_text(f"موعد المكافأة: {bonus.date()}\nالمتبقي: {left} يوم", reply_markup=get_main_menu_markup())

    elif data == "contact":
        await query.edit_message_text("الهاتف: 920002122\nالإيميل: info@tu.edu.sa", reply_markup=get_main_menu_markup())

    elif data == "doctors_rating":
        await query.edit_message_text("https://t.me/tudoctors", reply_markup=get_main_menu_markup())

    elif data == "university_system":
        await query.edit_message_text("https://edugate.tu.edu.sa", reply_markup=get_main_menu_markup())

    elif data == "blackboard":
        await query.edit_message_text("https://lms.tu.edu.sa", reply_markup=get_main_menu_markup())

    elif data == "male_students_map":
        await query.edit_message_text("https://maps.app.goo.gl/SJ2vYZt9wiqQYkx89", reply_markup=get_main_menu_markup())

    elif data == "female_students_map":
        await query.edit_message_text("https://maps.app.goo.gl/BPwmcoQ7T16CT2FX8", reply_markup=get_main_menu_markup())

    elif data == "graduation":
        await query.edit_message_media(
            media="https://www2.0zz0.com/2025/05/15/07/864959598.jpeg"
        )
        # أو ترسل الصورة كرسالة منفصلة بدل edit_message_media لو حاب:
        # await query.edit_message_text("حفل التخرج")
        # await query.message.reply_photo("https://www2.0zz0.com/2025/05/15/07/864959598.jpeg")

    elif data == "academic_calendar":
        await query.edit_message_text("التقويم الأكاديمي:", reply_markup=calendar_keyboard())

    elif data == "legend":
        await query.edit_message_text(
            "شرح الرموز:\n"
            "⏳ = لم يبدأ بعد\n"
            "✅ = جاري\n"
            "❌ = انتهى"
            , reply_markup=calendar_keyboard()
        )

    elif data.startswith("event_"):
        idx = int(data.split("_")[1])
        title, start, end = academic_events[idx]
        await query.edit_message_text(f"{title}\nمن: {start}\nإلى: {end}", reply_markup=calendar_keyboard())

    elif data == "gpa_calc":
        context.user_data["gpa_entries"] = []
        await query.edit_message_text(
            "حياك! 🚀 جاهز لحساب معدلك الفصلي؟\n"
            "أرسل المواد بصيغة:\n"
            "عدد الساعات/الدرجة مثل:\n"
            "`3/A+ 4/B 2/C+`\n\n"
            "بعد ما تخلص، أرسل *حساب* لحساب المعدل، أو *إلغاء* للخروج.",
            parse_mode="Markdown"
        )

    # أضف هنا باقي ال callback_data اللي تحتاجها حسب تطبيقك

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in shown_welcome:
        await update.message.reply_text("رجاءً ارسل /start أولًا لتشغيل البوت واظهار القائمة.")
        return

    msg = update.message.text.strip()

    if "gpa_entries" in context.user_data:
        if msg.lower() == "حساب":
            entries = context.user_data.get("gpa_entries", [])
            if not entries:
                await update.message.reply_text("❌ ما أدخلت أي مواد، أرسل المواد أولاً.")
                return
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
            await update.message.reply_text("تم إلغاء حساب المعدل.", reply_markup=get_main_menu_markup())
            return
        else:
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

    # نصوص باقي الأوامر، يمكن تجاهلها لأن القائمة الآن أزرار Inline
    await update.message.reply_text("اضغط على أحد الأزرار من القائمة.")

async def handle_gpa_calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    entries = context.user_data.get("gpa_entries", [])
    if not entries:
        await query.edit_message_text("❌ ما أدخلت أي مواد، أرسل المواد أولاً.")
        return

    total_hours = sum(hours for hours, _ in entries)
    if total_hours == 0:
        await query.edit_message_text("❌ مجموع الساعات لا يمكن أن يكون صفر.")
        return

    total_points = sum(hours * GRADE_POINTS.get(grade, 0) for hours, grade in entries)
    gpa = total_points / total_hours
    await query.edit_message_text(f"معدلك الفصلي هو: {gpa:.2f}", reply_markup=get_main_menu_markup())
    context.user_data.pop("gpa_entries", None)

async def handle_gpa_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["gpa_entries"] = []
    await query.edit_message_text("تم إعادة تعيين المواد. أرسل المواد مرة أخرى بصيغة:\nعدد الساعات/الدرجة مثل:\n`3/A+ 4/B 2/C+`", parse_mode="Markdown")

async def handle_gpa_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.pop("gpa_entries", None)
    await query.edit_message_text("تم إلغاء حساب المعدل.", reply_markup=get_main_menu_markup())

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback_query))
    app.add_handler(CallbackQueryHandler(handle_gpa_calculate, pattern="^gpa_calculate$"))
    app.add_handler(CallbackQueryHandler(handle_gpa_reset, pattern="^gpa_reset$"))
    app.add_handler(CallbackQueryHandler(handle_gpa_cancel, pattern="^gpa_cancel$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
