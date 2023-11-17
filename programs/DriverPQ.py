from collections import deque
import heapq

class DriverPQ:
    def __init__(self, passengers, drivers):
        self.STARTTIME = min(drivers[0].datetime, passengers[0].datetime)
        
        self.passengers = passengers
        self.activePassengers = []
        for passenger in self.passengers:
            wrapper = ((passenger.datetime - self.STARTTIME).total_seconds(), passenger)
            self.activePassengers.append(wrapper)
        self.activePassengers = deque(self.activePassengers)

        self.drivers = drivers
        self.activeDrivers = []
        for driver in self.drivers:
            wrapper = ((driver.datetime - self.STARTTIME).total_seconds(), driver)
            self.activeDrivers.append(wrapper)
        heapq.heapify(self.activeDrivers)

    def hasPassengers(self):
        return len(self.activePassengers) > 0
                   
    def pushPQ(self, driver, newTime):
        heapq.heappush(self.activeDrivers, (newTime, driver))

    def getNextMatchT1(self):
        _, passenger = self.activePassengers.popleft()
        startTimeAndDriver = heapq.heappop(self.activeDrivers)
        return (passenger, startTimeAndDriver)

    def getNextMatchT2(self):
        passengerTime, passenger = self.activePassengers.popleft()
        i = 0
        while self.activeDrivers[i][0] <= passengerTime and i < len(self.activeDrivers):
            i += 1
        
        if i == 0:
            startTimeAndDriver = heapq.heappop(self.activeDrivers)
            return (passenger, startTimeAndDriver)
        
        minDistance = float('inf'); minJ = None
        for j, driverWrapper in enumerate(self.activeDrivers[:i]):
            if driverWrapper[1] < minDistance:
                minDriverWrapper = driverWrapper
                minJ = j
        self.activeDrivers[minJ] = self.activeDrivers[-1]
        self.activeDrivers.pop()
        heapq.heapify(self.activeDrivers)
        
        return (passenger, minDriverWrapper)
    
    def getNextMatchT3(self):
        pass
    
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

        