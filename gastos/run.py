import telebot
import datetime
import pandas as pd
from statistics import mode
import csv
import pdb
import os

from create_csv_lista_gastos import crear_lista_gastos

API_KEY = os.environ['GASTOS_API_KEY']
bot = telebot.TeleBot(API_KEY)
USER_ID_LICHA = 935301551
USER_ID_JULI = ''
USER_ID_LIST = [935301551]


def formatted_date():
    _today_sv = datetime.datetime.today()
    _today = _today_sv - datetime.timedelta(hours=3)
    _date = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    return _date


def deudor(df):
    gastos_licha = df[df.autor == 'licha'].monto.sum()
    gastos_juli = df[df.autor == 'juli'].monto.sum()
    dif = abs(gastos_juli - gastos_licha)

    if gastos_juli > gastos_licha:
        return 'licha', dif
    elif gastos_juli == gastos_licha:
        return 'ninguno', 0
    else:
        return 'juli', dif


@bot.message_handler(commands=['licha', 'Licha'])
def gasto_licha(message):
    user_id = message.from_user.id
    if user_id not in USER_ID_LIST:
        bot.send_message(message.chat.id, 'Usuario no habilitado')
        return

    df_gastos = pd.read_csv('lista_gastos.csv')
    _date = formatted_date()
    lista_mensaje = message.text.split(' ')

    try:
        _amount = int(lista_mensaje[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    _description = lista_mensaje[-2] if len(lista_mensaje) >= 3 else ''

    with open('lista_gastos.csv', 'w') as lista_gastos:
        writer = csv.writer(lista_gastos)
        writer.writerow([_amount, 'licha', _description, _date])

    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


@bot.message_handler(commands=['juli', 'Juli'])
def gasto_juli(message):
    user_id = message.from_user.id
    if user_id not in USER_ID_LIST:
        bot.send_message(message.chat.id, 'Usuario no habilitado')
        return

    df_gastos = pd.read_csv('lista_gastos.csv')
    _date = formatted_date()
    message_list = message.text.split(' ')

    try:
        _amount = int(message_list[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    _description = message_list[-2] if len(message_list) >= 3 else ''

    with open('lista_gastos.csv', 'w') as lista_gastos:
        writer = csv.writer(lista_gastos)
        writer.writerow([_amount, 'juli', _description, _date])

    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


@bot.message_handler(commands=['cerrar'])
def cerrar_mes(message):
    user_id = message.from_user.id
    if user_id not in USER_ID_LIST:
        bot.send_message(message.chat.id, 'Usuario no habilitado')
        return

    df_gastos = pd.read_csv('lista_gastos.csv')

    if df_gastos.empty:
        bot.send_message(message.chat.id, f"No hubo ningun gasto")
        return

    _date = formatted_date()

    fechas = list(df_gastos['fecha_de_creacion'])
    fechas = [int(x[5:7].replace('-', '')) for x in fechas]
    mes = mode(fechas)
    saved_file_name_total = f'gastos_{mes}_{_date}.csv'
    saved_file_name_licha = f'gastos_{mes}_{_date}_licha.csv'
    saved_file_name_juli = f'gastos_{mes}_{_date}_juli.csv'
    df_gastos.to_csv(saved_file_name_total, index=False)
    df_gastos[df_gastos.autor.isin(['licha', 'licha_individual'])].to_csv(saved_file_name_licha)
    df_gastos[df_gastos.autor.isin(['juli', 'juli_individual'])].to_csv(saved_file_name_juli)

    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f'El mes cerro con {_deudor} adeudando {_monto}')

    with open(saved_file_name_total, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

    with open(saved_file_name_licha, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

    with open(saved_file_name_juli, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

    os.remove('lista_gastos.csv')

    crear_lista_gastos()


@bot.message_handler(commands=['lichaIndividual'])
def gasto_individual_licha(message):
    user_id = message.from_user.id
    if user_id != USER_ID_LICHA:
        bot.send_message(message.chat.id, 'Usuario no habilitado')
        return

    _date = formatted_date()
    _message_list = message.text.split(' ')
    _description = ''
    if len(_message_list == 3):
        _description = _message_list[1]

    try:
        _amount = int(_message_list[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Olvidaste anotar el monto')
        return

    with open('lista_gastos.csv', 'w') as lista_gastos:
        writer = csv.writer(lista_gastos)
        writer.writerow([_amount, 'licha_individual', _description, _date])

    bot.send_message(message.chat.id, 'Pago cargado correctamente')


@bot.message_handler(commands=['juliIndividual'])
def gasto_individual_juli(message):
    user_id = message.from_user.id
    if user_id != USER_ID_JULI:
        bot.send_message(message.chat.id, 'Usuario no habilitado')
        return

    _date = formatted_date()
    _message_list = message.text.split(' ')
    _description = ''
    if len(_message_list == 3):
        _description = _message_list[1]

    try:
        _amount = int(_message_list[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Olvidaste anotar el monto')
        return

    with open('lista_gastos.csv', 'w') as lista_gastos:
        writer = csv.writer(lista_gastos)
        writer.writerow([_amount, 'juli_individual', _description, _date])

    bot.send_message(message.chat.id, 'Pago cargado correctamente')


@bot.message_handler(commands=['id'])
def show_id(message):
    _id = message.from_user.id
    bot.send_message(message.chat.id, _id)


bot.polling()
