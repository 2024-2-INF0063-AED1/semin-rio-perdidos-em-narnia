from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from queue import PriorityQueue
import random

def fetchCoordinates(postcode):
    geolocator = Nominatim(user_agent="Djikstra")
    location = geolocator.geocode(postcode)
    coordinates = (location.latitude, location.longitude)
    return coordinates

def calcDistance(a, b):
    distance = geodesic((a[0], a[1]), (b[0], b[1]))
    return distance

def calcDistanceAlt(a, b):
    distance = geodesic((a), (b))
    return distance

def readFile(filename):
    with open(filename, 'r') as file:
        for line in file:
            print((line.rstrip('\n')))

# api fetch
# print(calcDistance(fetchCoordinates("74605010"), fetchCoordinates("74690900")))

# hardcoded fetch
# print(calcDistance((-16.6747174, -49.2354413), (-16.60252115, -49.2690862)))

#readFile('file.txt')

places = [(1, '-80.713937, 57.406936'),
(2, '38.67153, 87.039646'),
(3, '2.797919, -35.300138'),
(4, '-67.529481, 39.976455'),
(5, '22.698894, 36.315485'),
(6, '60.527568, 39.530113'),
(7, '-54.230404, -21.524200'),
(8, '82.305747, 82.022292'),
(9, '-6.963851, 54.325348'),
(10, '87.370834, -65.206372')
]

i = 0
while i < len(places)-1:
    print(( (places[i][0]), (places[i+1][0]) ))
    print(calcDistanceAlt( (places[i][1]), (places[i+1][1]) ))
    i += 1
