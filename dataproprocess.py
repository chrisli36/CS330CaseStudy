import csv
from datetime import datetime 

def processPassengers(fileName):
    passengers = []
    with open(fileName, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            passengers.append({
                'datetime': datetime.strptime(row['Date/Time'], '%m/%d/%Y %H:%M:%S'),
                'source_lat': float(row['Source Lat']),
                'source_lon': float(row['Source Lon']),
                'dest_lat': float(row['Dest Lat']),
                'dest_lon': float(row['Dest Lon'])
            })
    return passengers



print(processPassengers('passengers.csv')[1])