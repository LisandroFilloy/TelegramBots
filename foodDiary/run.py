import telebot
import sqlite3
import datetime
import os


API_KEY = os.environ['FOOD_DIARY_API_KEY']
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['comida'])
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
    insert_query = f"""INSERT INTO foods VALUES ('{_date}', '{_description}')"""
    cursor.execute(insert_query)
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Comida cargada con éxito')


@bot.message_handler(commands=['suplemento'])
def supplement(message):
    _today = datetime.datetime.today()
    _date = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    _text = message.text.lower()
    _description = _text.replace('/suplemento ', '')

    connector = sqlite3.connect('food_diary_database.db')
    cursor = connector.cursor()
    cursor.execute(f"""INSERT INTO supplements VALUES ('{_date}', '{_description}')""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Suplemento cargado con exito')


@bot.message_handler(commands=['deposicion'])
def deposition(message):
    _today = datetime.datetime.today()
    _date = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    _text = message.text.lower()

    bristol_level = _text.split(' ')[-1]

    try:
        bristol_level = int(bristol_level)
    except ValueError:
        bot.send_message(message.chat.id, 'Recordá indicar escala Bristol')
        return

    connector = sqlite3.connect('food_diary_database.db')
    cursor = connector.cursor()
    cursor.execute(f"""INSERT INTO depositions VALUES ('{_date}', '{bristol_level}')""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Deposición cargada con éxito')


@bot.message_handler(commands=['sintoma', 'síntoma'])
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
    cursor.execute(f"""INSERT INTO symptoms VALUES ('{_date}', '{_description}')""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Síntoma cargado con éxito')


@bot.message_handler(commands=['comentario'])
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
    cursor.execute(f"""INSERT INTO comments VALUES ('{_date}', '{_description}')""")
    connector.commit()
    connector.close()

    bot.send_message(message.chat.id, 'Comentario cargado con éxito')


@bot.message_handler(func=(lambda x: True if '/id' in str(x).lower() else False))
def id(message):
    x = message.from_user.id
    bot.send_message(message.chat.id, x)


bot.polling()


