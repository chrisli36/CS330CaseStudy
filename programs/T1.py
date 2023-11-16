import heapq
import math
from datetime import datetime, timedelta
from collections import deque

# Whenever riders join the queue, they'll have a waiting time that starts ticking up. 
# T1 asks that you make no optimizations on distance and simply only use FIFO operations 
# as soon as drivers become available. 

# Task 2: Suppose at some point in time you have more passengers arriving but all of 
# your drivers are currently busy [indeed, you may need to use the graph to estimate
# how long your drivers would be busy on a particular ride]. Then you cannot 
# immediately match these drivers. The simple policy in T1 suggests, as a baseline, 
# that whenever a driver becomes available again, you match them to whichever passenger 
# has been waiting the longest.

"""
need:
FIFO for passengers
earliest available driver
passenger wait time calculation
trip time calculation    
    
"""


# T1
class T1:
    def baseline_algorithm(self, graph, drivers, passengers):
        # give id to driver to distinguish driver
        for i, driver in enumerate(drivers):
            driver['id'] = i
            
        total_passenger_wait_time = 0
        total_driver_active_time = 0
        driver_active_times = {driver['id']: 0 for driver in drivers}
        
        # add queue
        waiting_passengers = deque(passengers)
        
        # loop until all passengers are served or no driver available
        while waiting_passengers and drivers:
            passenger = waiting_passengers.popleft()
            p_vertex = graph.closestVertex(passenger['source_lat'], passenger['source_lon'])
            dropoff_vertex = graph.closestVertex(passenger['dest_lat'], passenger['dest_lon'])

            nearest_driver = None
            min_time_to_pickup = None
            
            # earliest available driver
            for driver in drivers:
                if not nearest_driver or driver['datetime'] < nearest_driver['datetime']:
                    nearest_driver = driver
                    d_vertex = graph.closestVertex(driver['latitude'], driver['longitude'])
                    day_type = 'weekday' if (driver['datetime']).weekday() < 5 else 'weekend'
                    hour = driver['datetime'].hour
                    
                    min_time_to_pickup = graph.dijkstra(d_vertex, p_vertex, day_type, hour)
                    
                    #print(min_time_to_pickup)

            if nearest_driver:
                passenger_wait_time = (passenger['datetime'] - nearest_driver['datetime']).total_seconds()
                total_passenger_wait_time += passenger_wait_time
                
                time_to_dropoff = graph.dijkstra(p_vertex, dropoff_vertex, day_type, hour)

                trip_time = min_time_to_pickup + time_to_dropoff
                total_driver_active_time += trip_time
                print("trip time:", trip_time)
                print("total drver active time", total_driver_active_time)
                print("total passenger wait time", total_passenger_wait_time)
                
                # update active time with driver id
                driver_active_times[nearest_driver['id']] += trip_time

                # update driver location and time
                nearest_driver['latitude'], nearest_driver['longitude'] = passenger['dest_lat'], passenger['dest_lon']
                nearest_driver['datetime'] = nearest_driver['datetime'] + timedelta(seconds=time_to_dropoff)

                # Check if driver's active time exceeds 8 hours
                if driver_active_times[nearest_driver['id']] >= 28800:
                    drivers.remove(nearest_driver)

        total_passenger_wait_time /= 60  # Convert to minutes
        total_driver_active_time /= 60   # Convert to minutes

        print("Total Passenger Wait Time (D1):", total_passenger_wait_time, "minutes")
        print("Total Driver Active Time (D2):", total_driver_active_time, "minutes")
        
        
    
   