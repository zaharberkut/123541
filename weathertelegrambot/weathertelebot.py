import os
from config import TOKEN, URL, url_davis, mbar_mmHg, mph_ms, in_mm
import flask
from flask import Flask, request
import telebot
import json
import urllib.request
import datetime
import pytz

#import requests

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

def json_getweather():
    tzkiev = pytz.timezone('Europe/Kiev')
    date_now = datetime.datetime.now(tzkiev)
    data = urllib.request.urlopen(url_davis).read().decode()
    obj =  json.loads(data)
    observation_time = obj['observation_time_rfc822']
    lastupdated_time = datetime.datetime.strptime(observation_time, '%a, %d %b %Y %H:%M:%S %z')
    delta_time = date_now - lastupdated_time
    if delta_time.seconds < 3800:
        try:
            pressure = round(float(obj['pressure_mb']) * mbar_mmHg)
            temperature = float(obj['temp_c'])
            wind_speed = round(float(obj['wind_mph']) * mph_ms,1)
            wind_direction = obj['wind_dir']
            humidity = obj['relative_humidity']
            rain_ratehr = round(float(obj['davis_current_observation']['rain_rate_in_per_hr']) * in_mm,2)
            rain_dayin = round(float(obj['davis_current_observation']['rain_day_in']) * in_mm,2)
            if wind_direction == "North":
                wind_dir_uk = "Північний"
            elif wind_direction == "South":
                wind_dir_uk = "Південний"
            elif wind_direction == "West":
                wind_dir_uk = "Західний"
            elif wind_direction == "East":
                wind_dir_uk = "Східний"
            elif wind_direction == "Northeast" or wind_direction == "North-northeast" or wind_direction == "East-northeast":
                wind_dir_uk = "Північно-Східний"
            elif wind_direction == "Northwest" or wind_direction == "North-northwest" or wind_direction == "West-northwest":
                wind_dir_uk = "Північно-Західний"
            elif wind_direction == "Southeast" or wind_direction == "South-southeast" or wind_direction == "East-southeast":
                wind_dir_uk = "Південно-Східний"
            elif wind_direction == "Southwest" or wind_direction == "South-southwest" or wind_direction == "West-southwest":
                wind_dir_uk = "Південно-Західний"
            collecting_data ='Погода станом на '+lastupdated_time.strftime("%H:%M\n")+'======================\n''Температура: '+str(temperature)+' ℃\n''Тиск: '+str(pressure)+' мм рт. ст.\n''Вологість: '+str(humidity)+'%\n''Швидкість вітру: '+str(wind_speed)+' м/с\n''Напрямок вітру: '+str(wind_dir_uk)+'\n''Опади: '+str(rain_dayin)+' мм/день, '+str(rain_ratehr)+' мм/год.'
        except KeyError:
                collecting_data = "❗️Метеостанція Offline💤\n"+"з " +lastupdated_time.strftime("%d/%m/%Y %H:%M")
    else:collecting_data = "❗️Метеостанція Offline💤\n"+"з " +lastupdated_time.strftime("%d/%m/%Y %H:%M")
    return collecting_data

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Отримати погоду \u26F7🏂 \u2603')

#markup = telebot.types.InlineKeyboardMarkup()
#26F7
#stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
#crossIcon = u"\u26C5"
#for key, value in stringList.items():
#    markup.add(telebot.types.InlineKeyboardButton(text=value, callback_data="['value', '" + value + "', '" + key + "']"),
#               telebot.types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + key + "']"))

@bot.message_handler(commands=['start','help'])
def start(message):
    #bot.reply_to(message, 'Привіт, ' + message.from_user.first_name)
    bot.send_message(message.chat.id, ' \u2744 Вас вітає погодній бот ГЛК Захар Беркут\n\n''Щоб отримати інформіцію тисніть кнопку "Отримати погоду", яка знаходиться внизу👇\n', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    collecting_data = json_getweather()
    #bot.reply_to(message, message.text)
    bot.send_message(message.chat.id, 'Вітаю ' + message.from_user.first_name + '\n'+collecting_data, reply_markup=keyboard)

@server.route("/" + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    return "!", 200
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    #server.run(threaded=True)
