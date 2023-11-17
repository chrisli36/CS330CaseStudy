from collections import deque
import heapq

class DriverPQ:
    def __init__(self, passengers, drivers):
        self.STARTTIME = min(drivers[0].datetime, passengers[0].datetime)
        
        self.passengers = []
        for passenger in passengers:
            wrapper = ((passenger.datetime - self.STARTTIME).total_seconds(), passenger)
            self.passengers.append(wrapper)
        self.passengers = deque(self.passengers)

        self.drivers = drivers
        self.activeDrivers = []
        for driver in self.drivers:
            wrapper = ((driver.datetime - self.STARTTIME).total_seconds(), driver)
            self.activeDrivers(wrapper)
        heapq.heapify(self.activeDrivers)
    
    def pushPQ(self, driver, newTime):
        heapq.heappush(self.activeDrivers, (newTime, driver))

    def getNextMatchT1(self):
        passenger = self.passengers.popleft()
        startTimeAndDriver = heapq.heappop(self.activeDrivers)
        return (passenger, startTimeAndDriver)

    def getNextMatchT2(self):
        passengerTime, passenger = self.passengers.popleft()
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
        