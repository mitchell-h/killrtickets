#!/usr/local/bin/python
#Imports
import random
from random import randrange
from datetime import datetime
from datetime import timedelta
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.policies import DCAwareRoundRobinPolicy, RetryPolicy, ExponentialReconnectionPolicy
import sys


#Schema
# CREATE TABLE killrtickets.event_by_location (
#     event_name text,
#     venue_location text,
#     event_date timestamp,
#     section text,
#     row text,
#     seat text,
#     date_taken timestamp,
#     genre text,
#     taken boolean,
#     venue_name text,
#     PRIMARY KEY ((event_name, venue_location), event_date, section, row, seat)
# )


#Connection Constants
KEYSPACE = 'killrtickets'
CONSISTENCY = ConsistencyLevel.LOCAL_ONE
SEED_NODES = ['127.0.0.1']
DATACENTER = None

#INSERT constants

INSERT_NOT_TAKEN = """INSERT INTO event_by_location (venue_name, venue_location, event_name, event_date, genre, section, row, seat, taken, date_taken)
VALUES (?,?,?,?,?,?,?,?,?,?)"""

INSERT_TAKEN = """INSERT INTO event_by_location (venue_name, venue_location, event_name, event_date, genre, section, row, seat, taken, date_taken)
VALUES (?,?,?,?,?,?,?,?,?,?)"""


#Event details args for data load

venue_name = str(sys.argv[1])
venue_location = str(sys.argv[2])
event_name = str(sys.argv[3])
event_date = datetime.strptime(str(sys.argv[4]), '%Y-%m-%d %I:%M:%S')
print event_date
genre = str(sys.argv[5])
not_takenTS = datetime.strptime('2016-03-20 01:00:00','%Y-%m-%d %I:%M:%S')
d1 = datetime.strptime('3/17/2016 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('3/21/2016 8:00 PM', '%m/%d/%Y %I:%M %p')


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


def takenTS(start, end):
    # generate random timestamp between two dates
    delta = end - start
    int_delta = (delta.days *24 *60 *60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def insert_events():
    for i, section in enumerate(['MEZZ','ORCH','BALC']):
        for row in 'ABCD':
            for seat in range(1,13):
                taken = bool(random.getrandbits(1))
                if taken:
                    connection.execute_async(INSERT_NOT_TAKEN_PREP, [venue_name, venue_location, event_name, event_date, genre, section, row, str(seat), taken, takenTS(d1,d2)])

                else:
                    connection.execute_async(INSERT_TAKEN_PREP, [venue_name, venue_location, event_name, event_date, genre, section, row, str(seat), taken, not_takenTS])

if __name__ == '__main__':

    #Connect to your cluster
    connection = connect(SEED_NODES, keyspace=KEYSPACE, datacenter=DATACENTER)

    #Prepare Statement
    INSERT_NOT_TAKEN_PREP = connection.prepare(INSERT_NOT_TAKEN)
    INSERT_TAKEN_PREP = connection.prepare(INSERT_TAKEN)

    #Insert
    insert_events()