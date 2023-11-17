import timeit
from datetime import datetime, timedelta
from PassengerDriverSim import PassengerDriverSim
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


class Simulator:
    def runT1(self, vertices, edges, drivers, passengers):
        self.runGeneralSimulation()

    def runT1(self, vertices, edges, drivers, passengers):
        # create graph
        graph = Graph(vertices, edges)
        matchMaker = PassengerDriverSim(passengers, drivers)
        
        count = 0
        while matchMaker.hasPassengers():
            print(count)
            count += 1
            # print(activeDrivers[0], activeDrivers[1])

            (passenger, (startTime, driver)) = matchMaker.getNextMatchT1()

            t1 = timeit.default_timer()
            # calculate the closest vertices for the driver start, pickup, and dropoff
            driverStart = graph.find_closestQT(driver.latitude, driver.longitude)
            passengerPickup = graph.find_closestQT(passenger.source_lat, passenger.source_lon)
            passengerDropoff = graph.find_closestQT(passenger.dest_lat, passenger.dest_lon) 
            
            # print("driver start", driverStart)
            # print("passengerpickup", passengerPickup)
            # print("passengerdropoff", passengerDropoff)
         
            t2 = timeit.default_timer()
            # calculate the time to pickup in seconds and record the datetime of pickup
            dayType = 'weekday' if driver.datetime.weekday() < 5 else 'weekend'
            hour = driver.datetime.hour
            timeToPickup = graph.dijkstra(driverStart, passengerPickup, dayType, hour)
            pickupDatetime = driver.datetime + timedelta(seconds=timeToPickup)
            t3 = timeit.default_timer()

            # caluclate the time to dropoff in seconds and record the datetime of dropoff
            dayType = 'weekday' if pickupDatetime.weekday() < 5 else 'weekend'
            hour = pickupDatetime.hour
            timeToDropoff = graph.dijkstra(passengerPickup, passengerDropoff, dayType, hour)
            dropoffDatetime = pickupDatetime + timedelta(seconds=timeToDropoff)
            t4 = timeit.default_timer()

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
            t5 = timeit.default_timer()

            print(t2 - t1, t3 - t2, t4 - t3, t5 - t4)

        avgWaitTime = matchMaker.getAvgWaitTime()
        avgRideProfit = matchMaker.getAvgRideProfit()

        print("Average total wait time for passengers: {}".format(avgWaitTime))
        print("Average ride profit for drivers: {}".format(avgRideProfit))


