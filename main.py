import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

TELEGRAM_TOKEN = os.environ.get("8135872395:AAEojpiYSPs91b-c98E67g7g9VCDrLTk2z8")
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n"
        "موضوع پستت رو بنویس، برات می‌سازم:\n\n"
        "📝 کپشن جذاب\n"
        "💡 ایده محتوا\n"
        "#️⃣ هشتگ‌های مرتبط\n\n"
        "مثال: کافه جدیدم رو افتتاح کردم"
    )

async def generate_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    await update.message.reply_text("⏳ در حال ساخت محتوا...")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""یه کپشن جذاب اینستاگرام فارسی برای این موضوع بنویس:
موضوع: {topic}

شامل اینا باشه:
- متن جذاب و احساسی (۳ تا ۵ خط)
- ۳ تا ۵ ایده محتوا برای پست‌های بعدی
- ۱۰ هشتگ مرتبط فارسی و انگلیسی
- یه call to action در آخر"""
        }]
    )

    await update.message.reply_text(response.content[0].text)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_caption))
app.run_polling()