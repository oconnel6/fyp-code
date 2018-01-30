import requests
import json
from rdflib import Graph, Literal, BNode, RDF, Namespace
from rdflib.namespace import FOAF, DC, OWL

base = "https://api.openweathermap.org/data/2.5/weather?"
token = "&id=524901&APPID=0bf967b47593d3c2338685f71a747c86"

def get(params):
  return requests.get(base + params + token).json()

city=input("Please enter the name of the city")
#city = "dublin"

weather = get("q=" + city)

lat = weather["coord"]["lat"]
lon = weather["coord"]["lon"]
weather_main = weather["weather"][0]["main"]
weather_main = weather["weather"][0]["description"]
temp = weather["main"]["temp"]
pressure = weather["main"]["pressure"]
humidity = weather["main"]["humidity"]
wind_speed = weather["wind"]["speed"]
clouds = weather["clouds"]["all"]

ontology = Namespace("https://www.auto.tuwien.ac.at/downloads/thinkhome/ontology/WeatherOntology.owl")

store = Graph()

# Create an identifier to use as the subject.
weather = BNode()

# Add triples using store's add method.
store.add((weather, ontology.hasLatitude, Literal(lat)))
store.add((weather, ontology.hasLongitude, Literal(lon)))
store.add((weather, ontology.hasAtmosphericPressure, Literal(pressure)))
store.add((weather, ontology.hasExteriorTemperature, Literal(temp)))
store.add((weather, ontology.hasHumidity, Literal(humidity)))
store.add((weather, ontology.hasCloudCover, Literal(clouds)))
store.add((weather, ontology.hasSpeed, Literal(wind_speed)))

# Create the RDF file.
store.serialize("weather.rdf", format="pretty-xml", max_depth=3)

print("RDF Serializations:")

# Serialize as Turtle
print("--- start: turtle ---")
print(store.serialize(format="turtle"))
print("--- end: turtle ---\n")

