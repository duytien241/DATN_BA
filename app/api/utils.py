from django.conf import settings
from app.models import Address, District
import requests
import re

def get_address_func():
	i = 0
	list_address = Address.objects.all()
	for address in list_address:
		if address.district is None:
			i = i + 1
			response = requests.get(
				'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address.address_full, settings.API_GOOGLE_KEY))
			coordinate = response.json()
			print(address.address_full)
			if len(coordinate['results']) > 0:
				result = coordinate['results'][0]['geometry']['location']
				address.location_lat = result['lat']
				address.location_lng = result['lng']
				address_components = coordinate['results'][0]['address_components']
				formatted_address = coordinate['results'][0]['formatted_address']
				arr_address = formatted_address.split(',')
				if len(arr_address) == 5:
					address.street_number = arr_address[0].strip()
					address.town = arr_address[-4].strip()
				else:
					street_number = ''
					for type in address_components:
						if 'street_number' in type['types']:
							street_number = type['long_name']
						if 'route' in type['types']:
							address.town = type['long_name']
							street_number = street_number + ' ' + type['long_name']
						address.street_number = street_number
				print(arr_address)
				try:
					for type in address_components:
						if 'administrative_area_level_2' in type['types']:
							if formatted_address.find('Từ Liêm') != -1:
								if address.address_full.find('Nam Từ Liêm'):
									district_obj = District.objects.get(
										district__icontains='Nam Từ Liêm')
								else:
									district_obj = District.objects.get(
										district__icontains='Bắc Từ Liêm')
							else:
								if type['long_name'] == 'Bac Tu Liem':
									district_obj = District.objects.get(
										district__icontains='Bắc Từ Liêm')
								else:
									district_obj = District.objects.get(district__icontains=type['long_name'])
							address.district = district_obj
					address.save()
				except:
					pass
		if i==3000:
			break


def no_accent_vietnamese(s):
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(r'[Đ]', 'D', s)
    s = re.sub(r'[đ]', 'd', s)
    return s
