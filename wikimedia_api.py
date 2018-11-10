import urllib.request, urllib.parse, urllib.error
import json
import pprint

url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=Lake_Michigan&rvsection=0"
url2 = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=Lake_Michigan&format=json"
# url3 is working to get first section of page  (infobox and summary) | nothing from 'history' and below
url3 = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&prop=pageprops&ppprop=wikibase_item&titles=Lake_Michigan&format=json"
url4 = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=1&titles=Lake_Michigan&format=json"
url5 = "https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=wikibase_item&titles=Lake_Michigan&format=json"

urlx = "https://en.wikipedia.org/w/api.php?action=parse&page=Lake_Michigan&format=json"

# api.php?action=parse&text={{Project:Sandbox}}&contentmodel=wikitext


address = urllib.request.urlopen(urlx)
data = address.read().decode()
wiki_lake = json.loads(data)

pprint.pprint(json.dumps(wiki_lake, indent=4))
