# killrtickets
Uses python 2.7.

Fictional ticketing agency wants to base ticketing around DataStax.

Database schema at resources/cql/killrtickets.cql

Generate seats for an event at resources/helper_scripts/Generate_Event_data.py

# killrtickets Banana Dashboard Setup

1. CREATE SCHEMA

$   cqlsh -f event_by_location.cql


2. LOAD SCHEMA (requires event_list.sh and EbyL_insert.py)

$  ./event_list.sh


3. CREATE INDEX 

Post Config (Heap is set to 4GB. Modify before posting if necessary):

 	$  curl http://localhost:8983/solr/resource/killrtickets.event_by_location/solrconfig.xml --data-binary @solrconfig.xml -H 'Content-type:text/xml; charset=utf-8'

Post Schema:

$  curl http://localhost:8983/solr/resource/killrtickets.event_by_location/schema.xml  --data-binary @schema.xml -H 'Content-type:text/xml; charset=utf-8'

Create Core:

$ curl "http://localhost:8983/solr/admin/cores?action=CREATE&name=killrtickets.event_by_location”

4. CONFIGURE BANANA

a. Download banana_release.zip from: https://github.com/lucidworks/banana/archive/release.zip

b. Copy to [dse_home]/solr/web/demos and unzip

c. Open browser and navigate to: http://localhost:8983/demos/banana_release/src/index.html#/dashboard

d. In the upper Right corner click the “Load” icon and open the killrtickets_dashboard file





