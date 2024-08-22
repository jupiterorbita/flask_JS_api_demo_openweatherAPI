from flask import Flask
import os
API_KEY = os.environ.get("WEATHER_API_KEY")
app = Flask(__name__)
# for session we need a sercet key
app.secret_key = "wesirduhfguiawer39iouaqr345weghtu9iqa"

# DATABASE="enter-db-here"