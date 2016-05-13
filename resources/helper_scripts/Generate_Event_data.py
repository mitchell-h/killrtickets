#!/usr/local/bin/python
# creates entries for an event
# mitchell.henderson@datastax.com

import random, uuid

insert_seats_query = """INSERT INTO killrTickets.seats_by_venue (event_id, section, row, seat, taken) VALUES (?, ?, ?, ?, ?);"""

# how many events to generate data for
events = 1
# number of sections in the venue - seats in a section = rows * seats
sections = 12
rows_in_section = 12
seats_in_section = 12

genre = [ 'country', 'hip-hop', 'pop', 'rock', 'soul','jazz' ]
venues = ['00adc344-9fab-43a5-a140-616f6d9e2086', '8878e3b5-35f9-45d0-bdb9-e3db06c28516', '054c59cf-734f-428f-b520-7ec98f5020fb',
          '5c680ba6-dac0-484f-b250-fcb8640e9ebe', 'e0526dfa-172c-41cf-9906-74c884054235', '7e48e182-83d3-461c-baaa-e4556f719b20',
          '44a3891d-dbcd-47f5-be26-cbeeeaca8d23', '8cd14145-8a13-4996-8521-32ee343ec296', '040edf69-5400-48ba-8d2e-97939304e818',
          'a916f5a7-d239-4883-aef5-96d7904f2170', '417803f6-2078-4fed-b397-d310f62bf45d', '9d7e6e71-e7a8-4825-955a-d7b471595b6a',
          'bb161170-a93e-4a4c-87cd-59f73d9d7aa9']

#CREATE TABLE IF NOT EXISTS killrTickets.venue_by_id ( id uuid,
#                          venue_name text,
#                          venue_location text,
#                          PRIMARY KEY (venue_name,id));
def load_venues():
    pass
# for now we'll have on event and generate the uuid for it.
#CREATE TABLE IF NOT EXISTS killrTickets.events_by_id ( event_id uuid,
#                            name text,
#                            date TIMESTAMP,
#                            venue uuid,
#                            genre text,
#                            PRIMARY KEY (name, date));
def generate_event():
    ret_val = {}
    ret_val['event_id'] = uuid.uuid4()
    ret_val['name'] = 'name_of_event' + uuid.uuid(4)
    # GENERATE RANDOM FUTURE DATE HERE
    # ret_val['date'] = ''
    # need to generate venues first, or grab one and
    ret_val['venue'] = venue[random.randint(0,len(venue)-1)]
    ret_val['genre'] = genre[random.randint(0,len(genre)-1)]
    return ret_val

#

# returns a dict with {section: { row: [seats]}}
#                           5 sections, 7 rows, 12 seats per row
# seats = generate_section_seats(5,7,12)
def generate_section_seats(num_of_sections, rows_per_section, seats_per_section):
    ret = {}
    sea = 1
    for section_num in range(1, num_of_sections):
        ret[section_num] = {}
        for row in range(1, rows_per_section):
            ret[section_num][row] = []
            while sea <= seats_per_section:
                # print "section %s : seat %s" % (section_num, sea)
                ret[section_num][row].append(sea)
                sea = sea + 1
            row = row + 1
            sea = 0
        num_of_sections = num_of_sections + 1
        sea = 0
    return ret

# for generating seat data for events - randomish
# insert the data for the seats we're given for a given event_id
def insert_for_event(event_id, seats,status_report=False):
    counter=0
    for section in seats.keys():
        for row in seats[section].keys():
            for seat in seats[section][row]:
                # add failure detections here
                try:
                    q = sess.execute(insert_seats_query_preped, [event_id, str(section), str(row), str(seat), False])
                except Exception as excep:
                    print("Error: %s" % excep)

if __name__ == '__main__':
    # this is for generating random seat data for events.
    #import uuid
    from cassandra.cluster import Cluster
    from cassandra.auth import PlainTextAuthProvider
    from pprint import pprint

    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
    sess = cluster.connect()
    insert_seats_query_preped = sess.prepare(insert_seats_query)
    for i in range(events):
        print('Injecting %d sections, %d rows per section and %d seats per section for event %d' % (sections, rows_in_section, seats_in_section, i+1))
        event_id = uuid.uuid1()
        seats = generate_section_seats(sections, rows_in_section, seats_in_section)
        insert_for_event(event_id, seats)
