# https://rdflib.github.io/sparqlwrapper/
# wikidata query: http://tinyurl.com/y97cvhb4

from SPARQLWrapper import SPARQLWrapper, JSON
import json

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
#     print(result)


count=0
lakeLabel=0
gnis=0
geoname=0
mediawiki=0
wikipedia=0
coordinates=0

for lake in results["results"]["bindings"]:
    print("Number:", count+1)

    try:
        count+=1
    except KeyError:
        pass  # key not present

    try:
        print("Lake Name:", lake["lakeLabel"]["value"])  # Lake name
        lakeLabel+=1
    except KeyError:
        pass  # key not present

    try:
        print("GNIS ID:", lake["GNIS_ID"]["value"])  # GNIS ID
        gnis+=1
    except KeyError:
        pass  # key not present

    try:
        print("Geo Name ID:", lake["GeoNames_ID"]["value"])  #Geo Name ID
        geoname+=1
    except KeyError:
        pass  # key not present
    try:
        print("Mediawiki URL:", lake["lake"]["value"])  # wikidata entry
        mediawiki+=1
    except KeyError:
        pass  # key not present
    try:
        print("Wikipedia URL:", lake["article"]["value"]) #wikipedia entry
        wikipedia+=1
    except KeyError:
        pass  # key not present
    try:
        c = list(map(float, lake["coordinate_location"]["value"].strip('Point()').split()))
        coord = [c[0], c[1], c]
        print("Coordiantes:", coord) # coordinates => long and lat split and saved as a list
        coordinates+=1
        print("---------------------")
    except KeyError:
        pass  # key not present

lakepct = ("{:.2f}".format((lakeLabel/(count) *100))+"%")   # percentage of lakes labeled
gnispct = ("{:.2f}".format((gnis/(count) *100))+"%")   # percentage of lakes with gnis IDs
geopct = ("{:.2f}".format((geoname/(count) *100))+"%")    # percentage of lakes with geo name IDs
mediawikipct = ("{:.2f}".format((mediawiki/(count) *100))+"%")   # percentage of lakes with mediawiki entries
wikipediapct = ("{:.2f}".format((wikipedia/(count) *100))+"%")  # percentage of lakes with wikipedia articles
coordpct = ("{:.2f}".format((coordinates/(count) *100))+"%")   # percentage of lages with given coordinates


# print descriptive statistics
print("Total number of lakes in Mediawiki query:", (count), \
      "\n-----------------------------------------\n"+ \
      "Total number of Lake Labels:", lakeLabel, "out of", (count), \
      "\nPercentage of Lake Labels:", lakepct, \
      "\n-----------------------------------------\n"+ \
      "Total number of GNIS IDs:", gnis, "out of", (count), \
      "\nPercentage of GNIS IDs:", gnispct, \
      "\n-----------------------------------------\n"+ \
      "Total number of Geo Name IDs:", geoname, "out of", (count), \
      "\nPercentage of Geo Name IDs:", geopct, \
      "\n-----------------------------------------\n"+ \
      "Total number of Mediawiki entries:", mediawiki, "out of", (count), \
      "\nPercentage of Mediawiki entries:", mediawikipct, \
      "\n-----------------------------------------\n"+ \
      "Total number of Wikipedia articles:", wikipedia, "out of", (count), \
      "\nPercentage of Wikipedia pages:", wikipediapct, \
      "\n-----------------------------------------\n"+ \
      "Total number of coordinates given:", coordinates, "out of", (count), \
      "\nPercentage of given coordinates:", coordpct)



# print(coord)
# x = list(map(float, coord))
# test = [x[0], x[1], x]
# print(test)


# x = [1,2]
# x
# y = [3,4]
# x.append(y)
# print(x)
#
#
# w = [1,2,3]
# f = w
#
# print(f)
# w.append(f)
# print(w)




#################################TESTING#################################


# coord = results["results"]["bindings"][3]["coordinate_location"]['value'] #example
# coord = coord.strip('Point()').split()  #stripping coordinates
# print(coord)

# # save headings
# headings = results['head']['vars']
# print(headings)

# # save as json file
# json = json.dumps(results)
# f = open("results.json", "w")
# f.write(json)
# f.close()

# # save as text file
# f = open("results.txt", "w")
# f.write(str(results))
# f.close()

# # save as a list of dictionaries
# results1 = results["results"]["bindings"]
# for result1 in results1:
#     print(result1)
# print(results1)


# f = open("results1.txt", "w")
# for line in results:
#     f.write(str(results))
# f.close()
#
# with open("myfile.txt", "w") as f:
#     for key, value in results.items():
#         f.write('%s:%s\n' % (key, value))
