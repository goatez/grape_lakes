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
LIMIT 20""")
sparql.setReturnFormat(JSON)

results = sparql.query().convert()

# for result in results["results"]["bindings"]:
#     pprint.pprint(result)

lakes_with_properties ={}
lakes_missing_properties = {}

for lake in results["results"]["bindings"]:

    if "lakeLabel" in lake: # Lake name (label)
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({"lake_name" : lake["lakeLabel"]["value"] })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = {"lake_name" : lake["lakeLabel"]["value"] }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({"lake_name" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = {"lake_name" : None }

    if "artile" in lake: #wikipedia URL
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "wikipedia_link" : lake["article"]["value"] })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "wikipedia_link" : lake["article"]["value"] }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "wikipedia_link" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "wikipedia_link" : None }

    if "lake" in lake: # wikidata URL
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "wikidata_link" : lake["lake"]["value"] })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "wikidata_link" : lake["lake"]["value"] }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "wikidata_link" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "wikidata_link" : None }

    if "coordinate_location" in lake: # coordinates
        c = list(map(float, lake["coordinate_location"]["value"].strip('Point()').split()))  # striping string to be cast to a float
        coord = [{"lat" : c[0], "long" : c[1]}, c]  # creating dictionary of lat/long key pairing, and a list
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "coordinates" : coord })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "coordinates" : coord }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "coordinates" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "coordinates" : None }

    if "lake_inflows" in lake: # lake inflows
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "lake_inflow" : lake["lake_inflows"]["value"].strip('http://www.wikidata.org/entity/') })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
            { "lake_inflow" : lake["lake_inflows"]["value"].strip('http://www.wikidata.org/entity/') }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "lake_inflow" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "lake_inflow" : None }

    if "lake_outflow" in lake: # lake outflows
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "lake_outflow" : lake["lake_outflow"]["value"].strip('http://www.wikidata.org/entity/') })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { "lake_outflow" : lake["lake_outflow"]["value"].strip('http://www.wikidata.org/entity/') }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "lake_outflow" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "lake_outflow" : None }

    if "elevation_above_sea_level" in lake: # elevation above sea level
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "elevation" : float(lake["elevation_above_sea_level"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "elevation" : float(lake["elevation_above_sea_level"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "elevation" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "elevation" : None }

    if "area" in lake: # area
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "area" : float(lake["area"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "area" : float(lake["area"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "area" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "area" : None }

    if "length" in lake: # length
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "length" : float(lake["length"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "length" : float(lake["length"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "length" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "length" : None }

    if "width" in lake: # width
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "width" : float(lake["width"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "width" : float(lake["width"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "width" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "width" : None }

    if "volume_as_quantity" in lake: # volume as quantity
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "volume" : int(lake["volume_as_quantity"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "volume" : int(lake["volume_as_quantity"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "volume" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "volume" : None }

    if "watershed_area" in lake: # watershed area
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "watershed" : int(lake["watershed_area"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "watershed" : int(lake["watershed_area"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "watershed" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "watershed" : None }

    if "perimeter" in lake: # perimeter
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "perimeter" : int(lake["perimeter"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "perimeter" : int(lake["perimeter"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "perimeter" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "perimeter" : None }

    if "residence_time_of_water" in lake: # residence time of water
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "residence_time_of_water" : float(lake["residence_time_of_water"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "residence_time_of_water" : float(lake["residence_time_of_water"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "residence_time_of_water" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "residence_time_of_water" : None }

    if "vertical_depth" in lake: # vertical depth
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
            .update({ "vertical_depth" : float(lake["vertical_depth"]["value"]) })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
             { { "vertical_depth" : float(lake["vertical_depth"]["value"]) } }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "vertical_depth" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "vertical_depth" : None }

    if "GNIS_ID" in lake: # GNIS ID
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "gnis_id" : lake["GNIS_ID"]["value"] })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "gnis_id" : lake["GNIS_ID"]["value"] }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "gnis_id" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "gnis_id" : None }

    if "GeoNames_ID" in lake: # GeoName ID
        try:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "geoname_id" : lake["GeoNames_ID"]["value"] })
        except:
            lakes_with_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "geoname_id" : lake["GeoNames_ID"]["value"] }
    else:
        try:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')].update({ "geoname_id" : None })
        except:
            lakes_missing_properties[lake["lake"]["value"].strip('http://www.wikidata.org/entity/')] = { "geoname_id" : None }

pprint.pprint(lakes_with_properties)
pprint.pprint(lakes_missing_properties)



###################################DESCRIPTIVE STATISTICS###################################

# counters
label=0
wikipedia=0
wikidata=0
coordinates=0
inflow=0
outflow=0
elevation=0
area=0
length=0
width=0
volume=0
watershed=0
perimeter=0
residence=0
depth=0
gnis=0
geoname=0

# data fields
lake_format = [["Lake Name:", "lakeLabel", "value", label], \
               ["Wikipedia URL:", "article", "value", wikipedia], \
               ["Wikidata URL:", "lake", "value", wikidata], \
               ["Coordiantes Location:", "coordinate_location", "value", coordinates], \
               ["Lake Inflow:", "lake_inflows", "value", inflow], \
               ["Lake Outflow:", "lake_outflow", "value", outflow], \
               ["Elevation Above Sea Level:", "elevation_above_sea_level", "value", elevation], \
               ["Area:", "area", "value", area], \
               ["Length:", "length", "value", length], \
               ["Width:", "width", "value", width], \
               ["Volume as Quantity:", "volume_as_quantity", "value", volume], \
               ["Watershed Area:", "watershed_area", "value", watershed], \
               ["Perimeter:", "perimeter", "value", perimeter], \
               ["Residence Time of Water:", "residence_time_of_water", "value", residence], \
               ["Vertical Depth:", "vertical_depth", "value", depth], \
               ["GNIS ID:", "GNIS_ID", "value", gnis], \
               ["Geo Name ID:", "GeoNames_ID", "value", geoname]]


# sum of occurences
for lake in results["results"]["bindings"]:
    for properties in lake_format:
        if properties[1] in lake:
            properties[3]+=1

for properties in lake_format:
    print( properties[0], properties[3] )




###################################TESTING###################################

# pprint.pprint(results)

# lake_format = [["Lake Name:", "lakeLabel", "value"], \
#                ["Wikipedia URL:", "article", "value"], \
#                ["Wikidata URL:", "lake", "value"], \
#                ["Coordiantes:", "coordinate_location", "value"], \
#                ["Lake Inflow:", "lake_inflows", "value"], \
#                ["Lake Outflow:", "lake_outflow", "value"], \
#                ["Elevation Above Sea Level:", "elevation_above_sea_level", "value"], \
#                ["Area:", "area", "value"], \
#                ["Length:", "length", "value"], \
#                ["Width:", "width", "value"], \
#                ["Volume:", "volume_as_quantity", "value"], \
#                ["Watershed:", "watershed_area", "value"], \
#                ["Perimeter:", "perimeter", "value"], \
#                ["Residence Time of Water:", "residence_time_of_water", "value"], \
#                ["Vertical Depth:", "vertical_depth", "value"], \
#                ["GNIS ID:", "GNIS_ID", "value"], \
#                ["Geo Name ID:", "GeoNames_ID", "value"] ]

# lake_dict = {}
# for lake in results["results"]["bindings"]:
#     for properties in lake_format:
#         try:
#             print(properties[0]+":", lake[properties[1]][properties[2]])
#             lake_dict[lake["lakeLabel"]["value"]] = {"lake_name" : lake["lakeLabel"]["value"]}
#         except KeyError:
#             pass # key not present


# lakeset = []
# lake_dict = {}
# for lake in results["results"]["bindings"]:
#     for properties in lake_format:
#         try:
#             lakeset.append(lake[properties[1]][properties[2]])
#             lake_dict[lake["lakeLabel"]["value"]].update( {lake[properties[1]] : lakeset } ) #this work
#         except KeyError:
#             pass  # key not present


# lake_dict[lake["lakeLabel"]["value"]] = {"lake_name" : lake["lakeLabel"]["value"], \
#                                          "gnis" : lake["GNIS_ID"]["value"], \
#                                          "geoname" : lake["GeoNames_ID"]["value"], \
#                                          "wikipedia" : lake["article"]["value"], \
#                                          "mediawiki" : lake["lake"]["value"], \
#                                          "coordinates" : lake["coordinate_location"]["value"]
#                                          }  #this works)
