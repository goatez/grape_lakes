import urllib.request, urllib.parse, urllib.error
import json
import pprint
from bs4 import BeautifulSoup
import requests
import os

# os.getcwd()

# action = query
urlQ1 = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&lang=en&titles=Lake_Michigan"
# urlQ2 = "https://en.wikipedia.org/w/api.php?format=json& action=query& prop=revisions& rvprop=content& rvsection=1& titles=Lake_Michigan"
# urlQ3 = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=pageprops&ppprop=wikibase_item&titles=Lake_Michigan"

# action = parse
urlP1 = "https://en.wikipedia.org/w/api.php?format=json&action=parse&section=0&list=langbacklinks&lbllang=en&page=Lake_Michigan"
urlP2 =  'api.php?action=parse&text={{Lake_Michigan}}&contentmodel=wikitext'
urlP3 = "https://en.wikipedia.org/w/api.php?format=json&action=parse&page=Infobox&page=Lake_Michigan"

address = urllib.request.urlopen(urlQ1)
data = address.read().decode()
wikiLake = json.loads(data)

pprint.pprint(json.dumps(wikiLake, indent=4))
# pprint.pprint(wikiLake['parse']['text'])

# prop=parsetree

url1 = 'https://en.wikipedia.org/w/api.php?format=json&action=query&prop=revisions&rvprop=content&rvsection=0&lang=en&titles=Lake_Michigan'
url2 = 'https://en.wikipedia.org/wiki/Lake_Michigan'



r = requests.get(url1)
soup = BeautifulSoup(r.text, 'lxml')
print(soup.prettify())


r = requests.get(url2)
soup = BeautifulSoup(r.text, 'xml')
print(soup.prettify())



# write to text
# with open('api.txt', 'w') as file:
#     file.write(json.dumps(wikiLake, indent=2))



# import wptools
# page = wptools.page('Lake_Ontario')
# page.get_parse()



parts = soup.find_all('value')
for part in parts:
    print(part.gettext())
