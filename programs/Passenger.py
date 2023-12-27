class Passenger:
    def __init__(self, datetime, slat, slon, dlat, dlon):
        self.datetime = datetime
        self.slat = slat
        self.slon = slon
        self.dlat = dlat
        self.dlon = dlon
        self.waitTime = 0