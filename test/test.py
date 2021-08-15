import os
import json
import urllib.request
import datetime
import time
import pytz

a = "Hello World"
print (a)

#time = time.clock()
tzkiev = pytz.timezone('Europe/Kiev')
date = datetime.datetime.now(tzkiev)
#print (date)
print (date.strftime("%H:%M"))

# download raw json object
url = "https://api.weatherlink.com/v1/NoaaExt.json?user=001D0A0124D3&pass=zaharberkut2019&apiToken=ED47A9235AF1472A8B5BC594D830B39D"
data = urllib.request.urlopen(url).read().decode()

# parse json object
obj = json.loads(data)

pressure = round(float(obj['pressure_mb']) * 0.75006375541921,1)
print (pressure)
temperature = float(obj['temp_c'])
print (temperature)
wind_speed = round(float(obj['wind_mph']) * 0.44704,1)
print (wind_speed)


#wind_direction = obj['wind_dir']
#print (wind_direction)
humidity = obj['relative_humidity']
print (humidity)
rain_ratehr = round(float(obj['davis_current_observation']['rain_rate_in_per_hr']) * 25.4,2)
print (rain_ratehr)
rain_dayin = round(float(obj['davis_current_observation']['rain_day_in']) * 25.4,2)
print (rain_dayin)

wind_direction = "West-southwest"
print (wind_direction)
def switch_wind_dir (wind_direction) :
    global wind_dir_uk
    if wind_direction == "North":
        wind_dir_uk = "Північний"
        return wind_dir_uk
    if wind_direction == "South":
        wind_dir_uk = "Південний"
        return wind_dir_uk
    if wind_direction == "West":
        wind_dir_uk = "Західний"
        return wind_dir_uk
    if wind_direction == "East":
        wind_dir_uk = "Східний"
        return wind_dir_uk
    if wind_direction == "Northeast" or "North-northeast" or "East-northeast":
        wind_dir_uk = "Північно-Східний"
        return wind_dir_uk
    if wind_direction == "Northwest" or "North-northwest" or "West-northwest":
        wind_dir_uk = "Північно-Західний"
        return wind_dir_uk
    if wind_direction == "Southeast" or "South-southeast" or "East-southeast":
        wind_dir_uk = "Південно-Східний"
        return wind_dir_uk
    if wind_direction == "Southwest" or "South-southwest" or "West-southwest":
        wind_dir_uk = "Південно-Західний"
        return wind_dir_uk

print (switch_wind_dir(wind_direction))
print (wind_dir_uk)

collecting_data ='Погода станом на '+date.strftime("%H:%M")+'\n''Температура: '+str(temperature)+' C\n''Тиск: '+str(pressure)+' мм рт. ст.\n''Вологість: '+str(humidity)+'%\n''Швидкість вітру: '+str(wind_speed)+' м/с\n''Напрямок вітру: '+str(wind_dir_uk)+'\n''Опади: '+str(rain_dayin)+' мм/день '+str(rain_ratehr)+'мм/год.'
print (collecting_data)
#date_default_timezone_set('Europe/Kiev');

# output some object attributes
#print(obj['wind_dir'])
#print('$ ' + obj['wind_dir'])

#"https://api.weatherlink.com/v1/NoaaExt.json?user=001D0A0124D3&pass=zaharberkut2019&apiToken=ED47A9235AF1472A8B5BC594D830B39D"
















import os
from flask import Flask, request
import telebot
import json
import urllib.request
import datetime
import pytz

import requests

TOKEN = '1136504254:AAGCi_3eBz9D3NSnAOp0vNbau6Npo1Av3s8'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

url = "https://api.weatherlink.com/v1/NoaaExt.json?user=001D0A0124D3&pass=zaharberkut2019&apiToken=ED47A9235AF1472A8B5BC594D830B39D"
data = urllib.request.urlopen(url).read().decode()

obj = json.loads(data)

pressure = round(float(obj['pressure_mb']) * 0.75006375541921,1)
temperature = float(obj['temp_c'])
wind_speed = round(float(obj['wind_mph']) * 0.44704,1)

#wind_direction = obj['wind_dir']
#print (wind_direction)
humidity = obj['relative_humidity']
rain_ratehr = round(float(obj['davis_current_observation']['rain_rate_in_per_hr']) * 25.4,2)
rain_dayin = round(float(obj['davis_current_observation']['rain_day_in']) * 25.4,2)

wind_direction = "West-southwest"
def switch_wind_dir (wind_direction) :
    global wind_dir_uk
    if wind_direction == "North":
        wind_dir_uk = "Північний"
        return wind_dir_uk
    if wind_direction == "South":
        wind_dir_uk = "Південний"
        return wind_dir_uk
    if wind_direction == "West":
        wind_dir_uk = "Західний"
        return wind_dir_uk
    if wind_direction == "East":
        wind_dir_uk = "Східний"
        return wind_dir_uk
    if wind_direction == "Northeast" or wind_direction == "North-northeast" or wind_direction == "East-northeast":
        wind_dir_uk = "Північно-Східний"
        return wind_dir_uk
    if wind_direction == "Northwest" or wind_direction == "North-northwest" or wind_direction == "West-northwest":
        wind_dir_uk = "Північно-Західний"
        return wind_dir_uk
    if wind_direction == "Southeast" or wind_direction == "South-southeast" or wind_direction == "East-southeast":
        wind_dir_uk = "Південно-Східний"
        return wind_dir_uk
    if wind_direction == "Southwest" or wind_direction == "South-southwest" or wind_direction == "West-southwest":
        wind_dir_uk = "Південно-Західний"
        return wind_dir_uk

#print (wind_dir_uk)
print (switch_wind_dir(wind_direction))
tzkiev = pytz.timezone('Europe/Kiev')
date = datetime.datetime.now(tzkiev)

collecting_data = 'Погода станом на '+date.strftime("%H:%M")+'\n'+'======================'+'\n'+'Температура: '+str(temperature)+'‎ ℃\n'+'Тиск: '+str(pressure)+' мм рт. ст.\n'+'Вологість: '+str(humidity)+'%\n'+'Швидкість вітру: '+str(wind_speed)+' м/с\n'+'Напрямок вітру: '+wind_direction+'\n'+'Опади: '+str(rain_dayin)+' мм/день, '+str(rain_ratehr)+' мм/год.'

keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row('Отримати погоду')
#markup = telebot.types.InlineKeyboardMarkup()

#stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
#crossIcon = u"\u26C5"
#for key, value in stringList.items():
#    markup.add(telebot.types.InlineKeyboardButton(text=value, callback_data="['value', '" + value + "', '" + key + "']"),
#               telebot.types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + key + "']"))


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привіт, ' + message.from_user.first_name)
    bot.send_message(message.chat.id, 'Вітаю ' + message.from_user.first_name + '\n' + collecting_data, reply_markup=keyboard)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    #bot.reply_to(message, message.text)
    bot.send_message(message.chat.id, 'Вітаю ' + message.from_user.first_name + '\n' + collecting_data, reply_markup=keyboard)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://3db48bb1.ngrok.io/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    #server.run(threaded=True)

#1136504254:AAGCi_3eBz9D3NSnAOp0vNbau6Npo1Av3s8
