import requests
import json
import csv
import datetime
import sys

base = "https://api.openweathermap.org/data/2.5/weather?"
token = "&id=524901&APPID=0bf967b47593d3c2338685f71a747c86&units=metric"

def get(params):
  return requests.get(base + params + token).json()

list=['dublin', 'carlow', 'cavan', 'cork', 'donegal', 'galway', 'roscommon', 'tipperary' ]

for x in range (0,len(list)):
    city = list[x]
    print("Running for " + city)

    weather = get("q=" + city)
    
    #print(weather)

    lat = weather["coord"]["lat"]
    lon = weather["coord"]["lon"]
    weather_main = weather["weather"][0]["main"]
    weather_main = weather["weather"][0]["description"]
    temp = weather["main"]["temp"]
    pressure = weather["main"]["pressure"]
    humidity = weather["main"]["humidity"]
    wind_speed = weather["wind"]["speed"]
    clouds = weather["clouds"]["all"]

    today = datetime.date.today()

    today = today.strftime('%d-%b-%y')

    nextRow = [today, temp, -1, pressure, wind_speed, humidity];
    
    filename = city + ".csv"

    with open(filename, 'a', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(nextRow)
            