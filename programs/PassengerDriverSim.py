from collections import deque
import heapq
from datetime import datetime, timedelta

class PassengerDriverSim:
    def __init__(self, passengers, drivers):

        self.passengers = passengers
        self.activePassengers = []
        for passenger in self.passengers:
            wrapper = (passenger.datetime, passenger)
            self.activePassengers.append(wrapper)
        self.activePassengers = deque(self.activePassengers)

        self.drivers = drivers
        self.activeDrivers = []
        for driver in self.drivers:
            wrapper = (driver.datetime, driver)
            self.activeDrivers.append(wrapper)
        heapq.heapify(self.activeDrivers)

    def hasPassengers(self):
        return len(self.activePassengers) > 0
                   
    def pushPQ(self, driver, newTime):
        heapq.heappush(self.activeDrivers, (newTime, driver))

    def getNextMatchT1(self):
        # get next passenger off the queue
        passengerDatetime, passenger = self.activePassengers.popleft()
        # match the earliest driver with the passenger
        driverDatetime, driver = heapq.heappop(self.activeDrivers)
        print("\tFound 1 valid driver(s)")
        return (max(passengerDatetime, driverDatetime), passenger, driver)
    
    def getValidDrivers(self, passengerDatetime, activeDrivers):
        driverDatetime, driver = (datetime.min, None)
        validDrivers = []
        while driverDatetime <= passengerDatetime and activeDrivers:
            driverDatetime, driver = heapq.heappop(activeDrivers)
            validDrivers.append((driverDatetime, driver))

        if len(validDrivers) > 1:
            heapq.heappush(activeDrivers, validDrivers[-1])
            validDrivers.pop()

        print("\tFound {} valid driver(s)".format(len(validDrivers)))
        return validDrivers

    def getNextMatchT2(self, graph): # 1665.5, 1933
        # get next passenger off the queue
        passengerDatetime, passenger = self.activePassengers.popleft()
    
        # pop off the list of drivers who were available before the passenger requested a ride
        validDrivers = self.getValidDrivers(passengerDatetime, self.activeDrivers)

        # push the drivers back onto the priority queue except for the closest driver by straight-line distance
        driverDatetime, driver = validDrivers[0]
        minDistance = graph.getDistance(passenger.source_lat, passenger.source_lon, driver.latitude, driver.longitude)
        minDriverWrapper = (driverDatetime, driver)
        for driverDatetime, driver in validDrivers[1:]:
            distance = graph.getDistance(passenger.source_lat, passenger.source_lon, driver.latitude, driver.longitude)
            if distance < minDistance:
                heapq.heappush(self.activeDrivers, minDriverWrapper)
                minDriverWrapper = (driverDatetime, driver)
                minDistance = distance
            else:
                heapq.heappush(self.activeDrivers, (driverDatetime, driver))
        
        return (max(passengerDatetime, minDriverWrapper[0]), passenger, minDriverWrapper[1])
    
    def getNextMatchT3(self, graph): # 2174, 1080
        # get next passenger off the queue
        passengerDatetime, passenger = self.activePassengers.popleft()
        passengerPickup = graph.closestVertex(passenger.source_lat, passenger.source_lon)

        # pop off the list of drivers who were available before the passenger requested a ride
        validDrivers = self.getValidDrivers(passengerDatetime, self.activeDrivers)

        # push the drivers back onto the priority queue except for the closest driver by ETA
        driverDatetime, driver = validDrivers[0]
        driverStart = graph.closestVertex(driver.latitude, driver.longitude)
        minTime = graph.dijkstra(passengerPickup, driverStart, max(driver.datetime, passengerDatetime))
        minDriverWrapper = (driverDatetime, driver)
        for driverDatetime, driver in validDrivers[1:]:
            driverStart = graph.closestVertex(driver.latitude, driver.longitude)
            time = graph.dijkstra(passengerPickup, driverStart, max(driver.datetime, passengerDatetime))
            if time < minTime:
                heapq.heappush(self.activeDrivers, minDriverWrapper)
                minDriverWrapper = (driverDatetime, driver)
                minTime = time
            else:
                heapq.heappush(self.activeDrivers, (driverDatetime, driver))
        
        return (max(passengerDatetime, minDriverWrapper[0]), passenger, minDriverWrapper[1])
    
    def getNextMatchT4(self, graph):
        # get next passenger off the queue
        passengerDatetime, passenger = self.activePassengers.popleft()
        passengerPickup = graph.closestVertexQT(passenger.source_lat, passenger.source_lon)

        # pop off the list of drivers who were available before the passenger requested a ride
        validDrivers = self.getValidDrivers(passengerDatetime, self.activeDrivers)

        # push the drivers back onto the priority queue except for the closest driver by ETA
        driverDatetime, driver = validDrivers[0]
        driverStart = graph.closestVertexQT(driver.latitude, driver.longitude)
        minTime = graph.astar(passengerPickup, driverStart, max(driver.datetime, passengerDatetime))
        minDriverWrapper = (driverDatetime, driver)
        for driverDatetime, driver in validDrivers[1:]:
            driverStart = graph.closestVertexQT(driver.latitude, driver.longitude)
            time = graph.astar(passengerPickup, driverStart, max(driver.datetime, passengerDatetime))
            if time < minTime:
                heapq.heappush(self.activeDrivers, minDriverWrapper)
                minDriverWrapper = (driverDatetime, driver)
                minTime = time
            else:
                heapq.heappush(self.activeDrivers, (driverDatetime, driver))
        
        return (max(passengerDatetime, minDriverWrapper[0]), passenger, minDriverWrapper[1])
    
    def getNextMatchT5(self, graph): # 1488.33, 2131.128
        # get next passenger off the queue
        passengerDatetime, passenger = self.activePassengers.popleft()
        passengerPickup = graph.closestVertexQT(passenger.source_lat, passenger.source_lon)

        # make the passenger wait "additionalTime" before matching
        additionalTime = 300
        passenger.datetime += timedelta(seconds=additionalTime)
        passengerDatetime = passenger.datetime
        passenger.waitTime += additionalTime

        # pop off the list of drivers who were available before the passenger requested a ride
        validDrivers = self.getValidDrivers(passengerDatetime, self.activeDrivers)
        
        # push the drivers back onto the priority queue except for the closest driver by ETA
        driverDatetime, driver = validDrivers[0]
        driverStart = graph.closestVertexQT(driver.latitude, driver.longitude)
        minTime = graph.astar(passengerPickup, driverStart, max(driver.datetime, passengerDatetime))
        minDriverWrapper = (driverDatetime, driver)
        for driverDatetime, driver in validDrivers[1:]:
            driverStart = graph.closestVertexQT(driver.latitude, driver.longitude)
            time = graph.dijkstra(passengerPickup, driverStart, max(driver.datetime, passengerDatetime))
            if time < minTime:
                heapq.heappush(self.activeDrivers, minDriverWrapper)
                minDriverWrapper = (driverDatetime, driver)
                minTime = time
            else:
                heapq.heappush(self.activeDrivers, (driverDatetime, driver))
        
        return (max(passengerDatetime, minDriverWrapper[0]), passenger, minDriverWrapper[1])

    def getAvgWaitTime(self):
        waitTimes = []
        for passenger in self.passengers:
            if passenger.waitTime > 0:
                waitTimes.append(passenger.waitTime)
        return waitTimes

    def getAvgRideProfit(self):
        rideProfits = []
        for driver in self.drivers:
            if driver.rideProfit != 0:
                rideProfits.append(driver.rideProfit)
        return rideProfits

        