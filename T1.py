import json
import csv
import heapq
import math
from datetime import datetime, timedelta
import timeit
from collections import deque

# T1
class T1:
    def baseline_algorithm(self, graph, drivers, passengers):
        # give id to driver to distinguish driver
        for i, driver in enumerate(drivers):
            driver['id'] = i

        # track 
        total_passenger_wait_time = 0
        total_driver_active_time = 0
        driver_active_times = {driver['id']: 0 for driver in drivers}
        
        for passenger in passengers:
            p_vertex = graph.closestVertex(passenger['source_lat'], passenger['source_lon'])
            dropoff_vertex = graph.closestVertex(passenger['dest_lat'], passenger['dest_lon'])

            nearest_driver = None
            min_distance = float('infinity')
            min_time_to_pickup = None
            

            for driver in drivers:
                d_vertex = graph.closestVertex(driver['latitude'], driver['longitude'])
                day_type = 'weekday' if (driver['datetime']).weekday() < 5 else 'weekend'
                hour = driver['datetime'].hour

                time_to_pickup = graph.dijkstra(d_vertex, p_vertex, day_type, hour)
                time_to_dropoff = graph.dijkstra(p_vertex, dropoff_vertex, day_type, hour)
                
                #print(time_to_dropoff)
                #print(time_to_pickup)

                if time_to_pickup < min_distance:
                    min_distance = time_to_pickup
                    min_time_to_pickup = time_to_pickup
                    nearest_driver = driver

            if nearest_driver:
                passenger_wait_time = (passenger['datetime'] -nearest_driver['datetime']).total_seconds()
                total_passenger_wait_time += passenger_wait_time

                trip_time = min_time_to_pickup + time_to_dropoff
                total_driver_active_time += trip_time
                
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

        #print("Total Passenger Wait Time (D1):", total_passenger_wait_time, "minutes")
        #print("Total Driver Active Time (D2):", total_driver_active_time, "minutes")
        
        
    
   