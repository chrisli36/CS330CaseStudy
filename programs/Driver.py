class Driver:
    def __init__(self, datetime, latitude, longitude):
        self.datetime = datetime
        self.startTime = datetime
        self.latitude = latitude
        self.longitude = longitude
        self.rideProfit = 0

    def isExiting(self):
        return (self.datetime - self.startTime).total_seconds() >= 28800
    
    def __lt__(self, other):
        return self.datetime < other.datetime