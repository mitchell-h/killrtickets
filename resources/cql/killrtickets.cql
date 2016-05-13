CREATE KEYSPACE IF NOT EXISTS killrTickets WITH replication = {'class': 'NetworkTopologyStrategy', 'Cassandra': 1 };

CREATE TABLE IF NOT EXISTS killrTickets.venue_by_id ( id uuid,
                          venue_name text,
                          venue_location text,
                          lat int,
                          lon int,
                          PRIMARY KEY (venue_name, id));

#CREATE TABLE IF NOT EXISTS killrTickets.events_by_id ( event_id uuid,
#                           name text,
#                            date TIMESTAMP,
#                            venue uuid,
#                            genre text,
#                            lat text,
#                            lon text,
#                            PRIMARY KEY (name, date));

CREATE TABLE IF NOT EXISTS killrtickets.event_by_location (
     event_name text,
     venue_location text,
     event_date timestamp,
     section text,
     row text,
     seat text,
     date_taken timestamp,
     genre text,
     taken boolean,
     venue_name text,
     lat text,
     lon text,
     PRIMARY KEY ((event_name, venue_location), event_date, section, row, seat)
);

CREATE TABLE IF NOT EXISTS killrTickets.seats_by_venue ( event_id uuid,
                      section text,
                      row text,
                      seat text,
                      taken boolean,
                      date_taken TIMESTAMP,
                      primary key ((event_id, section), row, seat));


# need to dsetool create_core killrTickets.events_by_id
# needed for solr searching of event name.