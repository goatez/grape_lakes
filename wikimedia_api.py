import urllib.request, urllib.parse, urllib.error
import json
import pandas as pd

import os
os.getcwd()

# end_point = 'https://en.wikipedia.org/w/api.php'
# action = "&action=query"
# title = "&titles="
# prop = "&prop="
# format = "&format="
# example:  ?action=query&titles=Lake_Erie&prop=info&format=json

url = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles=Lake_Michigan&rvsection=0"
url2 = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&titles=Lake_Michigan&format=json"
url3 = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles=Lake_Michigan&format=json"

address = urllib.request.urlopen(url3)
data = address.read().decode()
wiki_lake = json.loads(data)

print(json.dumps(wiki_lake, indent=4))
