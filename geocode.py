import requests
import sys
from apikeys import GEOCODER_API_KEY, GEOSEARCH_API_KEY, STATIC_API_KEY

EXIT_PROGRAM_ON_ERROR = False
PRINT_DEBUG = True

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
static_api_server = 'https://static-maps.yandex.ru/v1'
search_api_server = "https://search-maps.yandex.ru/v1/"


# log
def request_error(response, url, exit=None):
    if PRINT_DEBUG:
        print("Ошибка выполнения запроса:")
        print('Сервер:', url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        print('url:', response.url)
        print('Выход:', exit)
    if EXIT_PROGRAM_ON_ERROR:
        sys.exit(1)


# geocoder
def get_toponym(toponym_to_find):
    request_params = {
        "apikey": GEOCODER_API_KEY,
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
    spn = min(list(map(lambda x, y: round(x - y, 4), upper_corner, lower_corner)))
    if mode == 'str':
        return f'{spn},{spn}'
    return spn


def get_address(toponym_to_find):
    toponym = get_toponym(toponym_to_find)
    address = toponym['metaDataProperty']['GeocoderMetaData']['text']
    return address


# static
def get_map(params):
    params['apikey'] = STATIC_API_KEY
    response = requests.get(static_api_server, params=params)
    if not response:
        request_error(response, static_api_server, get_map)
    return response


# geosearch
def get_org(params):
    params['apikey'] = GEOSEARCH_API_KEY
    response = requests.get(search_api_server, params=params)
    if not response:
        request_error(response, GEOSEARCH_API_KEY, get_org)
    return response
