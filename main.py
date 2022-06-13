import telebot

from config import *
from extensions import Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите команду в формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество первой валюты>\n\
Доступные валюты: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))

    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.lower().split()

    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        base, quote, amount = values
        result = Converter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Ошибка на сервере, попробуйте снова\n{e}')

    else:
        text = f'{amount} {base} = {result} {quote}'
        bot.reply_to(message, text)


bot.polling()