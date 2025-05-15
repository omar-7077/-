import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputFile
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TOKEN = "7597887705:AAEQr0g_aWxoZb6o1QC5geKZ3GzCBQtl7fY"

# بيانات المكافأة
def calculate_bonus():
    today = datetime.date.today()
    bonus_day = 26
    if today.day > bonus_day:
        next_month = today.replace(day=28) + datetime.timedelta(days=4)
        next_bonus = next_month.replace(day=bonus_day)
    else:
        next_bonus = today.replace(day=bonus_day)
    remaining = (next_bonus - today).days
    return f"موعد صرف المكافأة: {next_bonus.strftime('%d/%m/%Y')}\nالمتبقي: {remaining} يوم"

# بيانات التقويم الأكاديمي
calendar = [
    {"label": "طلب إعادة القيد", "from": "2025/01/05", "to": "2025/01/18"},
    {"label": "تأجيل الدراسة", "from": "2025/01/05", "to": "2025/01/14"},
    {"label": "استقبال طلبات الزيارة", "from": "2025/01/05", "to": "2025/01/16"},
    {"label": "بداية الدراسة للفصل الدراسي الثاني", "from": "2025/01/12", "to": "2025/06/26"},
    {"label": "الإعتذار عن الدراسة", "from": "2025/01/19", "to": "2025/05/10"},
    {"label": "الاختبارات النهائية", "from": "2025/05/18", "to": "2025/05/26"},
]

# تحديد حالة التاريخ
def get_date_status(start, end):
    today = datetime.date.today()
    start_date = datetime.datetime.strptime(start, "%Y/%m/%d").date()
    end_date = datetime.datetime.strptime(end, "%Y/%m/%d").date()
    if end_date < today:
        return "❌ منتهي"
    elif start_date > today:
        return "⏳ قادم"
    elif start_date <= today <= end_date:
        return "✅ جاري"
    return "❔"

# عرض القائمة الرئيسية
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("موعد المكافأة", callback_data='bonus'), InlineKeyboardButton("أرقام التواصل", callback_data='contact')],
        [InlineKeyboardButton("الأسئلة الشائعة", callback_data='faq'), InlineKeyboardButton("تقييم الدكاترة", url="https://t.me/tudoctors")],
        [InlineKeyboardButton("منظومة الجامعة", url="https://edugate.tu.edu.sa")],
        [InlineKeyboardButton("البلاك بورد", url="https://lms.tu.edu.sa")],
        [InlineKeyboardButton("موقع جامعة الطلاب", url="https://maps.app.goo.gl/SJ2vYZt9wiqQYkx89?g_st=com.google.maps.preview.copy"),
         InlineKeyboardButton("موقع جامعة الطالبات", url="https://maps.app.goo.gl/BPwmcoQ7T16CT2FX8?g_st=com.google.maps.preview.copy")],
        [InlineKeyboardButton("حفل التخرج", callback_data='graduation')],
        [InlineKeyboardButton("التقويم الجامعي", callback_data='calendar')],
        [InlineKeyboardButton("دليل التخصصات", callback_data='majors')],
        [InlineKeyboardButton("قروب بيع الكتب", url="https://t.me/bookTaifUniversity")],
        [InlineKeyboardButton("قروب الفصل الصيفي", url="https://t.me/summerTaifUniversity")],
        [InlineKeyboardButton("قروبات الكليات", callback_data="faculties")],
        [InlineKeyboardButton("قروبات الفروع", callback_data="branches")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("ضعت؟ ما لقيت احد يرد عليك؟ ولا يهمك\nانا هنا عشانك", reply_markup=reply_markup)

# استجابة الضغطات
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "bonus":
        await query.edit_message_text(text=calculate_bonus())
    elif query.data == "contact":
        await query.edit_message_text("للتواصل مع الجامعة:\nالهاتف: 920002122")
    elif query.data == "faq":
        keyboard = [
            [InlineKeyboardButton("كيف أسجل المواد؟", callback_data='faq_register')],
            [InlineKeyboardButton("رجوع", callback_data='back')]
        ]
        await query.edit_message_text("اختر السؤال:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "faq_register":
        await query.edit_message_text(
            "ادخل منظومة الجامعة ثم التسجيل الإلكتروني.\n"
            "- إذا لم تحذف مادة: اختر 'تسجيل المجموعات الإلكترونية'.\n"
            "- إذا سبق أن حذفت أو حملت مادة: اختر 'الحذف والإضافة' واختر يدويًا."
        )
    elif query.data == "calendar":
        keyboard = [[InlineKeyboardButton(f"{item['label']} ({get_date_status(item['from'], item['to'])})", callback_data=f"cal_{i}")] for i, item in enumerate(calendar)]
        keyboard.append([InlineKeyboardButton("❌ = منتهي | ✅ = جاري | ⏳ = قادم", callback_data="cal_info")])
        await query.edit_message_text("اختر الإجراء:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith("cal_") and query.data != "cal_info":
        i = int(query.data.split("_")[1])
        item = calendar[i]
        remaining = (datetime.datetime.strptime(item["to"], "%Y/%m/%d").date() - datetime.date.today()).days
        await query.edit_message_text(f"{item['label']}\nمن {item['from']} إلى {item['to']}\nالمتبقي: {remaining} يوم")
    elif query.data == "cal_info":
        await query.edit_message_text("❌ = منتهي | ✅ = جاري | ⏳ = قادم")
    elif query.data == "graduation":
        await query.message.reply_photo(photo=open("graduation.jpg", "rb"))
    elif query.data == "majors":
        await query.message.reply_document(document=InputFile("files/دليل التخصصات١٤٤٦هـ.pdf"))
    elif query.data == "faculties":
        keyboard = [
            [InlineKeyboardButton("كلية التربية", url="https://t.me/educationTaifUniversity")],
            [InlineKeyboardButton("الكلية التطبيقية", url="https://t.me/appliedstudiesTaifUniversity")],
            [InlineKeyboardButton("كلية العلوم", url="https://t.me/TaifUnivierstiy1")],
            [InlineKeyboardButton("كلية الهندسة", url="https://t.me/engineeringTaifUniversity")],
            [InlineKeyboardButton("كلية الحاسبات", url="https://t.me/computersTaifUniversity")],
            [InlineKeyboardButton("كلية الشريعة", url="https://t.me/+TKCYp3jPayCyUgSw")],
            [InlineKeyboardButton("كلية الطب", url="https://t.me/medicine_Tu")],
            [InlineKeyboardButton("كلية طب الأسنان", url="https://t.me/Dentistry_TU")],
            [InlineKeyboardButton("التمريض", url="https://t.me/nursstudent")],
            [InlineKeyboardButton("رجوع", callback_data='back')]
        ]
        await query.edit_message_text("اختر الكلية:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "branches":
        keyboard = [
            [InlineKeyboardButton("فرع تربة", url="https://t.me/+LTvqFqmbNhU3Nzg0")],
            [InlineKeyboardButton("فرع الخرمة", url="https://t.me/+TI4sw9271iJhNDU0")],
            [InlineKeyboardButton("فرع رنية", url="https://t.me/+LhI_BEwURHNlNGZk")],
            [InlineKeyboardButton("رجوع", callback_data='back')]
        ]
        await query.edit_message_text("اختر الفرع:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "back":
        await start(update, context)

# رسالة أي شيء غير الأوامر
async def fallback(update: Update, context: CallbackContext):
    await start(update, context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT, fallback))
    app.run_polling()
