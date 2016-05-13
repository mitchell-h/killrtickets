#!/usr/local/bin/python
# creates entries for an event
# mitchell.henderson@datastax.com
# marc.selwan@datastax.com
# CREATE TABLE IF NOT EXISTS seats_by_venue ( event_id uuid,
#                  section text,
#                  row text,
#                  seat text,
#                  taken boolean,
#                  primary key ((section, seat), row, event_id));

#Imports
from cassandra import ConsistencyLevel
import uuid
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy, RetryPolicy, ExponentialReconnectionPolicy
import sys
import getopt


#Connection Constants
KEYSPACE = 'killrtickets'
CONSISTENCY = ConsistencyLevel.LOCAL_ONE
SEED_NODES = ['127.0.0.1']
DATACENTER = None

#Query Conetants
INSERT_SEATS = """INSERT INTO killrTickets.seats_by_venue (event_id, section, row, seat, taken) VALUES (?, ?, ?, ?, ?);"""


# how many events to generate data for
#EVENTS = 1
# number of sections in the venue - seats in a section = rows * seats
#SECTIONS = 12
#ROWS_IN_SECTION = 12
#SEATS_IN_SECTION = 12



#Connection Class
def connect(seeds, keyspace, datacenter=None, port=9042):

    class CustomRetryPolicy(RetryPolicy):

        def on_write_timeout(self, query, consistency, write_type,
                             required_responses, received_responses, retry_num):

            # retry at most 5 times regardless of query type
            if retry_num >= 5:
                return (self.RETHROW, None)

            return (self.RETRY, consistency)


    load_balancing_policy = None
    if datacenter:
        # If you are using multiple datacenters it's important to use
        # the DCAwareRoundRobinPolicy. If not then the client will
        # make cross DC connections. This defaults to round robin
        # which means round robin across all nodes irrespective of
        # data center.
        load_balancing_policy = DCAwareRoundRobinPolicy(local_dc=datacenter)

    cluster = Cluster(contact_points=seeds,
                      port=port,
                      default_retry_policy=CustomRetryPolicy(),
                      reconnection_policy=ExponentialReconnectionPolicy(1, 60),
                      load_balancing_policy=load_balancing_policy,
                      protocol_version=3)

    cluster.control_connection_timeout = 10.0
    cluster.compression = False
    session = cluster.connect(keyspace)
    print 'Connection established with %s at port %s' %(seeds,port)
    return session


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
                    q = connection.execute_async(INSERT_SEATS_PREP, [event_id, str(section), str(row), str(seat), False])
                except Exception as excep:
                    print("Error: %s" % excep)

if __name__ == '__main__':
    # this is for generating random seat data for events.
    #Get args

    try:
        options, args = getopt.getopt(
            sys.argv[1:], 'hc:i:', ['events=',
                                    'sections=',
                                    'rows=',
                                    'seats='
                                    ])
    except getopt.GetoptError, err:
        print str(err)
        print_help()
        sys.exit(2)

    for opt, arg in options:
        if opt in ('--events'):
            EVENTS = int(arg)
        elif opt in ('--sections'):
            SECTIONS = int(arg)
        elif opt in ('--rows'):
            ROWS_IN_SECTION = int(arg)
        elif opt in ('--seats'):
            SEATS_IN_SECTION = int(arg)
            sys.exit(2)


    #Defaults
    try:
        EVENTS
    except NameError:
        EVENTS = 1
    try:
        SECTIONS
    except NameError:
        SECTIONS = 12
    try:
        ROWS_IN_SECTION
    except NameError:
        ROWS_IN_SECTION = 12
    try:
        SEATS_IN_SECTION
    except NameError:
        SEATS_IN_SECTION = 12

    #Connect to your cluster
    connection = connect(SEED_NODES, keyspace=KEYSPACE, datacenter=DATACENTER)

    #Prepare Statement
    INSERT_SEATS_PREP = connection.prepare(INSERT_SEATS)

    for i in range(EVENTS):
        print('Injecting %d sections, %d rows per section and %d seats per section for event %d' % (SECTIONS, ROWS_IN_SECTION, SEATS_IN_SECTION, i+1))
        event_id = uuid.uuid1()
        seats = generate_section_seats(SECTIONS, ROWS_IN_SECTION, SEATS_IN_SECTION)
        insert_for_event(event_id, seats)
