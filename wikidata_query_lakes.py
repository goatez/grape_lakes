# https://rdflib.github.io/sparqlwrapper/
# wikidata query: http://tinyurl.com/yatkw9da

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import pprint

# wikidata query for all the lakes in the US
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""#List of all the lakes in US
PREFIX schema: <http://schema.org/>
SELECT ?lake ?lakeLabel ?article ?coordinate_location ?lake_inflows ?lake_outflow
       ?elevation_above_sea_level ?area ?length ?width ?volume_as_quantity ?watershed_area
       ?perimeter ?residence_time_of_water ?vertical_depth ?GNIS_ID ?GeoNames_ID
WHERE {
  ?lake (wdt:P31/wdt:P279*) wd:Q23397.
  ?lake wdt:P17 wd:Q30.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL { ?article schema:about ?lake.
             ?article schema:inLanguage "en".
             ?article schema:isPartOf <https://en.wikipedia.org/>. }
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
  OPTIONAL { ?lake wdt:P1566 ?GeoNames_ID. }
}
LIMIT 100""")
sparql.setReturnFormat(JSON)

results = sparql.query().convert() # here lies my issue

# for result in results["results"]["bindings"]:
#     pprint.pprint(result)

lake_dict ={}
for lake in results["results"]["bindings"]:
    try:  # Lake name
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = {"lake_name" : lake["lakeLabel"]["value"]}
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = {"lake_name" : None }
    try:  # wikipedia URL
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "wikipedia_link" : lake["article"]["value"] })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "wikipedia_link" : None })
    try: # wikidata URL
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "wikidata_link" : lake["lake"]["value"] })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "wikidata_link" : None })
    try: # coordinates
        c = list(map(float, lake["coordinate_location"]["value"].strip('Point()').split()))  # striping string to be cast to a float
        coord = [{"lat" : c[0], "long" : c[1]}, c]  # creating dictionary of lat/long key pairing, and a list
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "coordinates" : coord })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "coordinates" : None })
    try:  # lake inflows
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
        .update({ "lake_inflow" : lake["lake_inflows"]["value"].strip('http://www.wikidata.org/entity/') })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "lake_inflow" : None })
    try: # lake outflows
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
        .update({ "lake_outflow" : lake["lake_outflow"]["value"].strip('http://www.wikidata.org/entity/') })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "lake_outflow" : None })
    try:  # elevation above sea level
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "elevation" : int(lake["elevation_above_sea_level"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "elevation" : None })
    try:  # area
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "area" : int(lake["area"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "area" : None })
    try: # length
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "length" : int(lake["length"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "length" : None })
    try:  # width
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "width" : int(lake["width"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "width" : None })
    try: # volume as quantity
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "volume" : int(lake["volume_as_quantity"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "volume" : None })
    try:  # watershed area
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "watershed" : int(lake["watershed_area"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "watershed" : None })
    try:  # perimeter
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "perimeter" : int(lake["perimeter"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "perimeter" : None })
    try: # residence time of water
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "residence_time_of_water" : int(lake["residence_time_of_water"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "residence_time_of_water" : None })
    try:  # vertical depth
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "vertical_depth" : int(lake["vertical_depth"]["value"]) })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "vertical_depth" : None })
    try:  # GNIS ID
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "gnis_id" : lake["GNIS_ID"]["value"] })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "gnis_id" : None })
    try:  # Geo-Name ID
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "geoname_id" : lake["GeoNames_ID"]["value"] })
    except:
        lake_dict[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "geoname_id" : None })

pprint.pprint(lake_dict)


###################################TESTING###################################

# lake_format = [["Lake Name:", "lakeLabel", "value"], \
#                ["GNIS ID:", "GNIS_ID", "value"], \
#                ["Geo Name ID:", "GeoNames_ID", "value"], \
#                ["Wikipedia URL:", "article", "value"], \
#                ["Mediawiki URL:", "lake", "value"], \
#                ["Coordiantes:", "coordinate_location", "value"]]

# for lake in results["results"]["bindings"]:
#     for properties in lake_format:
#         try:
#             print(properties[0]+":", lake[properties[1]][properties[2]])
#         except KeyError:
#             pass # key not present

# lake_dict[lake["lakeLabel"]["value"]] = {"lake_name" : lake["lakeLabel"]["value"], \
#                                          "gnis" : lake["GNIS_ID"]["value"], \
#                                          "geoname" : lake["GeoNames_ID"]["value"], \
#                                          "wikipedia" : lake["article"]["value"], \
#                                          "mediawiki" : lake["lake"]["value"], \
#                                          "coordinates" : lake["coordinate_location"]["value"]
#                                          }  #this works)
