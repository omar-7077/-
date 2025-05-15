from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import os

# قراءة التوكن من environment variable
TOKEN = os.environ["TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في البوت الجامعي!\n"
        "الأوامر المتاحة:\n"
        "/mokafa - موعد صرف المكافأة\n"
        "/contact - أرقام التواصل\n"
        "/faq - الأسئلة الشائعة\n"
        "/edugate - رابط منظومة الجامعة\n"
        "/blackboard - رابط البلاك بورد"
    )

async def mokafa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now()
    bonus_day = datetime(today.year, today.month, 26)
    if today > bonus_day:
        if today.month == 12:
            bonus_day = datetime(today.year + 1, 1, 26)
        else:
            bonus_day = datetime(today.year, today.month + 1, 26)
    days_left = (bonus_day - today).days
    await update.message.reply_text(
        f"موعد صرف المكافأة: {bonus_day.strftime('%d/%m/%Y')}\nالمتبقي: {days_left} يوم"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "للتواصل مع الجامعة:\n"
        "الهاتف: 920000000\n"
        "البريد الإلكتروني: info@tu.edu.sa"
    )

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أسئلة شائعة:\n"
        "1. هل يمكن تعديل الرغبات بعد الحفظ؟ نعم خلال فترة التقديم.\n"
        "2. هل القبول له أولوية حسب تاريخ التقديم؟ لا.\n"
        "3. ما الفرق بين الماجستير الأكاديمي والمهني؟ الأكاديمي للبحث، المهني للتطوير العملي."
    )

async def edugate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("رابط منظومة الجامعة: https://edugate.tu.edu.sa")

async def blackboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("رابط البلاك بورد: https://lms.tu.edu.sa")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mokafa", mokafa))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("edugate", edugate))
    app.add_handler(CommandHandler("blackboard", blackboard))
    app.run_polling()

if __name__ == "__main__":
    main()
