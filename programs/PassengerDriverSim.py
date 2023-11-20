from collections import deque
import heapq
from Graph import Graph
from datetime import datetime

class PassengerDriverSim:
    def __init__(self, passengers, drivers):
        # self.STARTTIME = min(drivers[0].datetime, passengers[0].datetime)
        
        self.passengers = passengers
        self.activePassengers = []
        for passenger in self.passengers:
            # wrapper = ((passenger.datetime - self.STARTTIME).total_seconds(), passenger)
            wrapper = (passenger.datetime, passenger)
            self.activePassengers.append(wrapper)
        self.activePassengers = deque(self.activePassengers)

        self.drivers = drivers
        self.activeDrivers = []
        for driver in self.drivers:
            # wrapper = ((driver.datetime - self.STARTTIME).total_seconds(), driver)
            wrapper = (driver.datetime, driver)
            self.activeDrivers.append(wrapper)
        heapq.heapify(self.activeDrivers)

    def hasPassengers(self):
        return len(self.activePassengers) > 0
                   
    def pushPQ(self, driver, newTime):
        heapq.heappush(self.activeDrivers, (newTime, driver))

    def getNextMatchT1(self): #1510, 710
        passengerDatetime, passenger = self.activePassengers.popleft()
        driverDatetime, driver = heapq.heappop(self.activeDrivers)
        return (max(passengerDatetime, driverDatetime), passenger, driver)
    
    def getNextMatchT2(self, graph):
        passengerDatetime, passenger = self.activePassengers.popleft()
        
        driverDatetime, driver = (datetime.min, None)
        validDrivers = []
        while driverDatetime <= passengerDatetime and self.activeDrivers:
            driverDatetime, driver = heapq.heappop(self.activeDrivers)
            validDrivers.append((driverDatetime, driver))
        
        driverDatetime, driver = validDrivers[0]
        minDistance = graph.getDistance(passenger.source_lat, passenger.source_lon, driver.latitude, driver.longitude)
        minDriverWrapper = (driverDatetime, driver)
        for driverDatetime, driver in validDrivers[1:]:
            distance = minDistance = graph.getDistance(passenger.source_lat, passenger.source_lon, driver.latitude, driver.longitude)
            if distance < minDistance:
                heapq.heappush(self.activeDrivers, minDriverWrapper)
                minDriverWrapper = (driverDatetime, driver)
            else:
                heapq.heappush(self.activeDrivers, (driverDatetime, driver))
        
        return (max(passengerDatetime, minDriverWrapper[0]), passenger, minDriverWrapper[1])
    
    # def getNextMatchT3(self, graph):
    #     passengerTime, passenger = self.activePassengers.popleft()
    #     passengerPickup = graph.closestVertexQT(passenger.source_lat, passenger.source_lon)

    #     driverTime, driver = (None, None)
    #     validDrivers = []
    #     while driverTime <= passengerTime and self.activeDrivers:
    #         driverTime, driver = heapq.heappop(self.activeDrivers)
    #         validDrivers.append((driverTime, driver))
        
    #     driverTime, driver = validDrivers[0]
    #     driverStart = graph.closestVertexQT(driver.latitude, driver.longitude)
    #     minDistance = graph.dijkstra(passengerPickup, driverStart, driver.datetime)
    #     minDriverWrapper = (driverTime, driver)
    #     for driverTime, driver in validDrivers[1:]:
    #         driverStart = graph.closestVertexQT(driver.latitude, driver.longitude)
    #         distance = graph.dijkstra(passengerPickup, driverStart, dayType, hour)
    #         if distance < minDistance:
    #             heapq.heappush(self.activeDrivers, minDriverWrapper)
    #             minDriverWrapper = (driverTime, driver)
    #         else:
    #             heapq.heappush(self.activeDrivers, (driverTime, driver))
        
    #     return (passenger, minDriverWrapper)
    
    def getAvgWaitTime(self):
        totalWaitTime = 0
        for passenger in self.passengers:
            totalWaitTime += passenger.waitTime
        return totalWaitTime / len(self.passengers)

    def getAvgRideProfit(self):
        totalRideProfit = 0
        for driver in self.drivers:
            totalRideProfit += driver.rideProfit
        return totalRideProfit / len(self.drivers)

        