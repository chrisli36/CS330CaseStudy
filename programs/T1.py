import heapq
import math
import timeit
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
    def runT1v2(self, graph, drivers, passengers):

        # passenger queue
        passengers = deque(passengers)
        simulatedPassengers = []

        # driver priority queue sorted by the next time they will be active
        STARTTIME = drivers[0].datetime
        activeDrivers = []
        for driver in drivers:
            wrapper = ((driver.datetime - STARTTIME).total_seconds(), driver)
            activeDrivers.append(wrapper)
        
        count = 0
        while passengers:
            print(count)
            count += 1
            # print(activeDrivers[0], activeDrivers[1])
            startTime, driver = heapq.heappop(activeDrivers)
            passenger = passengers.popleft()

            # t1 = timeit.default_timer()
            # calculate the closest vertices for the driver start, pickup, and dropoff
            driverStart = graph.closestVertex(driver.latitude, driver.longitude)
            passengerPickup = graph.closestVertex(passenger.source_lat, passenger.source_lon)
            passengerDropoff = graph.closestVertex(passenger.dest_lat, passenger.dest_lon)
            # t2 = timeit.default_timer()

            # calculate the time to pickup in seconds and record the datetime of pickup
            dayType = 'weekday' if driver.datetime.weekday() < 5 else 'weekend'
            hour = driver.datetime.hour
            timeToPickup = graph.dijkstra(driverStart, passengerPickup, dayType, hour)
            pickupDatetime = driver.datetime + timedelta(seconds=timeToPickup)
            # t3 = timeit.default_timer()

            # caluclate the time to dropoff in seconds and record the datetime of dropoff
            dayType = 'weekday' if pickupDatetime.weekday() < 5 else 'weekend'
            hour = pickupDatetime.hour
            timeToDropoff = graph.dijkstra(passengerPickup, passengerDropoff, dayType, hour)
            dropoffDatetime = pickupDatetime + timedelta(seconds=timeToDropoff)
            # t4 = timeit.default_timer()

            # update passenger's total wait time as time it took for driver to become active + pickup + dropoff
            waitTimeForActiveDriver = max(0, (driver.datetime - passenger.datetime).total_seconds())
            passenger.waitTime = waitTimeForActiveDriver + timeToPickup + timeToDropoff
            simulatedPassengers.append(passenger)

            # update the driver's ride profit by adding (-timetoPickup + timeToDropoff)
            driver.rideProfit += timeToDropoff - timeToPickup
            # update the driver's timeActive by adding (timetoPickup + timeToDropoff)
            thisRideDuration = timeToDropoff + timeToPickup
            driver.timeActive += thisRideDuration
            # update the driver's datetime
            driver.datetime = dropoffDatetime
            # add driver to pq only if not exiting
            if not driver.isExiting():
                heapq.heappush(activeDrivers, (startTime + thisRideDuration, driver))
            # t5 = timeit.default_timer()

            # print(t2 - t1, t3 - t2, t4 - t3, t5 - t4)

        totalWaitTime = 0
        for passenger in simulatedPassengers:
            totalWaitTime += passenger.waitTime
        avgWaitTime = totalWaitTime / len(simulatedPassengers)

        totalRideProfit = 0
        for driver in drivers:
            totalRideProfit += driver.rideProfit
        avgRideProfit = totalRideProfit / len(drivers)

        print("Average total wait time for passengers: {}".format(avgWaitTime))
        print("Average ride profit for drivers: {}".format(avgRideProfit))



    # def runT1(self, graph, drivers, passengers):
    #     # give id to driver to distinguish driver
    #     for i, driver in enumerate(drivers):
    #         driver['id'] = i
            
    #     total_passenger_wait_time = 0
    #     total_driver_active_time = 0
    #     driver_active_times = {driver['id']: 0 for driver in drivers}
        
    #     # add queue
    #     waiting_passengers = deque(passengers)
        
    #     # loop until all passengers are served or no driver available
    #     while waiting_passengers and drivers:
    #         passenger = waiting_passengers.popleft()
    #         p_vertex = graph.closestVertex(passenger['source_lat'], passenger['source_lon'])
    #         dropoff_vertex = graph.closestVertex(passenger['dest_lat'], passenger['dest_lon'])

    #         nearest_driver = None
    #         min_time_to_pickup = None
            
    #         # earliest available driver
    #         for driver in drivers:
    #             if not nearest_driver or driver['datetime'] < nearest_driver['datetime']:
    #                 nearest_driver = driver
    #                 d_vertex = graph.closestVertex(driver['latitude'], driver['longitude'])
    #                 day_type = 'weekday' if (driver['datetime']).weekday() < 5 else 'weekend'
    #                 hour = driver['datetime'].hour
                    
    #                 min_time_to_pickup = graph.dijkstra(d_vertex, p_vertex, day_type, hour)
                    
    #                 #print(min_time_to_pickup)

    #         if nearest_driver:
    #             passenger_wait_time = (passenger['datetime'] - nearest_driver['datetime']).total_seconds()
    #             total_passenger_wait_time += passenger_wait_time
                
    #             time_to_dropoff = graph.dijkstra(p_vertex, dropoff_vertex, day_type, hour)

    #             trip_time = min_time_to_pickup + time_to_dropoff
    #             total_driver_active_time += trip_time
    #             print("trip time:", trip_time)
    #             print("total drver active time", total_driver_active_time)
    #             print("total passenger wait time", total_passenger_wait_time)
                
    #             # update active time with driver id
    #             driver_active_times[nearest_driver['id']] += trip_time

    #             # update driver location and time
    #             nearest_driver['latitude'], nearest_driver['longitude'] = passenger['dest_lat'], passenger['dest_lon']
    #             nearest_driver['datetime'] = nearest_driver['datetime'] + timedelta(seconds=time_to_dropoff)

    #             # Check if driver's active time exceeds 8 hours
    #             if driver_active_times[nearest_driver['id']] >= 28800:
    #                 drivers.remove(nearest_driver)

    #     total_passenger_wait_time /= 60  # Convert to minutes
    #     total_driver_active_time /= 60   # Convert to minutes

    #     print("Total Passenger Wait Time (D1):", total_passenger_wait_time, "minutes")
    #     print("Total Driver Active Time (D2):", total_driver_active_time, "minutes")
        
        
    
   