# https://rdflib.github.io/sparqlwrapper/
# https://github.com/siznax/wptools/

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import pprint
import wptools
import re
import os

# wikidata query for all the lakes in the US
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""#List of all the lakes in US
PREFIX schema: <http://schema.org/>
SELECT  ?lake ?lakeLabel ?article ?coordinate_location ?lake_inflows ?lake_outflow
        ?elevation_above_sea_level ?area ?length ?width ?volume_as_quantity ?watershed_area
        ?perimeter ?residence_time_of_water ?vertical_depth ?GNIS_ID ?GeoNames_ID
WHERE { ?lake (wdt:P31/wdt:P279*) wd:Q23397.
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
LIMIT 1500""")  # change or delete the limit here to alter the number of lakes to be included in your query
sparql.setReturnFormat(JSON)

results = sparql.query().convert()
# pprint.pprint(results)

# wikidata counters
label=0
wikipedia_url=0
wikidata_item_id=0
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

#wikipedia counters
elevation2=0
area2=0
length2=0
width2=0
volume2=0
depth2=0
gnis2=0

# data fields
lake_format = [["lake_name", "lakeLabel", "value", label], \
               ["wikipedia_url", "article", "value", wikipedia_url], \
               ["wikidata_item_id", "lake", "value", wikidata_item_id], \
               ["coords", "coordinate_location", "value", coordinates], \
               ["inflow", "lake_inflows", "value", inflow], \
               ["outflow", "lake_outflow", "value", outflow], \
               ["elevation", "elevation_above_sea_level", "value", elevation], \
               ["area", "area", "value", area], \
               ["length", "length", "value", length], \
               ["width", "width", "value", width], \
               ["volume", "volume_as_quantity", "value", volume], \
               ["watershed_area", "watershed_area", "value", watershed], \
               ["perimeter", "perimeter", "value", perimeter], \
               ["residence_time", "residence_time_of_water", "value", residence], \
               ["depth", "vertical_depth", "value", depth], \
               ["gnis_id", "GNIS_ID", "value", gnis], \
               ["geo_name_id", "GeoNames_ID", "value", geoname]]

wikipedia_lake_format = [["elevation", "elevation", elevation2], \
                        ["area", "area", area2], \
                        ["length", "length", length2], \
                        ["width", "width", width2], \
                        ["volume", "volume", volume2], \
                        ["depth", "depth", depth2], \
                        ["gnis_id", "reference", gnis2]]

dict_with = {}
dict_without = {}
dict_noWikipedia = {}
dict_wikipedia = {}
bad_name = []

for entry in results["results"]["bindings"]:
    if "article" in entry:

        try:  # using wptools to parse wikipedia infobox
            lake_name = entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')
            page = wptools.page(lake_name)
            page.get_parse()
            lake = page.data['infobox']

            try:
                dict_wikipedia.update({entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/') : lake})
            except:
                dict_wikipedia = {entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/') : lake}
        except:
            lake_name = entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')
            bad_name.append(lake_name)
            pass

        # creating wikidata dictionary
        for properties in lake_format:
            if properties[1] in entry:

                # dealing with any entries that are to be cast as float
                if properties[1] == 'elevation_above_sea_level' or properties[1] == 'area' or\
                                    properties[1] == 'length' or properties[1] == 'width' or\
                                    properties[1] == 'volume_as_quantity' or properties[1] == 'watershed_area' or\
                                    properties[1] == 'perimeter' or properties[1] == 'residence_time_of_water' or\
                                    properties[1] == 'vertical_depth':
                    try:
                        dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')]\
                        .update({ properties[0] : float( entry[properties[1]][properties[2]] ) } )
                    except KeyError:
                        dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')] =\
                        { properties[0] : float(entry[properties[1]][properties[2]]) }

                # dealing with entries that strip text
                elif properties[1] == 'lake_inflows' or properties[1] == 'lake_outflow':
                    try: # wikidata text
                        dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')]\
                        .update({ properties[0] :  entry[properties[1]][properties[2]].lstrip('http://www.wikidata.org/entity/') } )
                    except KeyError:
                        dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')] =\
                        { properties[0] : entry[properties[1]][properties[2]].lstrip('http://www.wikidata.org/entity/') }

                # dealing with coordinates entry - spliting, casting as a float, and making a list
                elif properties[1] == 'coordinate_location':
                    c = list(map(float, entry[properties[1]][properties[2]].strip('Point()').split()))  # striping string to be cast to a float
                    coord = [{"lat" : c[0], "long" : c[1]}, c]  # creating dictionary of lat/long key pairing, and a list
                    try:
                        dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')]\
                        .update({ properties[0] : coord })
                    except KeyError:
                        dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')] =\
                        { properties[0] : coord }

                else:  # dealing with remaining entries containing lake properties
                    try:
                        dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')]\
                        .update({ properties[0] : entry[properties[1]][properties[2]] })
                    except KeyError:
                        dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')] =\
                        { properties[0] : entry[properties[1]][properties[2]] }

            else:  # dealing with missing lake properties, saving to second dictionary as None
                try:
                    dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')]\
                    .update({ properties[0] : None })
                    try:
                        dict_without[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')]\
                        .update({ properties[0] : None })
                    except KeyError:
                        dict_without[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')] =\
                        { properties[0] : None }
                except KeyError:
                # pass
                    dict_with[entry["article"]["value"].lstrip('https://en.wikipedia.org/wiki/')] =\
                    { properties[0] : None }

    else:  # lakes with no wikipedia entries
        for properties in lake_format:
            if properties[1] in entry:

                # dealing with any entries that are to be cast as float
                if properties[1] == 'elevation_above_sea_level' or properties[1] == 'area' or\
                                    properties[1] == 'length' or properties[1] == 'width' or\
                                    properties[1] == 'volume_as_quantity' or properties[1] == 'watershed_area' or\
                                    properties[1] == 'perimeter' or properties[1] == 'residence_time_of_water' or\
                                    properties[1] == 'vertical_depth':
                    try:
                        dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')]\
                        .update({ properties[0] : float( entry[properties[1]][properties[2]] ) } )
                    except KeyError:
                        dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')] =\
                        { properties[0] : float(entry[properties[1]][properties[2]]) }

                # dealing with entries that strip text
                elif properties[1] == 'lake_inflows' or properties[1] == 'lake_outflow':
                    # wikidata text
                    try:
                        dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')]\
                        .update({ properties[0] :  entry[properties[1]][properties[2]].lstrip('http://www.wikidata.org/entity/') } )
                    except KeyError:
                        dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')] =\
                        { properties[0] : entry[properties[1]][properties[2]].lstrip('http://www.wikidata.org/entity/') }

                # dealing with coordinates entry - spliting, casting as a float, and making a list
                elif properties[1] == 'coordinate_location':
                    c = list(map(float, entry[properties[1]][properties[2]].strip('Point()').split()))  # striping string to be cast to a float
                    coord = [{"lat" : c[0], "long" : c[1]}, c]  # creating dictionary of lat/long key pairing, and a list
                    try:
                        dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')]\
                        .update({ properties[0] : coord })
                    except KeyError:
                        dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')] =\
                        { properties[0] : coord }

                # dealing with remaining entries containing lake properties
                else:
                    try:
                        dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')]\
                        .update({ properties[0] : entry[properties[1]][properties[2]] })
                    except KeyError:
                        dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')] =\
                        { properties[0] : entry[properties[1]][properties[2]] }

            # dealing with missing lake properties, saving to second dictionary as None
            else:
                try:
                    dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')]\
                    .update({ properties[0] : None })
                except KeyError:
                # pass
                    dict_noWikipedia[entry["lake"]["value"].lstrip('http://www.wikidata.org/entity/')] =\
                    { properties[0] : None }

# Cleaning wikipedia dictionary
clean_wikipedia = {}
for article in dict_wikipedia:
    for prop in wikipedia_lake_format:

        try:  # deals with GNIS ID
            x = re.findall('{{gnis\W([0-9]*).*', dict_wikipedia[article][prop[1]])
            try:
                clean_wikipedia[article].update({prop[0] : x[0]})
            except:
                clean_wikipedia[article] = {prop[0] : x[0]}
        except:
            try: # also deals with other instances of GNIS ID
                y = re.findall('GNIS ID:\W([0-9]*).*', dict_wikipedia[article][prop[1]])
                try:
                    clean_wikipedia[article].update({prop[0] : y[0]})
                except:
                    clean_wikipedia[article] = {prop[0] : y[0]}
            except:
                try:  # deals with area, depth, elevation, length, volume, width
                    z = re.findall('{{convert\W([0-9]\.[0-9]{1,4}).*', dict_wikipedia[article][prop[1]])
                    try:
                        clean_wikipedia[article].update({prop[0] : float(z[0])})
                    except:
                        clean_wikipedia[article] = {prop[0] : float(z[0])}
                except:
                    try:  # deals with area, depth, elevation, length, volume, width with decimal points
                        zz = re.findall('{{convert\W([0-9]*).*', dict_wikipedia[article][prop[1]])
                        try:
                            clean_wikipedia[article].update({prop[0] : float(zz[0])})
                        except:
                            clean_wikipedia[article] = {prop[0] : float(zz[0])}
                    except:
                        try:  # deals with no property listed
                            clean_wikipedia[article].update({prop[0] : None })
                        except:
                            clean_wikipedia[article] = {prop[0] : None }

# create one dictionary containing both dictionaries made above
lake_dict = {}
lake_dict['wikidata_entries'] = dict_with
lake_dict['wikidata_missing_properties'] = dict_without
lake_dict['no_wikipedia_entries'] = dict_noWikipedia
lake_dict['wikipedia_entries'] = clean_wikipedia

# pprint.pprint(lake_dict)


###################################LAKE PROPERTY COMPARISON###################################

# Comparing lake properties in Wikidata and Wikipedia dictionaries
# writing comparison list of properties that do not match to text file
# saving list in new dictionary

# TODO only completed a comparison on 7 of the 14 lake properties, still must

lake_formating = ["area", "depth", "elevation", "gnis_id", "length", "volume", "width"]
lake_properties_not_matching = {}
wikidata = {}
wikipedia = {}

file = open("lake_comparison.txt","w")
file.write("Lake Properties Not Matching: Wikidata vs. Wikipedia\n")
for pond in lake_dict['wikipedia_entries']:
    file.write("\n----------------"+pond+"---------------------\n")
    for thing in lake_formating:
        if lake_dict['wikidata_entries'][pond][thing] != lake_dict['wikipedia_entries'][pond][thing]:
            file.write("No match | "  + pond + " | Wikidata  | " + thing +\
                       " : " + str(lake_dict['wikidata_entries'][pond][thing])+"\n")
            file.write("No match | "  + pond + " | Wikipedia | " + thing +\
                       " : " + str(lake_dict['wikipedia_entries'][pond][thing])+"\n")
            try:
                wikidata[pond].update({thing : lake_dict['wikidata_entries'][pond][thing] })
                wikipedia[pond].update({thing : lake_dict['wikipedia_entries'][pond][thing] })
            except:
                wikidata[pond] = {thing : lake_dict['wikidata_entries'][pond][thing] }
                wikipedia[pond] = {thing : lake_dict['wikipedia_entries'][pond][thing] }
        else:
            pass

file.close()

lake_properties_not_matching["Wikidata"] = wikidata
lake_properties_not_matching["Wikipedia"] = wikipedia

pprint.pprint(lake_properties_not_matching)

###################################DESCRIPTIVE STATISTICS###################################
# IF YOU RUN JUST THIS SECTION OF CODE, BE SURE TO SET THE COUNTERS TO ZERO IN CODE ABOVE

x = str(len(lake_dict['wikidata_entries']))
y = str(len(lake_dict['wikipedia_entries']))

f = open("lake_descriptive_statistics.txt", "w")

# sum of occurences
f.write("-----------------------------------------\
      \nDESCRIPTIVE STATISTICS: SUM OF OCCURENCES\
      \n-----------------------------------------\n")

# descriptive statistics for Wikidata articles dictionary
for lake in lake_dict['wikidata_entries']:
    for properties in lake_format:
        if  lake_dict['wikidata_entries'][lake][properties[0]] != None:
            properties[3]+=1

f.write("\n-----------------------------------------\
         \nTotal number of Wikidata articles: " + x +\
        "\n-----------------------------------------")
for properties in lake_format:
    f.write( "\n"+str(properties[0])+": "+ str(properties[3]) )

# descriptive statistics for Wikipedia articles dictionary

f.write("\n\n-----------------------------------------")
for lake in lake_dict['wikipedia_entries']:
    for properties in wikipedia_lake_format:
        if  lake_dict['wikipedia_entries'][lake][properties[0]] != None:
            properties[2]+=1

f.write("\nTotal number of Wikipedia articles: " + y +\
        "\n-----------------------------------------")
for properties in wikipedia_lake_format:
    f.write( "\n"+ str(properties[0])+ ": " + str(properties[2]) )

f.close()
