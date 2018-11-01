# https://rdflib.github.io/sparqlwrapper/
# wikidata query: http://tinyurl.com/y97cvhb4

from SPARQLWrapper import SPARQLWrapper, JSON
import json

# wikidata query for all the lakes in the US
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""#List of all the lakes in US
PREFIX schema: <http://schema.org/>
SELECT ?lakeLabel ?lake ?article ?coordinate_location ?GNIS_ID ?GeoNames_ID ?lake_inflows ?lake_outflow
WHERE {
  ?lake (wdt:P31/wdt:P279*) wd:Q23397.
  ?lake wdt:P17 wd:Q30.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL { ?article schema:about ?lake.
             ?article schema:inLanguage "en".
             ?article schema:isPartOf <https://en.wikipedia.org/>. }
  OPTIONAL { ?lake wdt:P625 ?coordinate_location. }
  OPTIONAL { ?lake wdt:P590 ?GNIS_ID. }
  OPTIONAL { ?lake wdt:P1566 ?GeoNames_ID. }
  # OPTIONAL { ?lake wdt:P200 ?lake_inflows. }
  # OPTIONAL { ?lake wdt:P201 ?lake_outflow. }
}
LIMIT 30""")
sparql.setReturnFormat(JSON)

results = sparql.query().convert() # here lies my issue

# for result in results["results"]["bindings"]:
#     print(result)


count=0
lakeLabel=0
gnis=0
geoname=0
mediawiki=0
wikipedia=0
coordinates=0

lake_format = [["Lake Name:", "lakeLabel", "value", lakeLabel], \
               ["GNIS ID:", "GNIS_ID", "value", gnis], \
               ["Geo Name ID:", "GNIS_ID", "value", geoname], \
               ["Wikipedia URL:", "article", "value", wikipedia], \
               ["Mediawiki URL:", "lake", "value", mediawiki], \
               ["Coordiantes:", "coordinate_location", "value", coordinates]]

for lake in results["results"]["bindings"]:
    for properties in lake_format:

        try:
            print(properties[0], lake[properties[1]][properties[2]])  # Lake name
            properties[3]+=1

        except KeyError:
            pass  # key not present

    print("next entry")
