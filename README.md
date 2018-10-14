# grape_lakes
INST 309 Independent Study - US Lakes Project

Project for independent study with Jonathan Brier @brierjon.

Plan of Action / Next Activities:<br />
-- Build a query in Wikidata to find all US lakes<br />
-- Each query should return a JSON - figure out how to look thru multiple results, and not just one result<br />
-- Build text file or some data structure inside program<br />
-- Recommended: dump query to text file so I don’t have to continuously work with API<br />
-- Start by looking at Infobox on wikipedia<br />

Proposed Activity:<br />
Do Wikipedia scanning to pull in missing facts to Wikidata for Lakes in the USA English<br />
-- Start with survey of what is missing in Wikidata<br />
-- Start with survey of what is present in Wikipedia English<br />
    - Could expand scope to other languages as a stretch<br />

Known issues:<br />
-- Not all Wikidata items have all the fields outlined in the Wikidata Project<br />
-- Not all Wikipedia pages have instance of lake<br />

Resources:<br />
https://en.wikipedia.org/w/api.php<br />
https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Lakes/Assessment<br />
Wikidata ideal lake content that should be queryable: https://www.wikidata.org/wiki/Wikidata:WikiProject_Lakes<br />
https://en.wikipedia.org/wiki/Template:Infobox_body_of_water<br />


Example Wikidata Item: https://www.wikidata.org/wiki/Q4738340<br />
Example Wikipedia Page: https://en.wikipedia.org/wiki/Alvord_Lake_(Arizona)<br />

Notes<br />
Scope of articles by quality and importance:<br />
-- FA thru stub<br />
-- List thru NA = ignore<br />

Wikidata - lake properties:<br />
Known instances need to be queried:<br />
-- not all lakes are listed under instance of lake<br />
-- pond<br />
-- groups of lakes<br />
-- lagoons<br />
-- glacial lake<br />

To query if lake:<br />
-- Coordinate location<br />
-- instance of<br />
-- country<br />
