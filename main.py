from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import datetime
import os

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"  # استبدل هذا بالتوكن الخاص بك

student_location = (21.4389, 40.5103)
female_location = (21.4392, 40.5110)

main_menu = [
    ["موعد المكافأة"],
    ["أرقام التواصل"],
    ["الأسئلة الشائعة"],
    ["تقييم الدكاترة"],
    ["منظومة الجامعة"],
    ["البلاك بورد"],
    ["موقع الطلاب"],
    ["موقع الطالبات"],
    ["حفل التخرج"],
    ["التقويم الجامعي"]
]

faq_menu = [["كيف أسجل المواد؟"], ["رجوع"]]

reply_main = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
reply_faq = ReplyKeyboardMarkup(faq_menu, resize_keyboard=True)

calendar_events = [
    ("طلب إعادة القيد", "2025-01-05", "2025-01-18"),
    ("تأجيل الدراسة", "2025-01-05", "2025-01-14"),
    ("استقبال طلبات الزيارة", "2025-01-05", "2025-01-16"),
    ("بداية الدراسة للفصل الدراسي الثاني", "2025-01-12", "2025-06-26"),
    ("الإعتذار عن الدراسة", "2025-01-19", "2025-05-10"),
    ("تقديم أعذار الطلبة المتغيبين", "2025-01-19", "2025-02-20"),
    ("يوم التأسيس", "2025-02-23", "2025-02-23"),
    ("إجازة منتصف الفصل الدراسي الثاني", "2025-02-24", "2025-03-01"),
    ("بداية الدراسة بعد الإجازة", "2025-03-02", "2025-03-13"),
    ("إجازة عيد الفطر", "2025-03-13", "2025-04-05"),
    ("الدراسة بعد عيد الفطر", "2025-04-06", "2025-06-26"),
    ("الاعتذار عن مقرر", "2025-04-13", "2025-04-17"),
    ("الاختبارات البديلة", "2025-04-20", "2025-04-24"),
    ("الاختبارات النهائية", "2025-05-18", "2025-05-26"),
    ("تغيير التخصص", "2025-05-25", "2025-06-30"),
    ("إجازة عيد الأضحى", "2025-05-26", "2025-06-14"),
    ("الدراسة بعد عيد الأضحى", "2025-06-15", "2025-06-26"),
    ("استكمال الاختبارات", "2025-06-15", "2025-06-24"),
    ("اعتماد النتائج", "2025-06-25", "2025-06-25"),
    ("إجازة نهاية العام", "2025-06-26", "2025-08-23")
]

def get_calendar_buttons():
    today = datetime.date.today()
    buttons = []
    for event, start, end in calendar_events:
        start_date = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
        if today > end_date:
            label = f"❌ {event}"
        elif start_date > today:
            label = f"⏳ {event}"
        else:
            label = f"✅ {event}"
        buttons.append([label])
    buttons.append(["رجوع"])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def save_user(user):
    user_id = user.id
    username = user.username or "لا يوجد"
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    line = f"{user_id} - @{username} - {full_name}\n"

    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f:
            f.write(line)
    else:
        with open("users.txt", "r") as f:
            if str(user_id) not in f.read():
                with open("users.txt", "a") as fa:
                    fa.write(line)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.message.from_user)
    await update.message.reply_text("اختر من الأزرار:", reply_markup=reply_main)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.message.from_user)
    msg = update.message.text

    if msg == "موعد المكافأة":
        today = datetime.datetime.today()
        bonus = datetime.datetime(today.year, today.month, 26)
        if today.day > 26:
            bonus = bonus.replace(month=bonus.month % 12 + 1, year=today.year + (bonus.month // 12))
        remain = (bonus - today).days
        await update.message.reply_text(f"{bonus.strftime('%d/%m/%Y')}\nالمتبقي: {remain} يوم")

    elif msg == "أرقام التواصل":
        await update.message.reply_text("920002122")

    elif msg == "الأسئلة الشائعة":
        await update.message.reply_text("اختر سؤالًا:", reply_markup=reply_faq)

    elif msg == "كيف أسجل المواد؟":
        await update.message.reply_text(
            "المنظومة ثم التسجيل الإلكتروني:\n"
            "- إذا لم تحذف مادة: اختر تسجيل المجموعات الإلكترونية.\n"
            "- إذا حذفت أو حملت مادة: اختر الحذف والإضافة وحدد المقررات يدويًا."
        )

    elif msg == "رجوع":
        await update.message.reply_text("رجوع", reply_markup=reply_main)

    elif msg == "تقييم الدكاترة":
        await update.message.reply_text("https://t.me/tudoctors")

    elif msg == "منظومة الجامعة":
        await update.message.reply_text("https://edugate.tu.edu.sa")

    elif msg == "البلاك بورد":
        await update.message.reply_text("https://lms.tu.edu.sa")

    elif msg == "موقع الطلاب":
        await context.bot.send_location(chat_id=update.effective_chat.id, latitude=student_location[0], longitude=student_location[1])

    elif msg == "موقع الطالبات":
        await context.bot.send_location(chat_id=update.effective_chat.id, latitude=female_location[0], longitude=female_location[1])

    elif msg == "حفل التخرج":
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://www2.0zz0.com/2025/05/15/07/864959598.jpeg")

    elif msg == "التقويم الجامعي":
        await update.message.reply_text("أحداث التقويم:", reply_markup=get_calendar_buttons())

    else:
        for event, start, end in calendar_events:
            if msg in [f"❌ {event}", f"⏳ {event}", f"✅ {event}"]:
                await update.message.reply_text(f"{start} → {end}")
                return
        await update.message.reply_text("ضعت؟ ما لقيت أحد يرد عليك؟ ولا يهمك… أنا هنا عشانك، اختار من القائمة تحت.", reply_markup=reply_main)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()
