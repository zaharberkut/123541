import os
import flask
from flask import Flask, request
import telebot
import json
import urllib.request
import datetime
import pytz

import requests


def json_getweather() :
    with open('1.json') as json_file:
        obj = json.load(json_file)
    #obj =  json.loads(data)
    tzkiev = pytz.timezone('Europe/Kiev')
    time_now = datetime.datetime.now(tzkiev)
    print(time_now)
    observation_time = obj['observation_time_rfc822']
    datetime_object = datetime.datetime.strptime(observation_time, '%a, %d %b %Y %H:%M:%S %z')
    delta_time = time_now - datetime_object
    if delta_time.seconds > 1200:
        print("OK!")
        if 'temp_c' not in obj:
            print("this doesn't exist")
        else:
            print("exist")
            pressure = round(float(obj['pressure_mb']) * 0.75006375541921)
            temperature = float(obj['temp_c'])
            wind_speed = round(float(obj['wind_mph']) * 0.44704,1)
            humidity = obj['relative_humidity']
            rain_ratehr = round(float(obj['davis_current_observation']['rain_rate_in_per_hr']) * 25.4,2)
            rain_dayin = round(float(obj['davis_current_observation']['rain_day_in']) * 25.4,2)
            wind_direction = obj['wind_dir']
            if wind_direction == "North":
                wind_dir_uk = "🡣Північний"
            elif wind_direction == "South":
                wind_dir_uk = "🡡Південний"
            elif wind_direction == "West":
                wind_dir_uk = "🡢Західний"
            elif wind_direction == "East":
                wind_dir_uk = "🡠Східний"
            elif wind_direction == "Northeast" or wind_direction == "North-northeast" or wind_direction == "East-northeast":
                wind_dir_uk = "🡧Північно-Східний"
            elif wind_direction == "Northwest" or wind_direction == "North-northwest" or wind_direction == "West-northwest":
                wind_dir_uk = "🡦Північно-Західний"
            elif wind_direction == "Southeast" or wind_direction == "South-southeast" or wind_direction == "East-southeast":
                wind_dir_uk = "\U0001F864Південно-Східний"
            elif wind_direction == "Southwest" or wind_direction == "South-southwest" or wind_direction == "West-southwest":
                wind_dir_uk = "🡥Південно-Західний"
                collecting_data = str(observation_time)[16:21]+'Температура: '+str(temperature)+' C\n'+str(pressure)+' мм рт. ст.\n'+'Вологість: '+str(humidity)+'%\n'+'Швидкість вітру: '+str(wind_speed)+' м/с\n'+'Напрямок вітру: '+str(wind_dir_uk)+'\n'+'Опади: '+str(rain_dayin)+' мм/день, '+str(rain_ratehr)+' мм/год.'
                return collecting_data

    #temperature = float(obj['temp_c'])

    #print (temperature)



#wind_direction = json_getweather()
#wind_direction = wind_direction[0]
#collecting_data = json_getweather()
#collecting_data = collecting_data[1]
#print (wer)
print (json_getweather())
#collecting_data = json_getweather()
#print (json_getweather())



#print (switch_wind_dir(wind_direction))

#    return temperature, wind_direction
#print (json_printweather(obj))
