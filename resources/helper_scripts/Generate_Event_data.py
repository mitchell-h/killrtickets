#!/usr/local/bin/python
# creates entries for an event
# mitchell.henderson@datastax.com
# CREATE TABLE IF NOT EXISTS seats_by_venue ( event_id uuid,
#                  section text,
#                  row text,
#                  seat text,
#                  taken boolean,
#                  primary key ((section, seat), row, event_id, date));

insert_seats_query = """INSERT INTO killrTickets.seats_by_venue (event_id, section, row, seat, taken) VALUES (?, ?, ?, ?, ?);"""

# how many events to generate data for
events = 1
# number of sections in the venue - seats in a section = rows * seats
sections = 12
rows_in_section = 12
seats_in_section = 12


# for now we'll have on event and generate the uuid for it.

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
def insert_for_event(event_id, seats):
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
    import uuid
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
