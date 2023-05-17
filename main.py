from config import TOKEN
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, filters, MessageHandler, ConversationHandler
import bot
from bot import *

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Crea un comando llamado start
    # que es manejado por la función start
    dispatcher.add_handler(CommandHandler('start', bot.start))
    dispatcher.add_handler(CommandHandler('menu', bot.menu))
    dispatcher.add_handler(CallbackQueryHandler(bot.stars, pattern='estrellitas'))
    dispatcher.add_handler(CallbackQueryHandler(bot.ver_todas, pattern='all'))
    dispatcher.add_handler(CallbackQueryHandler(bot.ver_constelacion, pattern='constellation'))
    dispatcher.add_handler(CallbackQueryHandler(bot.ver_estrellas, pattern='stars'))
    dispatcher.add_handler(CallbackQueryHandler(bot.cargar_constelacion))

    # help
    dispatcher.add_handler(CommandHandler('help', bot.help))

    recurrence_handler = ConversationHandler(
    entry_points=[CommandHandler('rsolve', rsolve)],
    states={
        RECURRENCE: [MessageHandler(
            filters.Filters.text & ~filters.Filters.command, get_initial_values)],
        INITIAL_VALUES: [MessageHandler(
            filters.Filters.text & ~filters.Filters.command, show_rsolved)]
    },
    fallbacks=[CommandHandler('cancel', cancel_rsolve)],
    )
    dispatcher.add_handler(recurrence_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
