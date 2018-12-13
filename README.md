# grape_lakes
INST 309 Independent Study - US Lakes Project
Project for independent study with Jonathan Brier @brierjon.

Resources:<br />
https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Lakes/Assessment<br />
Wikidata ideal lake content that should be queryable: https://www.wikidata.org/wiki/Wikidata:WikiProject_Lakes<br />
https://en.wikipedia.org/wiki/Template:Infobox_body_of_water<br />
Wptools: https://github.com/siznax/wptools<br />

Example Wikidata Item: https://www.wikidata.org/wiki/Q4738340<br />
Example Wikipedia Page: https://en.wikipedia.org/wiki/Alvord_Lake_(Arizona)<br />

Project Goals<br />
For this project, I am comparing the Wikipedia and Wikidata entries of all the lakes in the U.S. in an effort to identify any entries between the two that differ – particularly finding any missing or different characteristics within the Wikipedia entries in order to pull missing characteristics into the Wikidata:WikiProject_Lakes project. This may mean the entries for a specific characteristic of a lake do not match, or are just missing. Ultimately I intended to do Wikipedia scanning to pull in missing facts to Wikidata for Lakes in the U.S. Not all Wikidata items have all the property fields outlined in the Wikidata Project of U.S. Lakes, and not all Wikipedia pages have instances of the lakes within the Wikidata:WikiProject Lakes project.

Project Overview<br />
In order to compare the Wikipedia and Wikidata U.S. Lake articles, I needed to create a dictionaries containing both entries, so that they can then be compared against each other, with any differing or missing lake properties saved in another dictionary.

Lake Properties: as defined on the Wikidata page for the WikiProject Lakes<br />

 
•	country<br />
•	coordinate location<br />
•	lake inflows<br />
•	lake outflow<br />
•	elevation above sea level<br />
•	area<br />
•	length<br />
•	width<br />
•	volume as quantity<br />
•	watershed area<br />
•	perimeter<br />
•	residence time of water<br />
•	vertical depth<br />
 

Additionally, the following fields are also included in my search:<br /> 

•	GNIS ID #<br />
•	Geo-name ID #<br />

Properties being compared<br />
For the sake of time and project complexity, I have scaled down the scope of the project that was initially proposed; and I will be comparing the following properties.<br />

•	elevation above sea level (elevation)<br />
•	area (area)<br />
•	length (length)<br />
•	width (width)<br />
•	volume as quantity (volume)<br />
•	vertical depth (depth)<br />
•	GNIS ID # (reference)<br />

Properties not being compared<br />
These are the lake properties that I will not be comparing, again, for sake of time and project complexity.<br />

•	coordinate location<br />
•	lake inflows<br />
•	lake outflow<br />
•	watershed area<br />
•	perimeter<br />
•	residence time of water<br />
•	Geo-name ID #<br />
 
SPARQL Query<br />
In order to create the dictionaries, I first built a SPARQL query containing all the given lake properties.. I used Wikidata Query Helper to create the SPARQL query:<br/> 
http://tinyurl.com/yccoohx2.<br /> 
Using SPARQLWrapper as an endpoint interface into Python so I could save the results as a dictionary, my query returned a JSON structure containing the properties listed above. This was then able to be manipulated and used to create the dictionaries.

Wikidata<br />
For the Wikidata dictionary, I used the Wikipedia lake page name as the key (parsed from the Wikipedia URL that was retrieved through the SPARQL query), with the dictionary of properties as the value. Basically a dictionary of dictionaries. Within each nested dictionary, the key/value pairs were saved as: lake property/property value. There was also a third dictionary within the Wikidata dictionary – a dictionary consisting of each lake that does not have a Wikipedia article, and thus no Wikipedia lake page name. For this dictionary, I used the Wikidata Qlabel from the lake’s Wikidata article. 

Wikipedia<br />
For the Wikipedia page, I used wptools 0.4.17, which contains Wikipedia tools (for humans) used for extracting data from Wikipedia, Wikidata, and other MediaWikis via Python. Wptools uses a Wikipedia article name as its argument, and can be used to parse any portion of a Wikipedia page. In this instance, I used it to parse the infoboxes. One limitation I encountered was wptools not being able to handle special characters, including apostrophes. As I iterated through the results from the SPARQL query, and in the same fashion as I created the key names for the Wikidata dictionary, I used the Wikipedia lake page name taken from the Wikipedia URL. I saved the results, which wptools saves in dictionary form, into a dictionary, using the same key/value structure as the Wikidata dictionaries. The output from wptools is less normalized than the output from the SPARQL query, since wptools basically is scraping from the actual page, so the results had to be stripped and manipulated to match the form used for the Wikidata dictionaries. For this I used regex to strip away any unnecessary characters, and manipulated the data output for any other edge cases as necessary. I’ll let the code and the comments within the code speak for the specifics. Once this dictionary was created, the comparisons could begin.

Comparison and Descriptive Statistics<br />
For the comparison, I saved the mismatches in a dictionary, which contained two dictionaries – Wikipedia and Wikidata. I also printed to a text file the name of lake, followed by any comparison mismatches. The descriptive statistics also output into a text file. 

Future Scope<br />
Moving forward, the two most pressing matters would be dealing with the special characters when using wptools to parse Wikipedia infoboxes, and finishing the comparison of all of the lake properties. Beyond that, searching through other Wikipedia’s abroad would be another goal. Also, within Wikipedia, I would need to verify that all edge cases and infobox templates were considered. Lastly, the SPARQL query itself should probably be worked on, to also gather more edge cases that I did not have an opportunity to explore. 
