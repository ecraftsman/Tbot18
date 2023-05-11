import requests
import json


class APIException(Exception):
    pass


class Exchange:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        try:
            response = requests.get(f'https://api.exchangeratesapi.io/latest?base={base}&symbols={quote}')
        except:
            raise APIException('Не удалось получить данные по курсу валют')

        try:
            result = json.loads(response.content)
            price = result['rates'][quote]
        except:
            raise APIException(f'Не удалось обработать ответ от API. Код ответа: {response.status_code}')

        return price * amount

    TOKEN = '5859958650:AAE6AdNq-g3RbuYx2FzJCtgPX61ixH9EVsQ'
    import telebot
    from extensions import APIException, Exchange
    from config import TOKEN

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message,
                     "Привет! Чтобы узнать цену валюты, введите запрос в формате: \n<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>")

    @bot.message_handler(commands=['values'])
    def send_values(message):
        bot.reply_to(message, "Доступные валюты: USD, EUR, RUB")

    @bot.message_handler(func=lambda message: True)
    def send_price(message):
        try:
            base, quote, amount = message.text.split(' ')
            result = Exchange.get_price(base.upper(), quote.upper(), float(amount))
        except APIException as e:
            bot.reply_to(message, f'Ошибка: {str(e)}')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать запрос: {str(e)}')
        else:
            bot.reply_to(message, f'{amount} {base.upper()} = {result:.2f} {quote.upper()}')

    bot.polling()