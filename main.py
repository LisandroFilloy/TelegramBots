import telebot
import datetime as dt
import pandas as pd
from statistics import mode

API_KEY = '2128358744:AAHk2RCqN89kR04RIWCrNgQob0sHn2LajNE'
bot = telebot.TeleBot(API_KEY)


def deudor(df):
    gastos_licha = df[df.autor == 'licha'].monto.sum()
    gastos_juli = df[df.autor == 'juli'].monto.sum()
    dif = abs(gastos_juli - gastos_licha)

    if gastos_juli > gastos_licha:
        return 'licha', dif
    else:
        return 'juli', dif


@bot.message_handler(commands=['licha', 'Licha'])
def gasto_licha(message):
    df_gastos = pd.read_csv('lista_gastos.csv')
    _fecha = str(dt.datetime.today())[:16]
    lista_mensaje = message.text.split(' ')

    try:
        ultimo_gasto = int(lista_mensaje[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    motivo = lista_mensaje[-2] if len(lista_mensaje) >= 2 else ''

    fila_gastos = {'monto': ultimo_gasto, 'autor': 'licha', 'motivo': motivo, 'fecha_de_creacion': _fecha}
    df_gastos.append(fila_gastos, ignore_index=True)
    df_gastos.to_csv('lista_gastos.csv')
    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


@bot.message_handler(commands=['juli', 'Juli'])
def gasto_juli(message):
    df_gastos = pd.read_csv('lista_gastos.csv')
    _fecha = str(dt.datetime.today())[:16]
    lista_mensaje = message.text.split(' ')

    try:
        ultimo_gasto = int(lista_mensaje[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    motivo = lista_mensaje[-2] if len(lista_mensaje) >= 2 else ''

    fila_gastos = {'monto': ultimo_gasto, 'autor': 'juli', 'motivo': motivo, 'fecha_de_creacion': _fecha}
    df_gastos.append(fila_gastos, ignore_index=True)
    df_gastos.to_csv('lista_gastos.csv')
    _deudor, _monto = deudor(df_gastos)
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


# @bot.message_handler(commands=['cerrar'])
# def cerrar_mes(message):
#     df_gastos = pd.read_csv('lista_gastos.csv')
#     _fecha = str(dt.datetime.today())[:16]
#
#     fechas = list(df_gastos['fecha_de_creacion'])
#     fechas = [int(x[5:7].replace('-', '')) for x in fechas]
#
#     mes = mode(fechas)
#     df_gastos.to_csv(f'gastos_{mes}.csv')
#
#     _deudor, _monto = deudor(df_gastos)
#
#     if _deudor == 'licha':
#         deuda = _monto + 10000
#         autor = 'juli'
#     else:
#         if _monto > 10000:
#             deuda = _monto - 10000
#             autor = 'licha'
#         else:
#             deuda = 10000 - _monto
#             autor = 'juli'
#
#     df_gastos = pd.DataFrame({'monto': deuda, 'autor': autor, 'motivo': 'deuda_mes_pasado',
#                               'fecha_de_creacion': _fecha})
#
#     df_gastos.to_csv('lista_gastos.csv')


bot.polling()
