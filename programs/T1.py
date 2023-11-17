import heapq
import math
import timeit
from datetime import datetime, timedelta
from collections import deque
from quadtree import QuadTree, QuadTreeNode
from Graph import Graph

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
    def runT1v2(self, vertices, edges, drivers, passengers):
        # create graph
        graph = Graph()
        for vertex in vertices:
            graph.addVertex(vertex)
        for edge in edges:
            graph.addEdge(edge) 

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
            #driverStart = graph.closestVertex(driver.latitude, driver.longitude)
            #passengerPickup = graph.closestVertex(passenger.source_lat, passenger.source_lon)
            #passengerDropoff = graph.closestVertex(passenger.dest_lat, passenger.dest_lon)
            
            # try quadtree 
            max_lat = 0
            max_lon = 0
            min_lat = float("inf")
            min_lon = float("inf")
            for vertex in vertices:
                # find boundary
                if vertex.latitude > max_lat:
                    max_lat = vertex.latitude
                if vertex.longitude > max_lon:
                    max_lat = vertex.longitude
                if vertex.latitude < min_lat:
                    min_lat = vertex.latitude
                if vertex.longitude < min_lon:
                    min_lon = vertex.longitude
            
            x = (min_lon + max_lon)/2
            y = (min_lat + max_lat)/2
            width = (min_lat + max_lat + 1)
            height = (min_lon + max_lon + 1)
            boundary = (x, y, width, height)
            qt = QuadTree(boundary, 4)
            
            # build tree
            for vertex in vertices:
                node = QuadTreeNode(vertex.latitude, vertex.longitude, vertex.id)
                qt.insert(node)
              
            driverStart = QuadTree.find_closest(driver.latitude, driver.longitude, 0.01, 0.01)
            passengerPickup = QuadTree.find_closest(passenger.source_lat, passenger.source_lon)
            passengerDropoff = QuadTree.find_closest(passenger.dest_lat, passenger.dest_lon) 
            
            print("driver start", driverStart)
            
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


