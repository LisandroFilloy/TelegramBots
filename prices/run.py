import telebot
import requests as req
from bs4 import BeautifulSoup

API_KEY = '2046818445:AAGt75S5ZzzRr9pJ3I0ucjB9C6PcKU5R-Mw'
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['dolarBlue'])
def dolar_blue_pricing(message):
    dolar_blue_html_req = req.get('https://dolarhoy.com/cotizaciondolarblue')
    soup = BeautifulSoup(dolar_blue_html_req.content, 'html.parser')
    values = soup.find_all('div', attrs={'class': 'value'})
    low = float(values[0].string.replace('$', ''))
    high = float(values[1].string.replace('$', ''))
    dolar_blue_mean = low + high / 2

    bot.send_message(message.chat.id, f'Bajo : {low}')
    bot.send_message(message.chat.id, f'Alto : {high}')
    bot.send_message(message.chat.id, f'Promedio : {dolar_blue_mean}')


@bot.message_handler(commands=['dolarCCL', 'dolarccl'])
def dolar_ccl_pricing(message):
    dolar_blue_html_req = req.get('https://dolarhoy.com/cotizaciondolarcontadoconliqui')
    soup = BeautifulSoup(dolar_blue_html_req.content, 'html.parser')
    values = soup.find_all('div', attrs={'class': 'value'})
    low = float(values[0].string.replace('$', ''))
    high = float(values[1].string.replace('$', ''))

    bot.send_message(message.chat.id, f'Punta compradora : {low}')
    bot.send_message(message.chat.id, f'Punta vendedora : {high}')


@bot.message_handler(commands=['PVU', 'pvu'])
def pvu_price(message):
    pvu_price_json = req.get(
        'https://api.pancakeswap.info/api/v2/tokens/0x31471e0791fcdbe82fbf4c44943255e923f1b794').json()
    _data = pvu_price_json.get('data', {})
    _price = _data.get('price')
    if _price:
        _price = round(float(_price), 3)

    bot.send_message(message.chat.id, f'PVU price: ${_price} (PancakeSwapV2)')


@bot.message_handler(commands=['BNB', 'bnb'])
def bnb_price(message):
    bnb_price_json = req.get(
        'https://api.pancakeswap.info/api/v2/tokens/0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c').json()
    _data = bnb_price_json.get('data', {})
    _price = _data.get('price')
    if _price:
        _price = round(float(_price), 3)

    bot.send_message(message.chat.id, f'BNB price: ${_price} (PancakeSwapV2)')


@bot.message_handler(commands=['Sueldo', 'sueldo'])
def sueldo(message):
    dolar_blue_html_req = req.get('https://dolarhoy.com/cotizaciondolarcontadoconliqui')
    soup = BeautifulSoup(dolar_blue_html_req.content, 'html.parser')
    values = soup.find_all('div', attrs={'class': 'value'})
    low = float(values[0].string.replace('$', ''))
    high = float(values[1].string.replace('$', ''))
    dolar_blue_mean = low + high / 2

    dolar_blue_html_req = req.get('https://dolarhoy.com/cotizaciondolarcontadoconliqui')
    soup = BeautifulSoup(dolar_blue_html_req.content, 'html.parser')
    values = soup.find_all('div', attrs={'class': 'value'})
    ccl_low = float(values[0].string.replace('$', ''))
    ccl_high = float(values[1].string.replace('$', ''))

    _sueldo = dolar_blue_mean * 290 + ccl_high * 400 * 0.83

    bot.send_message(message.chat.id, f'Sueldo = ${_sueldo} (ARG)')


bot.infinity_polling()
