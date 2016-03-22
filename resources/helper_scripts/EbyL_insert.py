#!/usr/local/bin/python
import random
import uuid
import sys
from datetime import datetime
from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect('killrtickets')

def takenTS(start, end):
# generate random timestamp between two dates
	from random import randint
	from random import randrange
	from datetime import timedelta

	delta = end - start
	int_delta = (delta.days *24 *60 *60) + delta.seconds
	random_second = randrange(int_delta)
	return start + timedelta(seconds=random_second)

# starting and ending date range for ticket purchase
d1 = datetime.strptime('3/17/2016 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('3/21/2016 8:00 PM', '%m/%d/%Y %I:%M %p')

# event details
venue_name = str(sys.argv[1]) 
venue_location = str(sys.argv[2])
event_name = str(sys.argv[3])
event_date = str(sys.argv[4])
genre = str(sys.argv[5])
not_takenTS = '2016-03-20 01:00:00'

for i, section in enumerate(['MEZZ','ORCH','BALC']):
	for row in 'ABCD':
		for seat in range(1,13):
			taken = bool(random.getrandbits(1))
			if taken: 
				session.execute(
					"""
					INSERT INTO event_by_location (venue_name, venue_location, event_name, event_date, genre, section, row, seat, taken, date_taken)
					VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
					""",
					(venue_name,venue_location,event_name,event_date,genre,section,row,str(seat),taken,takenTS(d1,d2)) 
				)
			else:
		 		session.execute(
                                        """
                                        INSERT INTO event_by_location (venue_name, venue_location, event_name, event_date, genre, section, row, seat, taken, date_taken)
                                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                        """,
                                        (venue_name,venue_location,event_name,event_date,genre,section,row,str(seat),taken,not_takenTS)
                                )
			


