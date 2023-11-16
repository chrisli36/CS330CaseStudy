class Driver:
    def __init__(self, datetime, latitude, longitude):
        self.datetime = datetime
        self.latitude = latitude
        self.longitude = longitude
        self.timeActive = 0

    def isExiting(self):
        return self.timeActive >= 28800