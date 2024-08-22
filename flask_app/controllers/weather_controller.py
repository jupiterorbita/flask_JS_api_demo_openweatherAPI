# ROUTING
from flask_app import app, API_KEY
from flask import render_template, redirect, request, session, flash, jsonify
# from flask_app.models.user_model import User
# from flask_app.models.party_model import Party
import requests

from flask_app.services.functions import service_get_forecast, service_get_final_data

from datetime import datetime, timezone
import pytz # convert to local time

print(API_KEY)

@app.route("/")
def weather_landing():
    return render_template("weather.html")


@app.route("/weather_data")
def weather_data():
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={API_KEY}")
    # we must keep in line with JSON format.
    # requests has a method to convert the data coming back into JSON.
    return jsonify( r.json() )


@app.route("/weather/form", methods=['POST'])
def get_city_name_form():

    # clear previous session
    # session.clear()
    if 'forecast' in session:
        session.pop("forecast")

    # check if the user entered anything
    if len(request.form['city_name']) < 2:
        flash("please enter a city name", 'city_name_err')
        return redirect("/")

    city = request.form['city_name']

    r_json_list = service_get_forecast(city)

    service_get_final_data(r_json_list)
    
    return redirect("/")

@app.route("/weather/form/forecast", methods=['POST'])
def get_weather_forecast():

    # clear previous session
    session.clear()
    # if 'weather' in session:
    #     session.pop("weather")

    # check if the user entered anything
    if len(request.form['city_name']) < 2:
        flash("please enter a city name", 'city_name_err')
        return redirect("/")
    
    print(f"\n ==== request.form ====\n", request.form)
    print(f"\n ==== city_name ====\n", request.form['city_name'])
    city = request.form['city_name']
    
    # get the lat lon for the city
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}")
    r_json_list = r.json()
    print("r_json_list =>", r_json_list)

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
    forecast_weather_res = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial")
    forecast_weather_res_json = forecast_weather_res.json()
    print("*******************")
    print(forecast_weather_res_json)
    print("*******************")

    def convert_to_local_time(unix_timestamp, local_timezone):
        # Convert UNIX timestamp to UTC datetime
        utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        # Convert UTC time to the specified local timezone
        local_time = utc_time.astimezone(pytz.timezone(local_timezone))
        return local_time.strftime('%A, %d %B %I:%M %p')

    # Choose your local timezone, e.g., 'America/New_York'
    local_timezone = 'America/New_York'

    # Convert all times in the response to local time
    for item in forecast_weather_res_json['list']:
        item['local_time'] = convert_to_local_time(item['dt'], local_timezone)
        print(item['local_time'])

    session['forecast'] = forecast_weather_res_json['list']

    return redirect("/")