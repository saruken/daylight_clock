import json, pygame, pytz
import update
from datetime import date, datetime, timedelta

class City():
    def __init__(self, data):
        global NOW
        global TZLOCAL
        global TZUTC

        self.name = data['name']
        self.lat = data['lat']
        self.long = data['long']
        self.lxy = tuple(data['lxy'])
        self.sunrise = datetime.strptime(data['sunrise'], '%Y-%m-%d %H:%M:%S%z')
        self.sunset = datetime.strptime(data['sunset'], '%Y-%m-%d %H:%M:%S%z')
        self.str_sunrise = datetime.strftime(self.sunrise, '%H:%M:%S')
        self.str_sunset = datetime.strftime(self.sunset, '%H:%M:%S')

        while self.sunrise.day < NOW.day:
            self.sunrise += timedelta(days=1)
        while self.sunset.day < NOW.day:
            self.sunset += timedelta(days=1)

        self.is_day = False
        self.is_selected = False

        self.light = pygame.Surface((8, 8))
        self.light.set_colorkey(TRANSPARENT_COLOR)
        light_sprite = pygame.image.load('light.bmp').convert()
        self.light.blit(light_sprite, (0, 0))

        self.select = pygame.Surface((20, 20))
        self.sxy = tuple([x - 6 for x in data['lxy']])
        self.select.set_colorkey(TRANSPARENT_COLOR)
        select_sprite = pygame.image.load('select.bmp').convert()
        self.select.blit(select_sprite, (0, 0))

    def check_sun(self):

        global NOW

        sunrise = self.sunrise
        sunset = self.sunset

        # Day / light on = True
        return sunrise < NOW < sunset or sunset < sunrise < NOW

    def update(self):

        self.is_day = self.check_sun()

        if self.is_day:
            self.light.set_alpha(255)
        else:
            self.light.set_alpha(0)

        if self.is_selected:
            self.select.set_alpha(255)
        else:
            self.select.set_alpha(0)

def main():

    global GAME_SCREEN_SIZE
    global BACKGROUND_COLOR
    global TRANSPARENT_COLOR
    global NOW
    global TZLOCAL
    global TZUTC

    TZLOCAL = pytz.timezone('US/Eastern')
    TZUTC = pytz.timezone('UTC')
    NOW = datetime.utcnow().replace(tzinfo=TZUTC).astimezone(TZLOCAL)

    game_running = True
    screen = pygame.display.set_mode(GAME_SCREEN_SIZE)

    pygame.key.set_repeat(350, 80)

    ###########################################################################
    ####   Graphics                                                       #####
    ###########################################################################

    map_sprite = pygame.image.load('map.bmp').convert()

    map_obj = pygame.Surface(GAME_SCREEN_SIZE)
    map_obj.blit(map_sprite, (0, 0))

    cities = get_city_data()

    font = pygame.font.Font("pixeled.ttf", 12)

    ###########################################################################
    ####   Main loop                                                      #####
    ###########################################################################

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    select_city(cities, -1)
                elif event.key == pygame.K_RIGHT:
                    select_city(cities, 1)
            elif event.type == pygame.QUIT:
                game_running = False

        screen.fill(BACKGROUND_COLOR)

        screen.blit(map_obj, (0, 0))

        for city in cities:
            city.update()
            screen.blit(city.light, city.lxy)
            screen.blit(city.select, city.sxy)

            if city.is_selected:
                text = f'{city.name}: rise {city.str_sunrise}; set {city.str_sunset}'
                screen.blit(font.render(text, True, (0, 0, 0)), (10, 283))

        pygame.display.update()

    ###########################################################################
    ####   Teardown                                                       #####
    ###########################################################################

    pygame.quit()

###############################################################################
####   Helper functions                                                   #####
###############################################################################

def get_city_data():

    with open('sun_times.json', 'r') as f:
        data = json.load(f)

    try:
        if datetime.strptime(data['timestamp'], '%Y-%m-%d').date() < date.today():
            data = update.load_data() 
    except TypeError:
        data = update.load_data()
    
    cities = []
    for cdata in data['cities']:
        city = City(cdata)
        cities.append(city)

    cities.sort(key=lambda x: x.long)
    cities[0].is_selected = True
    
    return cities

def select_city(cities, index):

    for i, city in enumerate(cities):
        if city.is_selected:
            city.is_selected = False
            try:
                cities[i + index].is_selected = True
            except IndexError:
                cities[0].is_selected = True
            return

if __name__ == '__main__':

    ###########################################################################
    ####   Pygame setup                                                   #####
    ###########################################################################

    global GAME_SCREEN_SIZE
    global BACKGROUND_COLOR
    global TRANSPARENT_COLOR

    GAME_SCREEN_SIZE = (480, 320)
    BACKGROUND_COLOR = (0, 0, 0)
    TRANSPARENT_COLOR = (255, 0, 255)

    pygame.init()
    pygame.display.set_caption('Daylight Clock')
    
    main()

    '''
    #TODO

    TODO Scroll/mask text if too long for textbox
    TODO Do live refresh
    TODO Figure out refresh intervals
    TODO Move backup_data into update.py
    TODO Handle error / no response from sunrise-sunset.org
    DONE Fix light positions
    DONE Integrate light visibility with day/night
    DONE Figure out font
    DONE Populate info textbox on keyboard events
    DONE Migrate sun times requests from main.py
    DONE Display sunrise/sunset times in textbox

    '''