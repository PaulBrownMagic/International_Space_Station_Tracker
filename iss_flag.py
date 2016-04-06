import requests
from geopy.geocoders import Nominatim  # pip install geopy
from time import sleep
from pygame import *
import sys
# Constants
SCREEN_WIDTH = 260
SCREEN_HEIGHT = 220
FPS = 1 / 10  # 1 frame every 10 seconds
ISS_URL = 'http://api.open-notify.org/iss-now.json'
# Setup PyGame and geolocator
init()
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = display.set_mode(size)
display.set_caption("ISS")
clock = time.Clock()
geolocator = Nominatim()
# Variables
done = False
file_name = None
# Functions
def get_long_lat():
    returned_data = requests.get(ISS_URL)
    data = returned_data.json()
    iss_position = data['iss_position']
    longitude = iss_position['longitude']
    latitude = iss_position['latitude']
    print(latitude, longitude)
    return longitude, latitude

def get_location(longitude, latitude):
    location = geolocator.reverse((latitude,longitude))
    place = location.raw
    if location.address is not None:
        country_code = place['address']['country_code']
        country = place['address']['country']
        print(country_code, country, location.address)  # Two letter (ISO) country code
        return country_code, country
    else:
        print("Out to Sea")
        return "sea", "Sea"

# Main Loop
while not done:

    for events in event.get():
        if events.type == QUIT:
            done = True
    try:
        longitude, latitude = get_long_lat()
        country_code, country = get_location(longitude, latitude)
        if file_name != "country-flags/png250px/" + country_code + ".png":
            screen.fill((35,35,45))
            file_name = "country-flags/png250px/" + country_code + ".png"
            flag = image.load(file_name)
            x_pos = (SCREEN_WIDTH - flag.get_rect().size[0])//2
            y_pos = (SCREEN_HEIGHT - flag.get_rect().size[1])//2
            screen.blit(flag, (x_pos, y_pos))
            display.set_caption("ISS - " + country )
    except:
        file_name = None
        print("Error")
        display.set_caption("ISS")
    print()

    display.update()
    clock.tick(FPS)

quit()
sys.exit()
