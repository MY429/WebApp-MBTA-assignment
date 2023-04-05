# Your API KEYS (you need to use your own keys - very long random characters)


import urllib.request
import json
from pprint import pprint

MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MAPBOX_TOKEN = 'pk.eyJ1IjoicGxpbjMiLCJhIjoiY2xnMno5cGgzMDJ0ODNocHB1ODh1YjJ2dCJ9.KNUL4cTNYef4sVjHrJt0Dw'
# query = 'Babson%20College'
# url=f'{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi'

# Useful URLs (you need to add the appropriate parameters for your requests)
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"
MBTA_KEY = "107766d5a96d4445b66abc6089caba49"


# A little bit of scaffolding if you want to use it


def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    url=f'{MAPBOX_BASE_URL}/{place_name}.json?access_token={MAPBOX_TOKEN}&types=poi'
    responses_data = get_json(url)
    return [responses_data["features"][0]["center"][1],responses_data["features"][0]["center"][0]]




def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    
    MBTA_URL = f"https://api-v3.mbta.com/stops?api_key={MBTA_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"
    
    responses_data =get_json(MBTA_URL)

    return (responses_data['data'][0]["attributes"]['name'], responses_data['data'][0]["attributes"]['wheelchair_boarding'])



def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    latitude, longitude = get_lat_long(place_name)

    return get_nearest_station(latitude, longitude)


def main():
    """
    You can test all the functions here
    """
    
    print(find_stop_near("brookline"))



if __name__ == '__main__':
    main()
