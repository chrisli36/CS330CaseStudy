import heapq
import math
import timeit
from datetime import datetime, timedelta
from collections import deque
from quadtree import QuadTree, QuadTreeNode
from DriverPQ import DriverPQ
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




# T1
class T1:
    def runT1(self, vertices, edges, drivers, passengers):
        # create graph
        graph = Graph()
        for vertex in vertices:
            graph.addVertex(vertex)
        for edge in edges:
            graph.addEdge(edge) 

        matchMaker = DriverPQ(passengers, drivers)
        
        count = 0
        while matchMaker.hasPassengers():
            print(count)
            count += 1
            # print(activeDrivers[0], activeDrivers[1])

            (passenger, (startTime, driver)) = matchMaker.getNextMatchT2()

            # t1 = timeit.default_timer()
            # calculate the closest vertices for the driver start, pickup, and dropoff
            driverStart = graph.closestVertex(driver.latitude, driver.longitude)
            passengerPickup = graph.closestVertex(passenger.source_lat, passenger.source_lon)
            passengerDropoff = graph.closestVertex(passenger.dest_lat, passenger.dest_lon)
            
            # # try quadtree 
            # max_lat = 0
            # max_lon = 0
            # min_lat = float("inf")
            # min_lon = float("inf")
            # for vertex in vertices:
            #     # find boundary
            #     if vertex.latitude > max_lat:
            #         max_lat = vertex.latitude
            #     if vertex.longitude > max_lon:
            #         max_lat = vertex.longitude
            #     if vertex.latitude < min_lat:
            #         min_lat = vertex.latitude
            #     if vertex.longitude < min_lon:
            #         min_lon = vertex.longitude
            
<<<<<<< Updated upstream
            # x = (min_lon + max_lon)/2
            # y = (min_lat + max_lat)/2
            # width = (min_lat + max_lat + 1)
            # height = (min_lon + max_lon + 1)
            # boundary = (x, y, width, height)
            # qt = QuadTree(boundary, 4)
=======

            boundary = (min_lat, min_lon, max_lat, max_lon)
            qt = QuadTree(boundary, 4)
            print(qt)
            
>>>>>>> Stashed changes
            
            # # build tree
            # for vertex in vertices:
            #     node = QuadTreeNode(vertex.latitude, vertex.longitude, vertex.id)
            #     qt.insert(node)
              
<<<<<<< Updated upstream
            # driverStart = QuadTree.find_closest(driver.latitude, driver.longitude, 0.01, 0.01)
            # passengerPickup = QuadTree.find_closest(passenger.source_lat, passenger.source_lon)
            # passengerDropoff = QuadTree.find_closest(passenger.dest_lat, passenger.dest_lon) 
            
            # print("driver start", driverStart)
=======
            driverStart = qt.find_closest(driver.latitude, driver.longitude, 0.01, 0.01)
            passengerPickup = qt.find_closest(passenger.source_lat, passenger.source_lon)
            passengerDropoff = qt.find_closest(passenger.dest_lat, passenger.dest_lon) 
            
            print("driver start", driverStart)
            print("passengerpickup", passengerPickup)
            print("passengerdropoff", passengerDropoff)
        
>>>>>>> Stashed changes
            
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

            # update the driver's ride profit by adding (-timetoPickup + timeToDropoff)
            driver.rideProfit += timeToDropoff - timeToPickup
            # update the driver's timeActive by adding (timetoPickup + timeToDropoff)
            thisRideDuration = timeToDropoff + timeToPickup
            driver.timeActive += thisRideDuration
            # update the driver's datetime
            driver.datetime = dropoffDatetime
            # add driver to pq only if not exiting
            if not driver.isExiting():
                matchMaker.pushPQ(driver, startTime + thisRideDuration)
            # t5 = timeit.default_timer()

            # print(t2 - t1, t3 - t2, t4 - t3, t5 - t4)

        avgWaitTime = matchMaker.getAvgWaitTime()
        avgRideProfit = matchMaker.getAvgRideProfit()

        print("Average total wait time for passengers: {}".format(avgWaitTime))
        print("Average ride profit for drivers: {}".format(avgRideProfit))


