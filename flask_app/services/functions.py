from flask_app import app, API_KEY
from flask import render_template, redirect, request, session, flash, jsonify
import requests
import pprint
from datetime import datetime, timezone
import pytz # convert to local time

print(API_KEY)

def service_get_forecast(city):
    # get the lat lon for the city
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}")
    r_json_list = r.json()
    return r_json_list

def service_get_final_data(r_json_list):
    # check if the api came back with a valid city
    if len(r_json_list) < 1:
        flash("please enter a VALID city name", 'city_name_err')
        return redirect("/")

    # store data to call next api
    name = r_json_list[0]['name']
    lat = r_json_list[0]['lat']
    lon = r_json_list[0]['lon']
    country = r_json_list[0]['country']
    state = r_json_list[0]['state']
    print(f"{name}, {state}, {country} is at lat:{lat}, lon:{lon}")

    # get final data
    curent_weather_res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial")
    curent_weather_res_json = curent_weather_res.json()
    print(curent_weather_res_json)
    
    # final data to store in session
    template_dict = {
        'name' : curent_weather_res_json['name'],
        'description' : curent_weather_res_json['weather'][0]['description'],
        'icon' : curent_weather_res_json['weather'][0]['icon'],
        'temp': curent_weather_res_json['main']['temp']
    }

    session['weather'] = template_dict