CREATE KEYSPACE IF NOT EXISTS killrTickets WITH replication = {'class': 'NetworkTopologyStrategy', 'dc1': 1 };

CREATE TABLE IF NOT EXISTS killrTickets.venue_by_id ( id uuid,
                          venue_name text,
                          venue_location text,
                          PRIMARY KEY (venue_name,id));

CREATE TABLE IF NOT EXISTS killrTickets.events_by_id ( event_id uuid,
                            name text,
                            date TIMESTAMP,
                            venue uuid,
                            PRIMARY KEY (name, date));

CREATE TABLE IF NOT EXISTS killrTickets.seats_by_venue ( event_id uuid,
                  section text,
                  row text,
                  seat text,
                  taken boolean,
                  primary key ((section, seat), row, event_id));

#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '1', false);
#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '2', false);
#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '3', false);
#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '4', false);
#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '5', false);
#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '6', false);
#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '7', false);
#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '8', false);
#INSERT INTO seats_by_venue (event_id, section, row, seat, taken) VALUES (cd896ed9-35a5-4019-81ec-2cb8cb6bbaba, '1', '1', '9', false);

#UPDATE seats_by_venue SET taken = true where event_id = cd896ed9-35a5-4019-81ec-2cb8cb6bbaba AND section = '1' AND seat = '3' AND row = '1' IF taken = false;
