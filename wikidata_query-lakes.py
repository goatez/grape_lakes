# https://rdflib.github.io/sparqlwrapper/
# wikidata query: http://tinyurl.com/y97cvhb4

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import pprint

# wikidata query for all the lakes in the US
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""#List of all the lakes in US
PREFIX schema: <http://schema.org/>
SELECT ?lake ?article ?coordinate_location ?lake_inflows ?lake_outflow ?elevation_above_sea_level ?area ?length ?width ?volume_as_quantity ?watershed_area ?perimeter ?residence_time_of_water ?vertical_depth ?GNIS_ID WHERE {
  ?lake (wdt:P31/wdt:P279*) wd:Q23397.
  ?lake wdt:P17 wd:Q30.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL {
    ?article schema:about ?lake.
    ?article schema:inLanguage "en".
    ?article schema:isPartOf <https://en.wikipedia.org/>.
  }
  OPTIONAL { ?lake wdt:P625 ?coordinate_location. }
  OPTIONAL { ?lake wdt:P200 ?lake_inflows. }
  OPTIONAL { ?lake wdt:P201 ?lake_outflow. }
  OPTIONAL { ?lake wdt:P2044 ?elevation_above_sea_level. }
  OPTIONAL { ?lake wdt:P2046 ?area. }
  OPTIONAL { ?lake wdt:P2043 ?length. }
  OPTIONAL { ?lake wdt:P2049 ?width. }
  OPTIONAL { ?lake wdt:P2234 ?volume_as_quantity. }
  OPTIONAL { ?lake wdt:P2053 ?watershed_area. }
  OPTIONAL { ?lake wdt:P2547 ?perimeter. }
  OPTIONAL { ?lake wdt:P3020 ?residence_time_of_water. }
  OPTIONAL { ?lake wdt:P4511 ?vertical_depth. }
  OPTIONAL { ?lake wdt:P590 ?GNIS_ID. }
  OPTIONAL { ?lake wdt:P625 ?coordinate_location. }
}
LIMIT 100""")
sparql.setReturnFormat(JSON)

results = sparql.query().convert() # here lies my issue

for result in results["results"]["bindings"]:
    pprint.pprint(result)


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
    except:
        lake_dict[lake["lakeLabel"]["value"]] = {"lake_name" : None }
    try:
        lake_dict[lake["lakeLabel"]["value"]].update({ "gnis" : lake["GNIS_ID"]["value"] })
    except:
        lake_dict[lake["lakeLabel"]["value"]].update({ "gnis" : None })
    try:
        lake_dict[lake["lakeLabel"]["value"]].update({ "geoname" : lake["GeoNames_ID"]["value"] })
    except:
        lake_dict[lake["lakeLabel"]["value"]].update({ "geoname" : None })
    try:
        lake_dict[lake["lakeLabel"]["value"]].update({ "wikipedia" : lake["article"]["value"] })
    except:
        lake_dict[lake["lakeLabel"]["value"]].update({ "wikipedia" : None })
    try:
        lake_dict[lake["lakeLabel"]["value"]].update({ "wikidata_link" : lake["lake"]["value"] })
    except:
        lake_dict[lake["lakeLabel"]["value"]].update({ "wikidata_link" : None })
    try:
        c = list(map(float, lake["coordinate_location"]["value"].strip('Point()').split()))
        coord = [{"lat" : c[0], "long" : c[1]}, c]
        lake_dict[lake["lakeLabel"]["value"]].update({ "coordinates" : coord })
    except:
        lake_dict[lake["lakeLabel"]["value"]].update({ "coordinates" : None })

# pprint.pprint(lake_dict)

