from django.conf import settings
from app.models import Restaurant, District, MenuItem, Address
import requests
import re
import geopy.distance
from math import sin, cos, sqrt, atan2, radians

R = 6373.0

def get_address_func(address):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, settings.API_GOOGLE_KEY))
    coordinate = response.json()
    if len(coordinate['results']) > 0:
        result = coordinate['results'][0]['geometry']['location']
        print(result['lat'], result['lng'])
        return(result['lat'], result['lng'], coordinate['results'][0]['formatted_address'],coordinate['results'][0]['address_components'])
    return 0

def checkInOneTradeMark(list_shop):
    if len(list_shop) == 0:
        return False
    isInOne = True
    trademark = list_shop[0].trademark
    if trademark is None and len(list_shop) > 1:
        return False
    for shop in list_shop:
        if shop.trademark != trademark:
            isInOne = False
    return isInOne

def getTimeOpenInTradeMark(list_shop, isInTradeMark):
    res = {}
    for shop in list_shop:
        split_name = shop.name.split('-')
        if shop.time_open in res:
            res[shop.time_open].append(split_name[-1])
        else:
            res[shop.time_open] = [split_name[-1]]
    return res

def getShopWithName(shop_name):
    if shop_name is None:
        return []
    else:
        return Restaurant.objects.filter(name__icontains=shop_name)

def getTimeOfShop(shop_name):
    if shop_name is None:
        return []
    return []

def getCountWithTradeMark(trademark):
    if trademark is None:
        return 0
    return Restaurant.objects.filter(trademark=trademark).count()
        
def getMenuOfRestaurant(restaurant):
    if restaurant is None:
        return None
    print(restaurant)
    return MenuItem.objects.filter(restaurant__name=restaurant)

def getLocationOfShop(shop_name, location):
    if location is None:
        return Address.objects.filter(restaurant__name__icontains=shop_name)
    return Address.objects.filter(restaurant__name__icontains=shop_name, address_full__icontains = location)

def getShopWithInfo(shop_name=None, shop_type=None, location=None, time=None):
    if location is not None:
        info_address = get_address_func(location + ' Hà Nội')
        print(info_address)
    else:
        info_address = None
    
    result = Address.objects.filter(town='Bách Khoa') | Address.objects.filter(district__district__icontains='Hai Bà Trưng')
    for item in result:
        item.distance = calculateDistance(21.0042694, 105.8459098, item.location_lat,item.location_lng)
    result2 = result.order_by('-distance')
    for item in result2:
        print(item.distance)

def calculateDistance(lat1, lon1, lat2, lon2):

    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    print(coords_1, coords_2)
    return geopy.distance.geodesic(coords_1, coords_2).km