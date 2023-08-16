from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from helpers import lookup, fahrenheit, mph, hour

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET"])
def index():
    if "temp" not in session:
        session["temp"] = "C"
        session["time"] = "24"
        session["speed"] = "K"
        session["default"] = None
        session["current"] = None
        session["input"] = False

    if session["default"] == None:
        return render_template("index.html")
    else:
        return redirect("/results")


@app.route("/results", methods=["GET", "POST"])
def results():

    if "default" not in session or "input" not in session:
        session["default"] = None
        session["input"] = False

    if request.method == "POST":

        city = request.form.get("city")

    elif request.method == "GET":
        if session["input"] == True:
            city = session["current"]
            session["input"] = False
        else:
            city = session["default"]
            if not city:
                return redirect("/")

    data = lookup(city)

    if not data:
        error = "Invalid city, please check your spelling!"
        return render_template("error.html", error=error)

    description = data["desc"]

    if data["desc"] in ["Smoke", "Dust", "Ash", "Sand"]:
        main = "/static/Dust.png"
    elif (data["desc"] in ["Fog", "Mist"]) and (data["time"] > data["sunrise"]) and (data["time"] < data["sunset"]):
        main = "/static/Haze.png"
    elif data["desc"] in ["Fog", "Mist"]:
        main = "/static/Fog.png"
    elif data["desc"] == "Clear":
        if data["icon"] == "01d":
            main = "/static/Sun.png"
        elif data["icon"] == "01n":
            main = "/static/Moon.png"
    elif data["desc"] == "Clouds":
        if data["icon"] in ["02d", "03d", "04d"] and data["num"] in [801, 802, 803]:
            main = "/static/CloudyDay.png"
            description = "Partly Cloudy"
        elif data["icon"] in ["02n", "03n", "04n"] and data["num"] in [801, 802, 803]:
            main = "/static/CloudyNight.png"
            description = "Partly Cloudy"
        elif data["num"] == 804:
            main = "/static/Clouds.png"
            description = "Cloudy"
    else:
        main = "/static/" + data["desc"] + ".png"

    if data["time"] < data["sunrise"]:
        sun = "/static/Sunrise.png"
        sunrise = str(data["sunrise"])[-8:-3]
        sunset = str(data["sunset"])[-8:-3]

    elif data["time"] > data["sunrise"] and data["time"] < data["sunset"]:
        sun = "/static/Sunset.png"
        sunset = str(data["sunset"])[-8:-3]
        sunrise = str(data["tsunrise"])[-8:-3]

    elif data["time"] > data["sunset"]:
        sun = "/static/Sunrise.png"
        sunrise = str(data["tsunrise"])[-8:-3]
        sunset = str(data["tsunset"])[-8:-3]


    time = str(data["time"])[-8:-3]

    date = data["time"]

    day = date.strftime('%A %B %-d, %Y')

    descs = ["Wind", "Pressure", "Humidity", "Feels", "Sun"]

    icons = []

    for i in range(len(descs)):
        icons.append("/static/" + descs[i] + ".png")


    for i in ["temp", "low", "high", "feels"]:
        if session["temp"] == "F":
            data[i] = str(fahrenheit(data[i])) + "°F"
        else:
            data[i] = str(data[i]) + "°C"

    if session["speed"] == "M":
        data["windspeed"] = str(mph(data["windspeed"])) + " mph"
    else:
        data["windspeed"] =  str(data["windspeed"]) + " km/h"

    times = {"time": time, "sunset": sunset, "sunrise": sunrise}

    for i in times:
        if session["time"] == "12":
            times[i] = hour(times[i])

    return render_template("weather.html", session=session, day=day, data=data, times=times, main=main, sun=sun, description=description, icons=icons)

@app.route("/default", methods=["GET", "POST"])
def default():
    if request.method == "GET":
        return redirect("/")
    elif request.method == "POST":
        session["default"] = request.form.get("default")
        return redirect("/results")

@app.route("/units", methods=["GET", "POST"])
def units():
    if request.method == "GET":
        return redirect("/")
    elif request.method == "POST":
        session["input"] = True
        for i in ["current", "temp", "speed", "time"]:
            session[i] = request.form.get(i)
        return redirect("/results")

