from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from queue import PriorityQueue
import itertools

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

places = [('A', '-80.713937, 57.406936'),
('B', '38.67153, 87.039646'),
('C', '2.797919, -35.300138'),
('D', '-67.529481, 39.976455'),
('E', '22.698894, 36.315485'),
]

permutations = itertools.permutations(places, 2)
for places in permutations:
    print("\ncaminho: ", places[0][0], places[1][0])
    print(calcDistanceAlt (places[0][1], places[1][1]) )
