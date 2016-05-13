# killrtickets
Uses python 2.7.

Fictional ticketing agency wants to base ticketing around DataStax.

Database schema at resources/cql/killrtickets.cql

Generate seats for an event at resources/helper_scripts/Generate_Event_data.py

# killrtickets Banana Dashboard Setup

CREATE SCHEMA

$   cqlsh -f event_by_location.cql

LOAD SCHEMA (requires event_list.sh and EbyL_insert.py)

$  ./event_list.sh

CREATE INDEX 

Post Config (Heap is set to 4GB. Modify before posting if necessary):

$  curl http://localhost:8983/solr/resource/killrtickets.event_by_location/solrconfig.xml --data-binary @solrconfig.xml -H 'Content-type:text/xml; charset=utf-8'

Post Schema:

$  curl http://localhost:8983/solr/resource/killrtickets.event_by_location/schema.xml  --data-binary @schema.xml -H 'Content-type:text/xml; charset=utf-8'

Create Core:

$ curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=killrtickets.event_by_location”

CONFIGURE BANANA

Download banana_release.zip from: https://github.com/lucidworks/banana/archive/release.zip

Copy to [dse_home]/solr/web/demos and unzip

Open browser and navigate to: http://localhost:8983/demos/banana_release/src/index.html#/dashboard

In the upper Right corner click the “Load” icon and open the killrtickets_dashboard file



#Application

The star of the show, light weight transactions.

'UPDATE killrTickets.seats_by_venue SET taken = True where event_id = 303b988c-1895-11e6-b7ee-a45e60df86d9 AND  section = '10' AND row = '1' and seat = '1' IF taken = False;'

User work flow is pretty simple.  

User selects an event they'd like to see.  

Selects a section they'd like to sit in.  We pull that section data back and verify there are seats avilable.

We issue a request to the queue works to purchase the seats.  

If seat purchase fails for any of the seats we back out the changes.



We also use the geospacial searching ability of DSE Search to recommond other shows near the event.


