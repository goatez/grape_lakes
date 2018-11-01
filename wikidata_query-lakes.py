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


# lake_format = [["Lake Name:", "lakeLabel", "value"], \
#                ["GNIS ID:", "GNIS_ID", "value"], \
#                ["Geo Name ID:", "GeoNames_ID", "value"], \
#                ["Wikipedia URL:", "article", "value"], \
#                ["Mediawiki URL:", "lake", "value"], \
#                ["Coordiantes:", "coordinate_location", "value"]]


            # print(properties[0], lake[properties[1]][properties[2]])
            # lake_haves.append(lake[properties[1]][properties[2]])
            # lake_dict[lake["lakeLabel"]["value"]] = lake_haves  #this work

            # lake_dict[lake["lakeLabel"]["value"]] = {"lake_name" : lake["lakeLabel"]["value"], \
            #                                          "gnis" : lake["GNIS_ID"]["value"], \
            #                                          "geoname" : lake["GeoNames_ID"]["value"], \
            #                                          "wikipedia" : lake["article"]["value"], \
            #                                          "mediawiki" : lake["lake"]["value"], \
            #                                          "coordinates" : lake["coordinate_location"]["value"]
            #                                          }  #this works


lake_dict ={}

for lake in results["results"]["bindings"]:
    try:
#       PUT COMMENTED OUT CODE ABOVE HERE,YA BIG DUMMY
        lake_dict[lake["lakeLabel"]["value"]] = {"lake_name" : lake["lakeLabel"]["value"]}
    except KeyError:
        lake_dict[lake["lakeLabel"]["value"]] = {"lake_name" : None }
    try:
        lake_dict[lake["lakeLabel"]["value"]].update({ "gnis" : lake["GNIS_ID"]["value"] })
    except KeyError:
        lake_dict[lake["lakeLabel"]["value"]].update({ "gnis" : None })
    try:
        lake_dict[lake["lakeLabel"]["value"]].update({ "geoname" : lake["GeoNames_ID"]["value"] })
    except KeyError:
        lake_dict[lake["lakeLabel"]["value"]].update({ "geoname" : None })
    try:
        lake_dict[lake["lakeLabel"]["value"]].update({ "wikipedia" : lake["article"]["value"] })
    except KeyError:
        lake_dict[lake["lakeLabel"]["value"]].update({ "wikipedia" : None })
    try:
        lake_dict[lake["lakeLabel"]["value"]].update({ "mediawiki" : lake["lake"]["value"] })
    except KeyError:
        lake_dict[lake["lakeLabel"]["value"]].update({ "mediawiki" : None })
    try:
        c = list(map(float, lake["coordinate_location"]["value"].strip('Point()').split()))
        coord = [{"lat" : c[0], "long" : c[1]}, c]
        lake_dict[lake["lakeLabel"]["value"]].update({ "coordinates" : coord })
    except KeyError:
        lake_dict[lake["lakeLabel"]["value"]].update({ "coordinates" : None })



for lake in lake_dict:
    print(lake_dict[lake])
