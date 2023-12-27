class Driver:
    def __init__(self, datetime, lat, lon):
        self.datetime = datetime
        self.startTime = datetime
        self.lat = lat
        self.lon = lon
        self.rideProfit = 0
        self.ridesTaken = 0

    def isExiting(self):
        return (self.datetime - self.startTime).total_seconds() >= 21600 and self.ridesTaken > 4
    
    def __lt__(self, other):
        return self.datetime < other.datetime