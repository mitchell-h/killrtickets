#!/usr/loca/bin/python
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid
from pprint import pprint

KEYSPACE = 'killrtickets'
CONSISTENCY = 'ConsistencyLevel.LOCAL_ONE'
SEED_NODES = ['127.0.0.1']
DATACENTER = None


# Connection Class
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
        load_balancing_policy = DCAwareRoundRobinPolicy(local_dc=DATACENTER)

    cluster = Cluster(contact_points=seeds,
                      port=port,
                      default_retry_policy=CustomRetryPolicy(),
                      reconnection_policy=ExponentialReconnectionPolicy(1, 60),
                      load_balancing_policy=load_balancing_policy,
                      protocol_version=3)

    cluster.control_connection_timeout = 10.0
    cluster.compression = False
    session = cluster.connect(keyspace)
    print 'Connection established with %s at port %s' % (seeds, port)
    return session


# need to add abiltiy to buy a range of seats
def buy_seat(event, section, row, seats=[]):
    results = {}
    buy_statement = 'UPDATE killrTickets.seats_by_venue SET taken = True WHERE event_id = ? AND section = ? AND row = ? AND seat = ? IF taken = False;'
    prepped_buy = sess.prepare(buy_statement)
    for seat in seats:
        res = sess.execute(prepped_buy, [uuid.UUID(event), section, row, seat])
        if res[0].applied == False:
            print("Failed to apply: event %s, section %s, row %s, seat %s") % (str(event), str(section), str(row), str(seat) )
            results[seat] = "False"
            # add logic here to deal with any failures
        elif res[0].applied == True:
            print("GOT: event %s, section %s, row %s, seat %s") % (str(event), str(section), str(row), str(seat) )
            results[seat] = "True"
    return results


if __name__ == '__main__':
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['127.0.0.1'], auth_provider=auth_provider)
    sess = cluster.connect()
    uuid_of_event = '303b988c-1895-11e6-b7ee-a45e60df86d9'
    section_of_event = '4'
    row_of_event = '1'
    seats_at_event = '6'
    res = buy_seat(uuid_of_event, section_of_event, row_of_event, seats_at_event)
    for se in res: # decide what to do with any seats that failed to be obtained here
        pass        # backout seat buys?
