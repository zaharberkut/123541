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
    url = "https://api.weatherlink.com/v1/NoaaExt.json?user=001D0A0124D3&pass=zaharberkut2019&apiToken=ED47A9235AF1472A8B5BC594D830B39D"
    data = urllib.request.urlopen(url).read().decode()
    obj =  json.loads(data)
    pressure = round(float(obj['pressure_mb']) * 0.75006375541921,1)
    temperature = float(obj['temp_c'])
    wind_speed = round(float(obj['wind_mph']) * 0.44704,1)
    humidity = obj['relative_humidity']
    rain_ratehr = round(float(obj['davis_current_observation']['rain_rate_in_per_hr']) * 25.4,2)
    rain_dayin = round(float(obj['davis_current_observation']['rain_day_in']) * 25.4,2)
    wind_direction = obj['wind_dir']
    
    collecting_data ='Температура: '+str(temperature)+' C\n'+str(pressure)+' мм рт. ст.\n'+'Вологість: '+str(humidity)+'%\n'+'Швидкість вітру: '+str(wind_speed)+' м/с\n'+'Напрямок вітру: '+wind_direction+'\n'+'Опади: '+str(rain_dayin)+' мм/день, '+str(rain_ratehr)+' мм/год.'
    return wind_direction, collecting_data
wind_direction = json_getweather()
wind_direction = wind_direction[0]
collecting_data = json_getweather()
collecting_data = collecting_data[1]
