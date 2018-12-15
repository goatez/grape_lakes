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

Project Goals:<br />
For this project, I am comparing the Wikipedia and Wikidata entries of all the lakes in the U.S. in an effort to identify any entries between the two that differ – particularly finding any missing or different characteristics within the Wikipedia entries in order to pull missing characteristics into the Wikidata:WikiProject_Lakes project. This may mean the entries for a specific characteristic of a lake do not match, or are just missing. Ultimately I intended to do Wikipedia scanning to pull in missing facts to Wikidata for Lakes in the U.S. Not all Wikidata items have all the property fields outlined in the Wikidata Project of U.S. Lakes, and not all Wikipedia pages have instances of the lakes within the Wikidata:WikiProject Lakes project.

Project Overview:<br />
In order to compare the Wikipedia and Wikidata U.S. Lake articles, I needed to create a dictionaries containing both entries, so that they can then be compared against each other, with any differing or missing lake properties saved in another dictionary.

Lake Properties:<br /> 
(as defined on the Wikidata page for the WikiProject Lakes)<br />

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
 
Additionally, the following fields were also included in my search:<br /> 

•	GNIS ID #<br />
•	Geo-name ID #<br />

Properties being compared:<br /> 
(For the sake of time and project complexity, I have scaled down the scope of the project that was initially proposed; and I will be comparing the following properties)<br />

•	elevation above sea level (elevation)<br />
•	area (area)<br />
•	length (length)<br />
•	width (width)<br />
•	volume as quantity (volume)<br />
•	vertical depth (depth)<br />
•	GNIS ID # (reference)<br />

Properties not being compared:<br /> 
(These are the lake properties that I will not be comparing, for sake of time and project complexity)<br />

•	coordinate location<br />
•	lake inflows<br />
•	lake outflow<br />
•	watershed area<br />
•	perimeter<br />
•	residence time of water<br />
•	Geo-name ID #<br />
 
SPARQL Query:<br />
In order to create the dictionaries, I first built a SPARQL query containing all the given lake properties, using the Wikidata Query Helper to create the query: http://tinyurl.com/yccoohx2.<br /> 
Using SPARQLWrapper as an endpoint interface into Python so I could save the results as a dictionary, my query returns a JSON structure containing the properties listed above. This was then able to be manipulated and used to create the dictionaries.

Wikidata:<br />
For the Wikidata dictionary, I used the Wikipedia lake page name as the key (parsed from the Wikipedia URL that was retrieved through the SPARQL query), with the dictionary of properties as the value. Basically a dictionary of dictionaries. Within each nested dictionary, the key/value pairs were saved as: lake property/property value. There was also a third dictionary within the Wikidata dictionary – a dictionary consisting of each lake that does not have a Wikipedia article, and thus no Wikipedia lake page name. For this dictionary, I used the Wikidata Qlabel from the lake’s Wikidata article. 

Wikipedia:<br />
For the Wikipedia page, I used wptools 0.4.17, which contains Wikipedia tools (for humans) used for extracting data from Wikipedia, Wikidata, and other MediaWikis via Python. Wptools uses a Wikipedia article name as its argument, and can parse any portion of a Wikipedia page. In this instance, I used it to parse the infoboxes. One limitation I encountered was wptools not being able to handle special characters, including apostrophes. As I iterated through the results from the SPARQL query, I used the Wikipedia lake page name taken from the Wikipedia URL as the key. I saved the results, which wptools saves in dictionary form, into a dictionary, using the same key/value structure as the Wikidata dictionaries. The output from wptools is less normalized than the output from the SPARQL query since wptools basically is scraping from the actual page, so the results had to be stripped and/or manipulated to match the form used for the Wikidata dictionaries. For this I used regex to strip away any unnecessary characters, and manipulated the data output for any other edge cases as necessary. Once this dictionary was created, the comparisons between Wikipedia and Wikidata U.S. lakes articles could begin.

Comparison and Descriptive Statistics:<br />
For the comparison, I saved the mismatches in a dictionary, which contained two dictionaries – one for properties of Wikipedia U.S. lake articles that do not match Wikidata, and the other dictionary for their non-matching Wikidata counterparts. I used this dictionary to output a list containing all mismatches of lake properties into a text file.  I also outputted to text file the descriptive statistics of the Wikipedia and Wikidata articles that were the basis of the comparisons. The descriptive statistics were of the lake properties that each dictionary contained, prior to the comparison.

Output Details:<br />
The code results in 4 different outputs: 3 text files and a screen print. The screen print is of the dictionary containing non-matching lake properties:<br /> 

lake_properties_not_matching<br />

The text file outputs are lake comparison mismatches, the lake dictionary descriptive statistics, and the lake names that wptools could not process, and thus were skipped.  The names of the outputted text files include:<br /> 

lake_comparison_mismatches<br />
lake_descriptive_statistics<br />
lake_names_could_not_compare<br />

Dictionaries/Lists of Interest which were created within the code:<br />
Since the code is dreadfully unreadable, here is a list of the end-result dictionaries that are created:<br />

Dictionary names (Short description)<br />
•	results[“results”][“bindings”] (results of SPARQL query prior to cleaning/manipulating)<br />
•	dict_wikipedia (wikipedia articles taken directly from wptools, prior to cleaning/manipulating)<br />
•	lake_dict (Wikidata and Wikipedia U.S. Lakes, created from results of SPARQL query)<br />
   •	lake_dict[‘wikidata_entries’]<br />
   •	lake_dict[‘wikidata_missing_properties’]<br />
   •	lake_dict[‘no_wikipedia_entries’]<br />
   •	lake_dict[‘wikipedia_entries’]<br />
•	lake_properties_not_matching (comparison mismatches from Wikidata and Wikipedia U.S. lakes)<br />
   •	lake_properties_not_matching[‘wikidata’]<br />
   •	lake_properties_not_matching[‘wikipedia’]<br />
•	bad_name (list containing names of lakes that wp.tools could not process, and thus were skipped)<br />

Future Scope:<br />
Moving forward, the two most pressing matters would be dealing with the special characters when using wptools to parse Wikipedia infoboxes, and finishing the comparison of all of the lake properties. Beyond that, searching through other Wikipedia’s abroad would be another goal. Also, within Wikipedia, I would need to verify that all edge cases and infobox templates were considered. Lastly, the SPARQL query itself should probably be worked on, to also gather more edge cases that I did not have an opportunity to explore. Also, my code is not easily readable, and I do recognize that. The use of several functions for the various aspects of the code would make it much cleaner and readable to others, but within the time constraints I was not able to accomplish that.
