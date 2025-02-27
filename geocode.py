import requests
import sys

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
static_api_server = 'https://static-maps.yandex.ru/v1'
search_api_server = "https://search-maps.yandex.ru/v1/"

geocoder_api_key = 'bbf3064a-4087-43a3-bec3-622e7cb6a919'  # '8013b162-6b42-4997-9691-77b7074026e0'
static_api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13' #   '23b263bf-d98d-43ee-b024-39ccb486f492'
geosearch_api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'


# log
def request_error(response, url, exit=None):
    print("Ошибка выполнения запроса:")
    print('Сервер:', url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    print('url:', response.url)
    print('Выход:', exit)
    sys.exit(1)


# geocoder
def get_toponym(toponym_to_find):
    request_params = {
        "apikey": geocoder_api_key,
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, request_params)
    if not response:
        request_error(response, geocoder_api_server, get_toponym)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return toponym


def get_ll(toponym_to_find, mode=None):
    toponym = get_toponym(toponym_to_find)
    toponym_coodrs = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrs.split(" ")
    if mode == 'str':
        return f'{toponym_longitude},{toponym_lattitude}'
    return float(toponym_longitude), float(toponym_lattitude)


def get_spn(toponym_to_find, mode=None):
    toponym = get_toponym(toponym_to_find)
    lower_corner = list(map(lambda x: float(x), toponym['boundedBy']['Envelope']['lowerCorner'].split()))
    upper_corner = list(map(lambda x: float(x), toponym['boundedBy']['Envelope']['upperCorner'].split()))
    spn = list(map(lambda x, y: round(x - y, 4), upper_corner, lower_corner))
    if mode == 'str':
        return f'{spn[0]},{spn[1]}'
    return spn


# static
def get_map(params):
    params['apikey'] = static_api_key
    response = requests.get(static_api_server, params=params)
    if not response:
        request_error(response, static_api_server, get_map)
    return response


# geosearch
def get_org(params):
    params['apikey'] = geosearch_api_key
    response = requests.get(search_api_server, params=params)
    if not response:
        request_error(response, geosearch_api_key, get_org)
    return response
