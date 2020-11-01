import geopy.distance
from django.conf import settings
import requests

def cal_distance(cond1, cond2):
    return geopy.distance.geodesic(coords_1, coords_2).km

def get_coordinate(address):
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address,settings.API_GOOGLE_KEY))
    coordinate = response.json()
    if len(coordinate['results']) > 0:
        result = coordinate['results'][0]['geometry']['location']
        print(result['lat'], result['lng'])
        return(result['lat'], result['lng'])
    return 0
