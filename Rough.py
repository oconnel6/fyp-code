# Transfer Met Eireann Data to RDF
import requests
import json
from rdflib import Graph, Literal, BNode, RDF, Namespace, URIRef
from rdflib.namespace import FOAF, DC, OWL
import numpy as np
from dateutil.parser import parse


import csv

with open("MetEireannFile.csv") as f:
    
    lines = f.readlines()
    lat, rest = lines[2].split(":", 1)[1].split(" ,", 1)
    print(lat)
    long = rest.split(": ")[1].split(",")[0]
    print(long)
    keys = lines[25].split(",")

    data = []
    for row in csv.reader(lines[26:]):
        data.append(dict(zip(keys, row)))
    

ontology = Namespace("https://www.auto.tuwien.ac.at/downloads/thinkhome/ontology/WeatherOntology.owl")

store = Graph()


for row in data:
    
    date = row['date']
    #print(type(parse(date).date()))
    
    # Create an identifier to use as the subject.
    #weather = BNode()
    weather = URIRef('http://example.com' + '/' + parse(date).date().isoformat())
    # Add triples using store's add method.
    
    
    store.add((weather, ontology.hasLatitude, Literal(lat)))
    store.add((weather, ontology.hasLongitude, Literal(long)))
    store.add((weather, ontology.hasAtmosphericPressure, Literal(row["cbl"])))
    store.add((weather, ontology.hasExteriorTemperature, Literal((float(data[0]['maxtp']) + float(data[0]['mintp'])) / 2)))
    #store.add((weather, ontology.hasHumidity, Literal(humidity)))
    #store.add((weather, ontology.hasCloudCover, Literal(clouds)))
    store.add((weather, ontology.hasSpeed, Literal(row["wdsp"])))


print("RDF Serializations:")

# Serialize as Turtle
print("--- start: turtle ---")
store.serialize("weather.rdf", format="turtle")
print("--- end: turtle ---\n")
