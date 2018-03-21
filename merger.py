import requests
import json
import csv
import datetime
import sys
import os
import time

from csv_to_rdf import create_rdf

# Set up directory
#dir = os.path.dirname(os.path.abspath(__file__))
# dir = "~/www"
dir = os.path.expanduser('~/www')

print("\n\nStarting Merger Script - " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))

# Define constants for API
base = "https://api.openweathermap.org/data/2.5/weather?"
token = "&id=524901&APPID=0bf967b47593d3c2338685f71a747c86&units=metric"

# Making these a set for comparison later
list_of_cities = set(['dublin', 'carlow', 'cavan', 'cork', 'donegal', 'galway', 'roscommon', 'tipperary' ])

# Makes a GET request to the API
def get(params):
  return requests.get(base + params + token)

# Creates an array to use as a row for the CSV files
def create_row(weather): 
  # Currently unused
  lat = weather["coord"]["lat"]
  lon = weather["coord"]["lon"]
  weather_main = weather["weather"][0]["main"]
  weather_main = weather["weather"][0]["description"]
  clouds = weather["clouds"]["all"]

  # Currently used
  temp = weather["main"]["temp"]
  pressure = weather["main"]["pressure"]
  wind_speed = weather["wind"]["speed"]
  humidity = weather["main"]["humidity"]
  today = datetime.date.today()
  today = today.strftime('%d-%b-%y')
  return [today, temp, None, pressure, wind_speed, humidity]

# Fetches the weather for the provided list of cities
# Returns a dictionary {city -> weather}
def fetch_data_from_list(list):  
  weather_by_city = dict()
  for city in list:
    print("Running for " + city)
    response = get("q=" + city)

    if not response.ok:
      print("Error fetching from API for " + city + ": " + str(response.status_code) + " " + response.reason)
    else:
      weather = response.json()
      print("Valid response received from API")

      weather_for_city = create_row(weather)
      print("Created next row object for " + city)
      
      weather_by_city[city] = weather_for_city
  return weather_by_city

# Writes results to their files
def write_results(weather_by_city):
  for city, row in weather_by_city.iteritems():
    filename = dir + "/data/csv/" + city + ".csv"

    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)
        print("Appended row to file for " + city)


######################################################
##############       Main Program       ##############
######################################################

# Initial list of cities not fetched is all of them
not_fetched_cities = list_of_cities

# While there is still cities we haven't fetched
# and we haven't retried more than 10 times
x = 0
while len(not_fetched_cities) != 0 and x < 10:
  print("Have cities to fetch: " + str(not_fetched_cities))

  # Fetch the weather for those cities
  weather_by_city = fetch_data_from_list(not_fetched_cities)

  # Write the fetched weather data to a file
  write_results(weather_by_city)

  # Remove the cities we just fetched from the list of non fetched cities
  not_fetched_cities = not_fetched_cities - set(weather_by_city.keys())
  
  print("non fetched cities: " + str(not_fetched_cities))

  # Wait 30 seconds to try again
  time.sleep(30)
  x = x + 1

if (len(not_fetched_cities) != 0):
  print("Couldn't fetch weather data for: " + str(not_fetched_cities))
else:
  print("Successfully completed for all counties")

create_rdf(list_of_cities)
