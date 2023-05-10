from config import TOKEN
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import bot
import recurrencia

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

    # # Comandos relacionados con relaciones de recurrencia
    # dispatcher.add_handler(CommandHandler('recurrence_menu', bot.recurrence_menu))
    # dispatcher.add_handler(CommandHandler('calculate_sequence', recurrencia.calculate_sequence))
    # dispatcher.add_handler(CommandHandler('calculate_value', recurrencia.calculate_value))
    # dispatcher.add_handler(CommandHandler('calculate_limit', recurrencia.calculate_limit))

    # help
    dispatcher.add_handler(CommandHandler('help', bot.help))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
