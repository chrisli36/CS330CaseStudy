import timeit
from datetime import datetime, timedelta
from PassengerDriverSim import PassengerDriverSim
from Graph import Graph
import csv

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

    def setProblem(self, version):
        self.version = version

    def getNextMatch(self, matchmaker, graph):
        if self.version == "T1":
            return matchmaker.getNextMatchT1()
        elif self.version == "T2":
            return matchmaker.getNextMatchT2(graph)
        elif self.version == "T3":
            return matchmaker.getNextMatchT3(graph)
        elif self.version == "T5":
            return matchmaker.getNextMatchT5(graph)
        print("Simulator does not contain version {}".format(self.version))
        return False

    def runSimulation(self, vertices, edges, drivers, passengers):
        # create graph
        graph = Graph(vertices, edges)
        matchMaker = PassengerDriverSim(passengers, drivers)
        
        count = 0
        while matchMaker.hasPassengers() and count < 200:
            print(count)
            count += 1

            t0 = timeit.default_timer()
            (startDatetime, passenger, driver) = self.getNextMatch(matchMaker, graph)

            t1 = timeit.default_timer()
            # calculate the closest vertices for the driver start, pickup, and dropoff
            driverStart = graph.closestVertexQT(driver.latitude, driver.longitude)
            passengerPickup = graph.closestVertexQT(passenger.source_lat, passenger.source_lon)
            passengerDropoff = graph.closestVertexQT(passenger.dest_lat, passenger.dest_lon) 
            
            t2 = timeit.default_timer()
            # calculate the time to pickup in seconds and record the datetime of pickup
            timeToPickup = graph.dijkstra(driverStart, passengerPickup, startDatetime)
            pickupDatetime = startDatetime + timedelta(seconds=timeToPickup)
            
            t3 = timeit.default_timer()
            # caluclate the time to dropoff in seconds and record the datetime of dropoff
            timeToDropoff = graph.dijkstra(passengerPickup, passengerDropoff, pickupDatetime)
            dropoffDatetime = pickupDatetime + timedelta(seconds=timeToDropoff)
            
            t4 = timeit.default_timer()
            # update passenger's total wait time as time it took for driver to become active + pickup + dropoff
            waitTimeToGetActiveDriver = max(0, (driver.datetime - passenger.datetime).total_seconds())
            passenger.waitTime = waitTimeToGetActiveDriver + timeToPickup + timeToDropoff
            # update the driver's ride profit by adding (-timetoPickup + timeToDropoff)
            driver.rideProfit += timeToDropoff - timeToPickup
            # update the driver's datetime
            driver.datetime = dropoffDatetime
            # update the driver's location
            driver.lat = passenger.dest_lat
            driver.lon = passenger.dest_lon
            # add driver to pq only if not exiting
            if not driver.isExiting():
                matchMaker.pushPQ(driver, dropoffDatetime)
            
            t5 = timeit.default_timer()
            print("match: {}, closest: {}, path1: {}, path2: {}, update: {}".format(t1 - t0, t2 - t1, t3 - t2, t4 - t3, t5-t4))

        waitTimes = matchMaker.getAvgWaitTime()
        rideProfits = matchMaker.getAvgRideProfit()


        with open("{} results.csv".format(self.version), "w") as f:
            write = csv.writer(f)
            write.writerow(waitTimes)
            write.writerow(rideProfits)

        print("Average total wait time for passengers: {}".format(sum(waitTimes) / len(waitTimes)))
        print("Average ride profit for drivers: {}".format(sum(rideProfits) / len(rideProfits)))


