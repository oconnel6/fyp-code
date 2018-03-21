import requests
import json
import csv
import datetime
import sys
import os
import time
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import FOAF, DC, OWL

from csv_to_rdf import create_rdf

# Set up directory
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

# Creates the rdf files from the csv files
def create_rdf(list_of_cities):
  for city in list_of_cities:

    print("Creating rdf for " + city)

    # Read in the CSV
    with open(dir + '/data/csv/' + city + '.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    # Create the RDF Graph
    ontology = Namespace("https://www.auto.tuwien.ac.at/downloads/thinkhome/ontology/WeatherOntology.owl")
    store = Graph()

    # For each row (date) create a uri
    for row in data:
      city_and_date = URIRef("http://irishweather.oconnell.scss.tcd.ie/" + city + "/" + row["date"])

      # unused
      # store.add((weather, ontology.hasLatitude, Literal(lat)))
      # store.add((weather, ontology.hasLongitude, Literal(lon)))
      # store.add((weather, ontology.hasCloudCover, Literal(clouds)))

      # Add the weather
      store.add((city_and_date, ontology.hasExteriorTemperature, Literal(row["temp"])))
      store.add((city_and_date, ontology.hasRain, Literal(row["rain"])))
      store.add((city_and_date, ontology.hasAtmosphericPressure, Literal(row["pressure"])))
      store.add((city_and_date, ontology.hasSpeed, Literal(row["wind_speed"])))
      store.add((city_and_date, ontology.hasHumidity, Literal(row["humidity"])))
    
    # Create the RDF file.
    store.serialize(dir + "/data/rdf/" + city + ".rdf", format="turtle", max_depth=3)

    print("Finished creating RDF for " + city)


######################################################
##############       Main Program       ##############
######################################################

# Initial list of cities not fetched is all of them
not_fetched_cities = list_of_cities

# While there is still cities we haven't fetched
# and we haven't retried more than 20 times
x = 0
while len(not_fetched_cities) != 0 and x < 20:
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
