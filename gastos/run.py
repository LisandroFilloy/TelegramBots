import telebot
import datetime as dt
import pandas as pd
from statistics import mode
import csv
import pdb
import os
from create_csv_lista_gastos import crear_lista_gastos

API_KEY = os.environ['GASTOS_API_KEY']
bot = telebot.TeleBot(API_KEY)


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
    df_gastos = pd.read_csv('lista_gastos.csv')
    _today = dt.datetime.today() - dt.timedelta(hours=3)
    _fecha = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    lista_mensaje = message.text.split(' ')

    try:
        ultimo_gasto = int(lista_mensaje[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    motivo = lista_mensaje[-2] if len(lista_mensaje) >= 3 else ''

    fila_gastos = {'monto': ultimo_gasto, 'autor': 'licha', 'motivo': motivo, 'fecha_de_creacion': _fecha}
    df_gastos = df_gastos.append(fila_gastos, ignore_index=True)
    df_gastos.to_csv('lista_gastos.csv', index=False)
    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


@bot.message_handler(commands=['juli', 'Juli'])
def gasto_juli(message):
    df_gastos = pd.read_csv('lista_gastos.csv')
    _today = dt.datetime.today() - dt.timedelta(hours=3)
    _fecha = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)
    lista_mensaje = message.text.split(' ')

    try:
        ultimo_gasto = int(lista_mensaje[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    motivo = lista_mensaje[-2] if len(lista_mensaje) >= 3 else ''

    fila_gastos = {'monto': ultimo_gasto, 'autor': 'juli', 'motivo': motivo, 'fecha_de_creacion': _fecha}
    df_gastos = df_gastos.append(fila_gastos, ignore_index=True)
    df_gastos.to_csv('lista_gastos.csv', index=False)
    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


@bot.message_handler(commands=['cerrar'])
def cerrar_mes(message):
    df_gastos = pd.read_csv('lista_gastos.csv')

    if df_gastos.empty:
        bot.send_message(message.chat.id, f"No hubo ningun gasto")
        return

    _today = dt.datetime.today() - dt.timedelta(hours=3)
    _fecha = '{}-{}-{} {}:{}'.format(_today.year, _today.month, _today.day, _today.hour, _today.minute)

    fechas = list(df_gastos['fecha_de_creacion'])
    fechas = [int(x[5:7].replace('-', '')) for x in fechas]
    mes = mode(fechas)
    saved_file_name = f'gastos_{mes}_{_fecha}.csv'
    df_gastos.to_csv(saved_file_name, index=False)

    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f'El mes cerro con {_deudor} adeudando {_monto}')

    with open(saved_file_name, 'rb') as doc:
        bot.send_document(message.chat.id, doc)

    os.remove('lista_gastos.csv')

    crear_lista_gastos()


bot.polling()
