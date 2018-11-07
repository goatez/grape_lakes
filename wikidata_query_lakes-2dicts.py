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
# pprint.pprint(results)

# for result in results["results"]["bindings"]:  # print results line by line
#     pprint.pprint(result)

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
lake_format = [["lake_name", "lakeLabel", "value", label], \
               ["wikipedia_url", "article", "value", wikipedia], \
               ["wikidata_url", "lake", "value", wikidata], \
               ["coordiantes", "coordinate_location", "value", coordinates], \
               ["lake_inflow", "lake_inflows", "value", inflow], \
               ["lake_outflow", "lake_outflow", "value", outflow], \
               ["elevation_above_sea_level", "elevation_above_sea_level", "value", elevation], \
               ["area", "area", "value", area], \
               ["length", "length", "value", length], \
               ["width", "width", "value", width], \
               ["volume_as_quantity", "volume_as_quantity", "value", volume], \
               ["watershed_area", "watershed_area", "value", watershed], \
               ["perimeter", "perimeter", "value", perimeter], \
               ["residence_time_of_water", "residence_time_of_water", "value", residence], \
               ["vertical_depth", "vertical_depth", "value", depth], \
               ["gnis_id", "GNIS_ID", "value", gnis], \
               ["geo_name_id", "GeoNames_ID", "value", geoname]]

dict_with = {}
dict_without = {}

# dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')] = {properties[0] : None }
# dict_without[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')] = {properties[0] : None }

for entry in results["results"]["bindings"]:
    for properties in lake_format:
        if properties[1] in entry:
            if properties[1] == 'elevation_above_sea_level' or properties[1] == 'area' or\
                                properties[1] == 'length' or properties[1] == 'width' or\
                                properties[1] == 'volume_as_quantity' or properties[1] == 'watershed_area' or\
                                properties[1] == 'perimeter' or properties[1] == 'residence_time_of_water' or\
                                properties[1] == 'vertical_depth':
                try:  # dealing with entries cast as float
                    dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
                    .update({ properties[0] : float( entry[properties[1]][properties[2]] ) } )
                except KeyError:
                    dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
                    { properties[0] : float(entry[properties[1]][properties[2]]) }

            elif properties[1] == 'lake_inflows' or properties[1] == 'lake_outflow':
                try:  # dealing with entries stripping text
                    dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
                    .update({ properties[0] :  entry[properties[1]][properties[2]].strip('http://www.wikidata.org/entity/') } )
                except KeyError:
                    dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
                    { properties[0] : entry[properties[1]][properties[2]].strip('http://www.wikidata.org/entity/') }

            elif properties[1] == 'coordinate_location':  # dealing with casting coordinates and making a list
                c = list(map(float, entry[properties[1]][properties[2]].strip('Point()').split()))  # striping string to be cast to a float
                coord = [{"lat" : c[0], "long" : c[1]}, c]  # creating dictionary of lat/long key pairing, and a list
                try:
                    dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
                    .update({ properties[0] : coord })
                except KeyError:
                    dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
                    { properties[0] : coord }
            else:
                try:  # dealing with remaining entries
                    dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
                    .update({ properties[0] : entry[properties[1]][properties[2]] })
                except KeyError:
                    dict_with[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
                    { properties[0] : entry[properties[1]][properties[2]] }
        else:
            try:  # dealing with dictionary of missing lake properties
                dict_without[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')]\
                .update({ properties[0] : None })
            except KeyError:
            # pass
                dict_without[entry["lake"]["value"].strip('http://www.wikidata.org/entity/')] =\
                { properties[0] : None }

pprint.pprint(dict_with)
pprint.pprint(dict_without)

###################################DESCRIPTIVE STATISTICS###################################

# sum of occurences
print("Descriptive Statistics: Sum of Occurences\
      \n-----------------------------------------")
for lake in results["results"]["bindings"]:
    for properties in lake_format:
        if properties[1] in lake:
            properties[3]+=1

for properties in lake_format:
    print( properties[0]+":", properties[3] )

##########################################TESTING##########################################
