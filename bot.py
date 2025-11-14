from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from handlers import (
    start_handler,
    help_handler,
    text_handler,
    photo_handler,
    main_menu_handler,
    language_toggle_handler,
    callback_query_handler,
)

TOKEN = "8581103233:AAG_CWCu2gAZGoyOIGZ6DUZcUZVLkTZsl2Y" 

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CallbackQueryHandler(callback_query_handler))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^Bosh Sahifa$'), main_menu_handler))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^Main Menu$'), main_menu_handler))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^Til tugmasi$'), language_toggle_handler))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^Language$'), language_toggle_handler))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(MessageHandler(filters.TEXT, text_handler))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
