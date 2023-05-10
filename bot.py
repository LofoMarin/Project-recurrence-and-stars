from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os.path
from model import Modelo

m = Modelo()


# --------------------- Comandos -----------------------------

# def para iniciar el bot
def start(update, context):
    try:
        update.message.reply_text('¡Hola! Bienvenido(a), soy un bot que te ayudará a visualizar'
                                  ' lo impresionante que es el universo con sus estrellas'
                                  ' y constelaciones. %s %s\n\nSi quieres ver qué puedo hacer '
                                  'solamente tienes que ejecutar el comando /menu.' % (u'\U0001F60A', u'\U0001F31F'))
    except Exception as e:
        print('Error en start: ', e)

# def para mostrar el menú
def menu(update, context):
    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())


# -------------------- Keyboards -------------------------
# def para mostrar el menú principal
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('Las estrellas', callback_data='stars')],
        [InlineKeyboardButton('Estrellas y una constelación', callback_data='constellation')],
        [InlineKeyboardButton('Quiero ver las estrellas y constelaciones', callback_data='all')]
    ]
    return InlineKeyboardMarkup(keyboard)

# def para mostrar el menú de constelaciones
def constellation_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('1', callback_data='Boyero'),
            InlineKeyboardButton('2', callback_data='Casiopea'),
            InlineKeyboardButton('3', callback_data='Cazo'),
            InlineKeyboardButton('4', callback_data='Cygnet')
        ],
        [
            InlineKeyboardButton('5', callback_data='Geminis'),
            InlineKeyboardButton('6', callback_data='Hydra'),
            InlineKeyboardButton('7', callback_data='Osa Mayor'),
            InlineKeyboardButton('8', callback_data='Osa Menor')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# ----------------- Messages ----------------
#  Mensaje para el menú principal
def main_menu_message():
    return 'Por favor, hazme saber qué te gustaría ver %s:' % u'\U0001F914'

# Mensaje para el menú de constelaciones
def constellation_menu_message():
    return '''Selecciona el botón correspondiente a la constelación que deseas ver: 
                1.  Boyero
                2.  Casiopea
                3.  Cazo
                4.  Cygnet
                5.  Geminis
                6.  Hydra
                7.  Osa Mayor
                8.  Osa Menor'''


# --------------------------------------------------------
# ----------------- Callbacks ----------------------------
# def para mostrar las estrellas
def ver_estrellas(update, context):
    try:
        query = update.callback_query
        chat_id = query.message.chat.id
        query.edit_message_text(text="¡Listo! Te mostraré las estrellas.")
        if not os.path.isfile('generated/stars.png'):
            m.plot_stars()
        context.bot.send_photo(chat_id, open('generated/stars.png', 'rb'))
    except Exception as e:
        print('Error:', e)

# def para mostrar todas las estrellas y constelaciones
def ver_todas(update, context):
    try:
        chat_id = update.callback_query.message.chat.id
        query = update.callback_query
        query.edit_message_text(text="¡Fantástico! Observa todas las estrellas y constelaciones.")
        if not os.path.isfile('generated/all.png'):
            m.plot_stars_and_constellations()
        context.bot.send_photo(chat_id, open('generated/all.png', 'rb'))
    except Exception as e:
        print('Error:', e)

# def para mostrar una constelación
def ver_constelacion(update, context):
    try:
        chat_id = update.callback_query.message.chat.id
        query = update.callback_query
        query.edit_message_text(text="¡Genial! Ahora necesito que me indiques cuál constelación"
                                     " deseas que te muestre %s:" % u'\U0001F914')
        update.callback_query.message.reply_text(text=constellation_menu_message(),
                                                 reply_markup=constellation_menu_keyboard())
    except Exception as e:
        print('Error:', e)

# def para cargar la constelación seleccionada
def cargar_constelacion(update, context):
    try:
        query = update.callback_query
        chat_id = query.message.chat.id
        constellation = query.data.upper()
        query.edit_message_text(text=f"¡Excelente! has seleccionado {query.data}")
        query.message.reply_text(text='¿Sabías que?\n%s' % get_dato_interesante(constellation))
        path = f'generated/{constellation}.png'
        if not os.path.isfile(path):
            m.plot_stars_and_constellation(constellation)
        context.bot.send_photo(chat_id, open(path, 'rb'))
    except Exception as e:
        print('Error:', e)

# def para mostrar datos interesantes de la constelación
def get_dato_interesante(constellation):
    if constellation == 'OSA MAYOR':
        return 'La Osa Mayor es la tercera constelación más grande, ocupando el 3.102% ' \
               'del cielo nocturno, y se distingue fácilmente por medio de un notable ' \
               'cúmulo de estrellas brillantes en los cielos del norte, formando ' \
               'lo que se conoce familiarmente como \"The Dipper\"'
    elif constellation == 'OSA MENOR':
        return 'La Osa Menor es una de las constelaciones más importantes para los' \
               ' astrónomos. Situada en el hemisferio norte, la Osa Menor es visible' \
               ' desde Europa durante todo el año. Su estrella principal es Polaris, ' \
               'para los astrónomos una de las más importantes ya que muchos otros cuerpos' \
               ' celestes utilizan a la estrella como un eje para girar. Además, Polaris ' \
               'también recibe un rol importante en la leyenda de los indios Vedas, en donde' \
               ' es el líder de un grupo de dioses.'
    elif constellation == 'BOYERO':
        return 'Bootes o el Boyero es una de las 88 constelaciones modernas y era una de' \
               ' las 48 constelaciones listadas por Ptolomeo. Bootes parece ser una figura' \
               ' humana grande, mirando hacia la Osa Mayor.'
    elif constellation == 'CASIOPEA':
        return 'En 1572 Tycho Brahe observó una supernova en Casiopeia. Más tarde, en el' \
               ' siglo XVII, se intentó cambiar el nombre de la constelación por María' \
               ' Magdalena, pero la propuesta nunca prevaleció.'
    elif constellation == 'CAZO':
        return 'El Gran Cazo no es por sí misma una constelación. Cinco de las estrellas' \
               ' del Gran Cazo están realmente cerca una de la otra en el espacio y fueron' \
               ' probablemente formadas casi al mismo tiempo.'
    elif constellation == 'CYGNET':
        return 'La constelación Cygnet o Cygnus (El Cisne) es también conocida como \'La' \
               ' Cruz del Norte\'. Al estar en medio de la Vía Láctea, esta constelación' \
               ' tiene bastantes objetos de cielo profundo muy interesantes que son' \
               ' codiciados por los astrofotógrafos.'
    elif constellation == 'GEMINIS':
        return 'La constelación Geminis lleva el nombre de los gemelos Castor y Pólux' \
               ' de la mitología griega. Las dos estrellas más brillantes representan' \
               ' las cabezas de Castor y Pollux y los demás forman los cuerpos.'
    elif constellation == 'HYDRA':
        return 'Hydra es la más grande de las 88 constelaciones modernas, y fue' \
               ' una de las 48 constelaciones que Ptolomeo registró. No debe ser' \
               ' confundida con Hydrus, constelación del hemisferio sur de menor tamaño.'
    return ''

def help(update, context):
    update.message.reply_text(text='¡Hola! Soy el bot de Astronomía. '
                                   'Puedes usar los siguientes comandos:\n'
                                   '/start: Inicia la conversación con el bot.\n'
                                   '/help: Muestra los comandos disponibles.\n')