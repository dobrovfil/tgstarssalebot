import os
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))


bot = Bot(token=TOKEN)


# Главное меню
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("💰 Купить звезды", callback_data="buy_stars")],
                [InlineKeyboardButton("👥 Партнерская программа", callback_data="ref_program")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! Выберите действие:", reply_markup=reply_markup)


# Покупка звёзд
def buy_stars(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("💰 Выберите способ оплаты:\n1️⃣ TON\n2️⃣ USDT\n3️⃣ СБП / Карты РФ\n\nОтправьте сумму звёзд, которую хотите купить (от 50):")


# Подтверждение платежа админом
def confirm_payment(update: Update, context: CallbackContext):
    if update.message.from_user.id == ADMIN_ID:
        update.message.reply_text("Введите ID пользователя и сумму, чтобы отправить звезды.")
    else:
        update.message.reply_text("У вас нет прав для этой команды.")


# Партнёрская программа
def ref_program(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    ref_link = f"https://t.me/YOUR_BOT_USERNAME?start=ref{query.from_user.id}"
    query.edit_message_text(f"💸 Привлекайте новых пользователей и зарабатывайте!\n\n🔗 Ваша реферальная ссылка: {ref_link}")


# Обработчик команд
def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("confirm", confirm_payment))
    application.add_handler(CallbackQueryHandler(buy_stars, pattern="buy_stars"))
    application.add_handler(CallbackQueryHandler(ref_program, pattern="ref_program"))
    
    application.run_polling()


if __name__ == "__main__":
    main()