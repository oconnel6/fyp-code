import csv
import os
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import FOAF, DC, OWL

# list_of_cities = set(['dublin', 'carlow', 'cavan', 'cork', 'donegal', 'galway', 'roscommon', 'tipperary' ])
dir = os.path.expanduser('~/www')

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
