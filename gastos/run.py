import telebot
import datetime
import pandas as pd
import csv
import os

API_KEY = os.environ['GASTOS_API_KEY']
bot = telebot.TeleBot(API_KEY)
USER_ID_LICHA = 935301551
USER_ID_JULI = 1986869505
USER_ID_LIST = [935301551, 1986869505]


def formatted_date():
    sv_time = datetime.datetime.today()
    arg_time = sv_time - datetime.timedelta(hours=3)
    hour = arg_time.hour if len(str(arg_time.hour)) == 2 else int('0' + str(arg_time.hour))
    minute = arg_time.minute if len(str(arg_time.minute)) == 2 else int('0' + str(arg_time.minute))
    _date = '{}-{}-{} {}:{}'.format(arg_time.year, arg_time.month, arg_time.day, hour, minute)
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

    _date = formatted_date()
    lista_mensaje = message.text.split(' ')

    try:
        _amount = int(lista_mensaje[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    _description = lista_mensaje[-2] if len(lista_mensaje) >= 3 else ''

    with open('lista_gastos.csv', 'a') as lista_gastos:
        writer = csv.writer(lista_gastos)
        writer.writerow([_amount, 'licha', _description, _date])

    df_gastos = pd.read_csv('lista_gastos.csv')
    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


@bot.message_handler(commands=['juli', 'Juli'])
def gasto_juli(message):
    user_id = message.from_user.id
    if user_id not in USER_ID_LIST:
        bot.send_message(message.chat.id, 'Usuario no habilitado')
        return

    _date = formatted_date()
    message_list = message.text.split(' ')

    try:
        _amount = int(message_list[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    _description = message_list[-2] if len(message_list) >= 3 else ''

    with open('lista_gastos.csv', 'a') as lista_gastos:
        writer = csv.writer(lista_gastos)
        writer.writerow([_amount, 'juli', _description, _date])

    df_gastos = pd.read_csv('lista_gastos.csv')
    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


@bot.message_handler(commands=['borrarUltimo'])
def delete_last_row(message):
    user_id = message.from_user.id
    if user_id not in USER_ID_LIST:
        bot.send_message(message.chat.id, 'Usuario no habilitado')
        return

    with open('lista_gastos.csv', 'r+') as lista_gastos:
        lines = lista_gastos.readlines()
        lines.pop()

    with open('lista_gastos.csv', 'w+') as lista_gastos:
        lista_gastos.writelines(lines)

    bot.send_message(message.chat.id, 'Ultimo gasto borrado correctamente')


@bot.message_handler(commands=['id'])
def show_id(message):
    _id = message.from_user.id
    bot.send_message(message.chat.id, _id)


bot.infinity_polling()
