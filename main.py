from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def fetchCoordinates(postcode):
    geolocator = Nominatim(user_agent="Djikstra")
    location = geolocator.geocode(postcode)
    coordinates = (location.latitude, location.longitude)
    return coordinates

def calcDistance(a, b):
    distance = geodesic((a[0], a[1]), (b[0], b[1]))
    return distance

# api fetch
# print(calcDistance(fetchCoordinates("00000000"), fetchCoordinates("00000000")))
