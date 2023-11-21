from collections import deque
import heapq
from Graph import Graph
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

    def getNextMatchT1(self): # 73, 26
        passengerDatetime, passenger = self.activePassengers.popleft()
        driverDatetime, driver = heapq.heappop(self.activeDrivers)
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

        return validDrivers

    def getNextMatchT2(self, graph): # 65, 99
        passengerDatetime, passenger = self.activePassengers.popleft()
    
        validDrivers = self.getValidDrivers(passengerDatetime, self.activeDrivers)

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
    
    def getNextMatchT3(self, graph): # 64.876, 104.148
        passengerDatetime, passenger = self.activePassengers.popleft()
        passengerPickup = graph.closestVertex(passenger.source_lat, passenger.source_lon)

        validDrivers = self.getValidDrivers(passengerDatetime, self.activeDrivers)
        
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
    
    def getNextMatchT5(self, graph):
        additionalTime = 300

        passengerDatetime, passenger = self.activePassengers.popleft()
        passenger.datetime += timedelta(seconds=additionalTime)
        passengerDatetime = passenger.datetime
        passenger.waitTime += additionalTime
        passengerPickup = graph.closestVertexQT(passenger.source_lat, passenger.source_lon)
        validDrivers = self.getValidDrivers(passengerDatetime, self.activeDrivers)
        
        driverDatetime, driver = validDrivers[0]
        driverStart = graph.closestVertexQT(driver.latitude, driver.longitude)
        minTime = graph.dijkstra(passengerPickup, driverStart, max(driver.datetime, passengerDatetime))
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
        totalWaitTime = 0; count = 0
        for passenger in self.passengers:
            if passenger.waitTime > 0:
                totalWaitTime += passenger.waitTime
                count += 1
        return totalWaitTime / count

    def getAvgRideProfit(self):
        totalRideProfit = 0; count = 0
        for driver in self.drivers:
            if driver.rideProfit != 0:
                totalRideProfit += driver.rideProfit
                count += 1
        return totalRideProfit / count

        