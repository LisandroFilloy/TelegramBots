import telebot
import sqlite3
import datetime
import os


API_KEY = os.environ['FOOD_DIARY_API_KEY']
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(func=(lambda x: True if str(x).lower() == 'comida' else False))
def food(message):
    _today = datetime.datetime.today()
    _date = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    _text = message.text.lower()
    _description = _text.replace('/comida ', '')

    if not _description:
        bot.send_message(message.chat.id, 'Recordá cargar la descripción')
        return

    connector = sqlite3.connect('food_diary_database.db')
    cursor = connector.cursor()
    cursor.execute(f"""INSERT INTO foods VALUES ({_date}, {_description})""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Comida cargada con éxito')


@bot.message_handler(func=(lambda x: True if str(x).lower() == 'suplemento' else False))
def supplement(message):
    _today = datetime.datetime.today()
    _date = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    _text = message.text.lower()
    message = _text.replace('/suplemento ', '')

    connector = sqlite3.connect('food_diary_database.db')
    cursor = connector.cursor()
    cursor.execute("""CREATE TABLE foods
                      (date text, description text)""")
    cursor.execute(f"""INSERT INTO foods VALUES ({_date}, {message})""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Suplemento cargado con exito')


@bot.message_handler(func=(lambda x: True if str(x).lower() == 'deposicion' else False))
def deposition(message):
    _today = datetime.datetime.today()
    _date = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    _text = message.text.lower()

    if len(_text.split(' ') != 3):
        bot.send_message(message.chat.id, 'Deposición mal cargada')
        return

    bristol_level = _text.split(' ')[-1]

    try:
        bristol_level = int(bristol_level)
    except ValueError:
        bot.send_message(message.chat.id, 'Recordá indicar escala Bristol')
        return

    connector = sqlite3.connect('food_diary_database.db')
    cursor = connector.cursor()
    cursor.execute(f"""INSERT INTO depositions VALUES ({_date}, {bristol_level})""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Deposición cargada con éxito')


@bot.message_handler(func=(lambda x: True if str(x).lower().replace('í', 'i') in ['sintoma'] else False))
def sintoma(message):
    _today = datetime.datetime.today()
    _date = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    _text = message.text.lower().replace('í', 'i')
    _description = _text.replace('/sintoma ', '')

    if not _description:
        bot.send_message(message.chat.id, 'Recordá cargar la descripción')
        return

    connector = sqlite3.connect('food_diary_database.db')
    cursor = connector.cursor()
    cursor.execute(f"""INSERT INTO symptoms VALUES ({_date}, {_description})""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Síntoma cargado con éxito')


@bot.message_handler(func=(lambda x: True if str(x).lower() in ['comentario'] else False))
def comentario(message):
    _today = datetime.datetime.today()
    _date = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    _text = message.text.lower()
    _description = _text.replace('/comentario ', '')

    if not _description:
        bot.send_message(message.chat.id, 'Recordá cargar la descripción')
        return

    connector = sqlite3.connect('food_diary_database.db')
    cursor = connector.cursor()
    cursor.execute(f"""INSERT INTO comments VALUES ({_date}, {_description})""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Comentario cargado con éxito')


@bot.message_handler(func=(lambda x: True if '\id' in str(x).lower()  else False))
def id(message):
    x = message.from_user.id
    bot.send_message(message.chat.id, x)


bot.polling()


