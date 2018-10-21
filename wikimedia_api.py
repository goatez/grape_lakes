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

url = "https://en.wikipedia.org/w/api.php?action=query&titles=Lake_Erie&prop=info&format=json"

address = urllib.request.urlopen(url)
data = address.read().decode()
wiki_lake = json.loads(data)

print(json.dumps(wiki_lake, indent=4))
