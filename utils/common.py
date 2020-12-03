from django.conf import settings
from app.models import Restaurant, District, MenuItem, Address
import requests
import re
import json
import geopy.distance
from math import sin, cos, sqrt, atan2, radians

R = 6373.0

list_shop_type = []
with open('resources/shop_type.txt', 'r', encoding='utf8') as f:
    for line in f:
        list_shop_type.append(line.lower().strip())
    f.close()

def get_address_func(address):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}&language=vi&region=VN'.format(address, settings.API_GOOGLE_KEY))
    coordinate = response.json()
    if len(coordinate['results']) > 0:
        result = coordinate['results'][0]['geometry']['location']
        return[result['lat'], result['lng'], coordinate['results'][0]['formatted_address'],coordinate['results'][0]['address_components']]
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

def getTimeOpenInTradeMark(pre_query, isInTradeMark):
    res = {}
    for item in pre_query:
        split_name = item['restaurant']['name'].split('-')
        if json.dumps(item['restaurant']['time_open']) in res:
            res[json.dumps(item['restaurant']['time_open'])].append(split_name[-1])
        else:
            res[json.dumps(item['restaurant']['time_open'])] = [split_name[-1]]
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

def getInfoLocation(location):
    if location in ['gần đây', 'đây']:
        info_address = get_address_func('Lê Thanh Nghị Hà Nội')
    else:
        info_address = get_address_func(location + ' Hà Nội')
    address_components = info_address[3]
    administrative_area_level_2 = ''
    for type in address_components:
        if 'administrative_area_level_2' in type['types']:
            administrative_area_level_2 = type['long_name']
    return (administrative_area_level_2,info_address[0], info_address[1] )

def getShopWithLocation(shop_name, location):
    shop_name = str(shop_name).replace("quán ","")
    if location is None:
        return Address.objects.filter(restaurant__name__icontains=shop_name.title())
    else:
        res_one = Address.objects.filter(restaurant__name__icontains=shop_name, address_full__icontains = location.title())
        if len(res_one) !=0:
            return res_one
        info_address = getInfoLocation(location)
        shop_name = str(shop_name).replace(str(location),"")
        return Address.objects.filter(restaurant__name__icontains=shop_name, district__district__icontains = info_address[0])
 
def getLocationOfShop(shop_name, location):
    print(shop_name)
    if shop_name is None:
        return []
    if location is None:
        return Address.objects.filter(restaurant__name__icontains=shop_name)
    else:
        return Address.objects.filter(restaurant__name__icontains=shop_name, address_full__icontains = location)

def getShopWithInfo(shop_name=None, shop_type=None, location=None, time=None):
    if location is not None:
        info_address = getInfoLocation(location)
    else:
        info_address = None
    res = {}
    arr_distance = []
    if shop_type is not None:
        shop_type_cv = converShopType(shop_type)
        if shop_type_cv in list_shop_type:
            if info_address is not None:
                result = Address.objects.filter(district__district__icontains=info_address[0], restaurant__category_type__name__icontains=shop_type_cv)
            else:
                result = Address.objects.filter(restaurant__category_type__name__icontains=shop_type_cv)
        else:
            if info_address is not None:
                result = Address.objects.filter(district__district__icontains=info_address[0], restaurant__name__icontains=shop_type)
            else:
                result = Address.objects.filter(restaurant__name__icontains=shop_type)
    else:
        if info_address is not None:
            result = Address.objects.filter(district__district__icontains=info_address[0])
        else:
            result = Address.objects.all()
    if info_address is not None:
        for item in result:
            tmp = calculateDistance(info_address[1], info_address[2], item.location_lat,item.location_lng)
            if(len(arr_distance) < 5 and tmp not in arr_distance):
                arr_distance.append(tmp)
                res[tmp] = item
            elif max(arr_distance) > tmp and tmp not in arr_distance:
                v_max = max(arr_distance)
                arr_distance.remove(v_max)
                del res[v_max]
                arr_distance.append(tmp)
                res[tmp] = item
    else:
        for item in result:
            res[item.name] = item
    return res

def getYNShopTime(name, list_time, is_trademark, pre_query):
    if list_time is not None:
        return ''
    res = {}
    response = ''
    for item in pre_query:
        for time in list_time:
            time_end = 12
            if time in ['tối', 'buổi tối']:
                time_end = 20
            elif time in ['sáng', 'buổi sáng', 'ban ngày']:
                time_end = 8
            elif time in ['đêm', 'ban đêm']:
                time_end = 24
            elif time in ['trưa', 'buổi trưa']:
                time_end = 12
            isOpen = False
            time_open = item['restaurant']['time_open']
            if time_open['has_two_shift']:
                time_1 = time_open['shift_one_start']
                time_2 = time_open['shift_one_end']
                time_3 = time_open['shift_two_start']
                time_4 = time_open['shift_two_end']
                range_1 = int(str(time_1).split(":")[0])*60 + int(str(time_1).split(":")[1])
                range_2 = int(str(time_2).split(":")[0])*60 + int(str(time_2).split(":")[1])
                range_3 = int(str(time_3).split(":")[0])*60 + int(str(time_3).split(":")[1])
                range_4 = int(str(time_4).split(":")[0])*60 + int(str(time_4).split(":")[1])
                if time_end * 60 in range(range_1,range_2) or time_end * 60 in range(range_3,range_4):
                    isOpen = True
            else:
                time_1 = time_open['shift_one_start']
                time_2 = time_open['shift_one_end']
                range_1 = int(str(time_1).split(":")[0])*60 + int(str(time_1).split(":")[1])
                range_2 = int(str(time_2).split(":")[0])*60 + int(str(time_2).split(":")[1])
                if time_end * 60 in range(range_1,range_2):
                    isOpen = True
            if item['restaurant']['name'] in res:
                res[item['restaurant']['name']][time] = isOpen
            else:
                res[item['restaurant']['name']] = {}
                res[item['restaurant']['name']][time] = isOpen
        # if isOpen:
            # response = response + "Quán {} có mở cửa {} từ {} đến {} \n".format(item['restaurant']['name'], time,time_open['shift_one_start'],time_open['shift_one_end'])
        # else:
            # response = response + "Quán {} không mở cửa {} mà chỉ mở từ {} đến {} \n".format(item['restaurant']['name'], time,time_open['shift_one_start'],time_open['shift_one_end'])
    for item in res:
        print(res[item])
        response = response + item
        for time in res[item]:
            print(time)
            if time:
                response = response + " có mở cửa {} ".format(time)
            else:
                response = response + " không mở cửa {} ".format(time)
    return response

def calculateFeeShip():
    distance = calculateDistance()

def calculateDistance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geopy.distance.geodesic(coords_1, coords_2).km

def converShopType(shop_type):
    if shop_type in ['ăn vặt', 'vỉa hè']:
        return 'ăn vặt/vỉa hè'
    if shop_type in ['bia', 'nhậu', 'quán nhậu']:
        return 'quán nhậu'
    return shop_type