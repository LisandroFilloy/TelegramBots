import telebot
import datetime as dt

API_KEY = '2128358744:AAHk2RCqN89kR04RIWCrNgQob0sHn2LajNE'
bot = telebot.TeleBot(API_KEY)
gastos_licha = []
gastos_juli = [10000]


def deudor(gastosLicha, gastosJuli):
    if gastosLicha < gastosJuli:
        return "Licha"
    else:
        return "Juli"


@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Hey, how's it going?")


@bot.message_handler(commands=['Hello', 'Hi'])
def greet(message):
    bot.send_message(message.chat.id, "Hello")


@bot.message_handler(commands=['licha'])
def gasto_licha(message):
    _today = dt.datetime.today()
    lista_mensaje = message.text.split(' ')

    try:
        ultimo_gasto = int(lista_mensaje[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    gastos_licha.append(ultimo_gasto)
    _deudor = deudor(gastos_licha, gastos_juli)
    _monto = abs(sum(gastos_licha) - sum(gastos_juli))
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto} - {_today}")


@bot.message_handler(commands=['juli'])
def gasto_juli(message):
    lista_mensaje = message.text.split(' ')

    try:
        ultimo_gasto = int(lista_mensaje[-1].replace('$', ''))
    except ValueError:
        bot.send_message(message.chat.id, 'Hay un error en el monto')
        return

    gastos_juli.append(ultimo_gasto)
    _deudor = deudor(gastos_licha, gastos_juli)
    _monto = abs(sum(gastos_licha) - sum(gastos_juli))
    bot.send_message(message.chat.id, f"Deudor: {_deudor} - ${_monto}")


bot.polling()
