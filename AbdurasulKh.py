import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_BOT_TOKEN = "8608715194:AAF6ZkPSBC9LYEzC7TxhIu9cdkh4T17CeEc"
GEMINI_API_KEY = "AQ.Ab8RN6KE0t4ggwbfJx9Ci6VBzHQvFgsOkgc2MctBcbGUVtkhEQ"

genai.configure(api_key=GEMINI_API_KEY)

# Botga xuddi aqlli AI yordamchi kabi muloqot qilish va chiroyli formatlash ko'rsatmasi
system_instruction = (
    "Siz aqlli, samimiy va tajribali sun'iy intellekt yordamchisisiz. "
    "Muloqotni har doim o'zbek tilida, do'stona, aniq va ravon olib boring.\n\n"
    "MATEMATIKA VA FIZIKA JAVOBLARI UCHUN SHARTLAR:\n"
    "1. HECH QACHON LaTeX belgilaridan foydalanmang (masalan: $$, \\frac, \\times, \\cdot, \\sqrt va h.k. belgilar TAQIQLANADI).\n"
    "2. Amallarni va sonlarni oddiy, odamlar chatda yozishadigan tushunarli matn shaklida yozing:\n"
    "   - Kasrlarni: '55 / 22' deb yozing.\n"
    "   - Ko'paytirishni: '*' yoki 'x' deb yozing.\n"
    "   - Darajalarni: '^' belgisi bilan (masalan: x^2) yozing.\n"
    "3. Masalalarni bosqichma-bosqich, 1-qadam, 2-qadam qilib, o'qishga juda qulay, chiroyli va tartibli tushuntiring.\n"
    "4. Javob so'ngida aniq yakuniy natijani ajratib ko'rsating."
)

model = genai.GenerativeModel(
    'gemini-3.8-flash',
    system_instruction=system_instruction
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Salom! Men Abdurasul tomonidan yaratilgan sun'iy intellektman.\n\n"
        "Matematika, fizika va boshqa barcha sohalarda savollaringizga aniq hamda tushunarli javob beraman. "
        "Qanday yordam bera olaman?"
    )
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(user_text))
        ai_reply = response.text
    except Exception as e:
        print(f"Xatolik: {e}")
        ai_reply = f"Kechirasiz, xatolik yuz berdi: {e}"

    await update.message.reply_text(ai_reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot xuddi aqlli AI uslubida ishga tushdi...")
    app.run_polling()