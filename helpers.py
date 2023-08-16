import requests
from datetime import datetime
from zoneinfo import ZoneInfo


def convert(s):
    if s[-2:] =="PM":
        s = s.split(":")
        s[0] = str(int(s[0]) + 12)
        s = s[0] + ":" + s[1] + ":" + s[2]
    elif s[-2:] == "AM":
        copy = s.split(":")
        if int(copy[0]) < 10:
            s = "0" + s
    return s[:8]

def fahrenheit(temp):
    return int(((1.8 * temp) + 32))

def mph(speed):
    return round((1.6 * speed), 1)

def hour(t):

    if (int(t[0:2]) < 12):
        if t[0] == "0":
            t = t[1:]
        t += " AM"
    elif (int(t[0:2]) == 12):
        t += " PM"
    else:
        a = int(t[0:2]) - 12
        t = str(a) + t[2:] + " PM"
    return t

def lookup(city):

    base1 = "http://api.openweathermap.org/data/2.5/weather?"

    api_key1 = "e0793fd94e02bda0b4af573b56e81f93"

    url1 = base1 + "appid=" + api_key1 + "&q=" + city

    base2 = "http://api.weatherapi.com/v1/current.json?"

    api_key2 = "18ec44f9acf04c2b9cf204420230106"

    url2 = base2 + "key=" + api_key2 + "&q=" + city

    base3 = "https://api.sunrisesunset.io/json?"


    try:
        response1 = requests.get(url1).json()
        city = response1["coord"]
        temp = round(response1["main"]["temp"] - 273.15)
        low = round(response1["main"]["temp_min"] - 273.15)
        high = round(response1["main"]["temp_max"] - 273.15)
        feels = round(response1["main"]["feels_like"] - 273.15)
        pressure = response1["main"]["pressure"]
        humidity = response1["main"]["humidity"]
        lon = response1["coord"]["lon"]
        lat = response1["coord"]["lat"]
        desc = response1["weather"][0]["main"]
        icon = response1["weather"][0]["icon"]
        num = response1["weather"][0]["id"]


        response2 = requests.get(url2).json()
        city = response2["location"]["name"]
        windspeed = response2["current"]["wind_kph"]
        direction = response2["current"]["wind_dir"]
        uv = response2["current"]["uv"]
        timezone = response2["location"]["tz_id"]
        time = (datetime.now(tz=ZoneInfo(timezone)))

        time = str(time)[:19]

        tcopy = str(time).split()

        url3 = base3 + "lat=" + str(lat) + "&lng=" + str(lon) + "&date=today"
        response3 = requests.get(url3).json()
        sunrise = response3["results"]["sunrise"]
        sunset = response3["results"]["sunset"]

        sunrise = tcopy[0] + " " + convert(sunrise)
        sunset = tcopy[0] + " " + convert(sunset)

        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        sunrise = datetime.strptime(sunrise, "%Y-%m-%d %H:%M:%S")
        sunset = datetime.strptime(sunset, "%Y-%m-%d %H:%M:%S")

        url4 = base3 + "lat=" + str(lat) + "&lng=" + str(lon) + "&date=tomorrow"
        response4 = requests.get(url4).json()
        tsunrise = response4["results"]["sunrise"]
        tsunset = response4["results"]["sunset"]

        tsunrise = tcopy[0] + " " + convert(tsunrise)
        tsunset = tcopy[0] + " " + convert(tsunset)

        tsunrise = datetime.strptime(tsunrise, "%Y-%m-%d %H:%M:%S")
        tsunset = datetime.strptime(tsunset, "%Y-%m-%d %H:%M:%S")


        return {
            "city": city,
            "time": time,
            "windspeed": windspeed,
            "low": low,
            "high": high,
            "temp":temp,
            "feels": feels,
            "direction": direction,
            "pressure":pressure,
            "humidity": humidity,
            "sunrise": sunrise,
            "sunset": sunset,
            "desc":desc,
            "icon":icon,
            "num": num,
            "uv":uv,
            "tsunset": tsunset,
            "tsunrise": tsunrise
            }

    except (requests.RequestException, ValueError, KeyError, IndexError):
        return None

