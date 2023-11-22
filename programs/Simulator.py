import timeit
from datetime import datetime, timedelta
from PassengerDriverSim import PassengerDriverSim
from Graph import Graph
import csv
import math

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
        elif self.version == "T4":
            return matchmaker.getNextMatchT4(graph)
        elif self.version == "T5":
            return matchmaker.getNextMatchT5(graph)
        print("Simulator does not contain version {}".format(self.version))
        return False
    
    def roundSignificantDigits(self, num, numSignficant):
        return round(num, numSignficant - int(math.floor(math.log10(abs(num)))) - 1)

    def runSimulation(self, vertices, edges, drivers, passengers):
        print("Running for problem {}".format(self.version))

        # create graph
        graph = Graph(vertices, edges)
        matchMaker = PassengerDriverSim(passengers, drivers)
        
        count = 0
        while matchMaker.hasPassengers(): # and count < 1000:
            count += 1

            t0 = timeit.default_timer()
            # get the next passenger-driver match
            (startDatetime, passenger, driver) = self.getNextMatch(matchMaker, graph)

            t1 = timeit.default_timer()
            # calculate the closest vertices for the driver start, pickup, and dropoff
            driverStart = graph.closestVertexQT(driver.lat, driver.lon)
            passengerPickup = graph.closestVertexQT(passenger.slat, passenger.slon)
            passengerDropoff = graph.closestVertexQT(passenger.dlat, passenger.dlon) 
            
            t2 = timeit.default_timer()
            # calculate the time to pickup in seconds and record the datetime of pickup
            timeToPickup = graph.astar(driverStart, passengerPickup, startDatetime)
            # d = graph.getDistance(graph.vertices[driverStart].lat, 
            #                       graph.vertices[driverStart].lon, 
            #                       graph.vertices[passengerPickup].lat, 
            #                       graph.vertices[passengerPickup].lon)
            # print(timeToPickup / d / 3600)
            # timeToPickup2 = graph.astar(driverStart, passengerPickup, startDatetime)
            # print(timeToPickup - timeToPickup2)
            pickupDatetime = startDatetime + timedelta(seconds=timeToPickup)
            
            t3 = timeit.default_timer()
            # caluclate the time to dropoff in seconds and record the datetime of dropoff
            timeToDropoff = graph.astar(passengerPickup, passengerDropoff, pickupDatetime)
            dropoffDatetime = pickupDatetime + timedelta(seconds=timeToDropoff)
            
            t34 = timeit.default_timer()
            # caluclate the time to dropoff in seconds and record the datetime of dropoff
            timeToDropoff = graph.dijkstra(passengerPickup, passengerDropoff, pickupDatetime)
            
            t4 = timeit.default_timer()

            print((t4 - t34) / (t34 - t3))

            # update passenger's total wait time as time it took for driver to become active + pickup + dropoff
            waitTimeToGetActiveDriver = max(0, (driver.datetime - passenger.datetime).total_seconds())
            passenger.waitTime = waitTimeToGetActiveDriver + timeToPickup + timeToDropoff
            # update the driver's ride profit by adding (-timetoPickup + timeToDropoff)
            driver.rideProfit += timeToDropoff - timeToPickup
            # update the driver's datetime
            driver.datetime = dropoffDatetime
            # update the driver's location
            driver.lat = passenger.dlat
            driver.lon = passenger.dlon
            # update the driver's rides taken
            driver.ridesTaken += 1
            # add driver to pq only if not exiting
            if not driver.isExiting():
                matchMaker.pushPQ(driver, dropoffDatetime)
            else:
                print(driver.ridesTaken, driver.datetime - driver.startTime)
            
            t5 = timeit.default_timer()
            print("Runtime: passenger {} | match: {}, closest: {}, path1: {}, path2: {}, update: {}".format(count, 
                                                                                                    self.roundSignificantDigits(t1 - t0, 5), 
                                                                                                    self.roundSignificantDigits(t2 - t1, 5), 
                                                                                                    self.roundSignificantDigits(t3 - t2, 5), 
                                                                                                    self.roundSignificantDigits(t4 - t3, 5), 
                                                                                                    self.roundSignificantDigits(t5 - t4, 5)))
            print("Passenger wait time was {} seconds: {}s for match, {}s for pickup, {}s for dropoff".format(passenger.waitTime, waitTimeToGetActiveDriver, timeToPickup, timeToDropoff))

        waitTimes = matchMaker.getAvgWaitTime()
        rideProfits = matchMaker.getAvgRideProfit()

        with open("{} results.csv".format(self.version), "w") as f:
            write = csv.writer(f)
            write.writerow(waitTimes)
            write.writerow(rideProfits)

        print()
        print("Average total wait time for {} matched passengers: {}".format(len(waitTimes), sum(waitTimes) / len(waitTimes)))
        print("Average ride profit for drivers: {}".format(sum(rideProfits) / len(rideProfits)))


