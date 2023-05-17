from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import os.path
from model import Modelo
from recurrencia import *
import re
import sympy as sp

m = Modelo()

# --------------------- Comandos -----------------------------
# def para iniciar el bot
def start(update, context):
    try:
        message = '¡Hola! Bienvenido(a), soy un bot que te ayudará a visualizar ' \
                  'lo impresionante que es el universo con sus estrellas ' \
                  'y constelaciones. También puedo ayudarte a resolver relaciones ' \
                  'de recurrencia tanto homogeneas como no homgeneas. 😊🌟\n\nSi quieres ver qué puedo hacer, ' \
                  'solamente tienes que ejecutar el comando /menu.'
        update.message.reply_text(message)
    except Exception as e:
        print('Error en start:', e)

# def para mostrar el menú
def menu(update, context):
    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())

# -------------------- Keyboards -------------------------
# def para mostrar el menú principal
def main_menu_estrellitas():
    keyboard = [
        [InlineKeyboardButton('Las Estrellitas', callback_data='stars')],
        [InlineKeyboardButton('Las Estrellitas y una Constelacion', callback_data='constellation')],
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

def main_menu_keyboard():
    menup = [
            [InlineKeyboardButton('Estrellitas', callback_data='estrellitas')],
            [InlineKeyboardButton('Relaciones de Recurrencia', callback_data='RR')]
    ]
    return InlineKeyboardMarkup(menup)

# ----------------- Messages ----------------
#  Mensaje para el menú principal
def main_menu_message():
    return 'Por favor, hazme saber qué te gustaría ver %s:' % u'\U0001F914'

def main_menu_message_stars():
    return 'Cuentame, ¿qué te gustaría ver? %s:' % u'\U0001F914'
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
        query.edit_message_text(text="Aqui te muestro las estrellas 🌠")
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

# def para mostrar menu si estrella o RR
def stars(update, context):
    try:
        chat_id = update.callback_query.message.chat.id
        query = update.callback_query
        query.edit_message_text(text="Ahora necesito que me indiques que quieres ver en las estrellas %s:" % u'\U0001F914')
        update.callback_query.message.reply_text(text=main_menu_message_stars(),
                                                 reply_markup=main_menu_estrellitas())
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
                                   '/menu: Muestra el menú de opciones.\n'
                                   '/help: Muestra los comandos disponibles.\n')

RECURRENCE, INITIAL_VALUES = range(2)

def rsolve(update, context):
    '''
    Recurrence relation solver input
    '''

    response = '''
    🔢 Enter the recurrence relation you want to solve. It has to be linear, homogeneous or non-homogeneous and with constant coefficients.

Try to write the function this way:
f(n) = c_1*f(n-1) + c_2*f(n-2) + ... + g(n)    '''

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return RECURRENCE

def latex_img(equation):
    '''
    Render a equation in latex
    '''

    import requests
    from io import BytesIO

    response = requests.get(
        'http://latex.codecogs.com/png.latex?\dpi{{1200}} {formula}'.format(formula=equation))

    # Get the HTTP requested image
    imagen_bytes = BytesIO(response.content)

    return imagen_bytes

def valores_iniciales(update, context):
    '''
    Initial values input
    '''

    response_1 = '''
    You entered the following function:
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_1)

    # Get the function from the user
    function_from_user = update.message.text.split("=")[1]
    context.chat_data['fn'] = function_from_user
    parsed_function = 'f(n) =' + sp.latex(sp.parse_expr(function_from_user))

    # Transform the parsed function to image (latex rendered)
    img = latex_img(parsed_function)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)

    response_2 = '''
    Now, give me the initial values like this:
f(0) = 1, f(1) = 2, ...
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_2)

    return INITIAL_VALUES

def rsol_mostrar(update, context):
    '''
    Show final result
    '''

    # Retrieve the function asked previously
    function_from_user = context.chat_data['fn']
    initial_conditions = update.message.text

    # Process the function
    solution = solve_recurrence(function_from_user, initial_conditions)

    response_1 = '''
    🧠 La no recurrente es:
    '''
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_1)

    img = latex_img(solution)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=img)

    return ConversationHandler.END

def cancel_rsolve(update, context):
    """
    Cancel option
    """

    response = "❌ Cancelled!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def prueba(update, context):
    '''
    Prueba
    '''

    response = ("Por favor dale click aqui %s /rsolve" % u'\U0001f449')
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)