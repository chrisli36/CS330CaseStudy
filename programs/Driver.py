class Driver:
    def __init__(self, datetime, latitude, longitude):
        self.datetime = datetime
        self.startTime = datetime
        self.latitude = latitude
        self.longitude = longitude
        self.rideProfit = 0
        self.ridesTaken = 0

    def isExiting(self):
        return (self.datetime - self.startTime).total_seconds() >= 14400 and self.ridesTaken > 4
    
    def __lt__(self, other):
        return self.datetime < other.datetime