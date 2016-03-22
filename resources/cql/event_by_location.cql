CREATE KEYSPACE IF NOT EXISTS killrTickets WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1 };
CREATE TABLE IF NOT EXISTS killrTickets.event_by_location ( 
venue_name text,
venue_location text,
event_name text,
event_date TIMESTAMP,
genre text,
section text,
row text,
seat text,
taken boolean,
date_taken TIMESTAMP,
primary key ((event_name, venue_location), event_date, section, row, seat));
