# grape_lakes
INST 309 Independent Study - US Lakes Project

Project for independent study with Jonathan Brier @brierjon.

Plan of Action / Next Activities:
-- Build a query in Wikidata to find all US lakes
-- Each query should return a JSON - figure out how to look thru multiple results, and not just one result
-- Build text file or some data structure inside program
-- Recommended: dump query to text file so I don’t have to continuously work with API
-- Start by looking at Infobox on wikipedia

Proposed Activity:
Do Wikipedia scanning to pull in missing facts to Wikidata for Lakes in the USA English
-- Start with survey of what is missing in Wikidata
-- Start with survey of what is present in Wikipedia English
    - Could expand scope to other languages as a stretch

Known issues:
-- Not all Wikidata items have all the fields outlined in the Wikidata Project
-- Not all Wikipedia pages have instance of lake

Resources:
https://en.wikipedia.org/w/api.php
https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Lakes/Assessment
Wikidata ideal lake content that should be queryable: https://www.wikidata.org/wiki/Wikidata:WikiProject_Lakes
https://en.wikipedia.org/wiki/Template:Infobox_body_of_water


Example Wikidata Item: https://www.wikidata.org/wiki/Q4738340
Example Wikipedia Page: https://en.wikipedia.org/wiki/Alvord_Lake_(Arizona)

Notes
Scope of articles by quality and importance:
-- FA thru stub 
-- List thru NA = ignore

Wikidata - lake properties:
Known instances need to be queried:
-- not all lakes are listed under instance of lake
-- pond
-- groups of lakes
-- lagoons
-- glacial lake

To query if lake:
-- Coordinate location
-- instance of
-- country
