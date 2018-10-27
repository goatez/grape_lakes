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


count=1
lakeLabel=0
gnis=0
geoname=0
mediawiki=0
wikipedia=0
coordinates=0

for lake in results["results"]["bindings"]:
    try:
        print("Number:", count)
        count+=1
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
        print("Coordiantes:", lake["coordinate_location"]["value"].strip('Point()').split()) # coordinates
        coordinates+=1
        print("---------------------")
    except KeyError:
        pass  # key not present


lakepct = ("{:.2f}".format((lakeLabel/count *100))+"%")   # percentage of lakes labeled
gnispct = ("{:.2f}".format((gnis/count *100))+"%")   # percentage of lakes with gnis IDs
geopct = ("{:.2f}".format((geoname/count *100))+"%")    # percentage of lakes with geo name IDs
mediawikipct = ("{:.2f}".format((mediawiki/count *100))+"%")   # percentage of lakes with mediawiki entries
wikipediapct = ("{:.2f}".format((wikipedia/count *100))+"%")  # percentage of lakes with wikipedia articles
coordpct = ("{:.2f}".format((coordinates/count *100))+"%")   # percentage of lages with given coordinates


print("Total number of Lake labels:", lakeLabel, "\nPercentage of Lake Labels:", lakepct)
print("\nTotal number of GNIS IDs:", gnis, "\nPercentage of GNIS IDs:", gnispct)
print("\nTotal number of Geo Name IDs:", geoname, "\nPercentage of Geo Name IDs:", geopct)
print("\nTotal number of Mediawiki entries:", mediawiki, "\nPercentage of Mediawiki entries:", mediawikipct)
print("\nTotal number of Wikipedia articles:", wikipedia, "\nPercentage of Wikipedia pages:", wikipediapct)
print("\nTotal number of coordinates given:", coordinates, "\nPercentage of given coordinates:", coordpct)


##############################################################################


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
