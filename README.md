visitors_bureau_final
=====================
server.py takes data from two json files, 'businesses.json' and 'events.json', and gives the website user (an admin) the ability to add (POST) and edit (PATCH) resources in the html files (businesses, business, events and event).  A POST form in businesses.html allows you to enter a new business. business.html has a PATCH method which non-idempotently allows the user to edit a resource. 

Microdata then allows the user to interoperate with other services.

rel=alternate and rel=collection are used to indicate alternate paths and collections of items, respectively.
