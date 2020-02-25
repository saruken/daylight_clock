import json, os, pytz, requests
from datetime import date, datetime, timedelta
from pathlib import Path

def generate_city_info():
    return [
        {
            'name': 'Algiers',
            'lat': 36.7538,
            'long': 3.0588,
            'lxy': [222, 134]
        },
        {
            'name': 'Anchorage',
            'lat': 61.21666667,
            'long': -149.9,
            'lxy': [38, 86]
        },
        {
            'name': 'Auckland',
            'lat': -36.8485,
            'long': 174.7633,
            'lxy': [432, 210]
        },
        {
            'name': 'Azores',
            'lat': 38.458,
            'long': -28.3228,
            'lxy': [186, 118]
        },
        {
            'name': 'Baghdad',
            'lat': 33.3152,
            'long': 44.3661,
            'lxy': [282, 138]
        },
        {
            'name': 'Bangkok',
            'lat': 13.7563,
            'long': 100.5018,
            'lxy': [342, 154]
        },
        {
            'name': 'Berlin',
            'lat': 52.52,
            'long': 13.405,
            'lxy': [234, 100]
        },
        {
            'name': 'Buenos Aires',
            'lat': -34.60333333,
            'long': -58.38166667,
            'lxy': [150, 216]
        },
        {
            'name': 'Cairo',
            'lat': 30.0444,
            'long': 31.2357,
            'lxy': [258, 140]
        },
        {
            'name': 'Calcutta',
            'lat': 22.5726,
            'long': 88.3639,
            'lxy': [320, 148]
        },
        {
            'name': 'Cape Town',
            'lat': -33.9249,
            'long': 18.4241,
            'lxy': [246, 208]
        },
        {
            'name': 'Casablanca',
            'lat': 33.5731,
            'long': -7.5898,
            'lxy': [206, 136]
        },
        {
            'name': 'Chicago',
            'lat': 41.88194444,
            'long': -87.62777778,
            'lxy': [108, 116]
        },
        {
            'name': 'Dawson',
            'lat': 64.06,
            'long': -129.57472222,
            'lxy': [56, 78]
        },
        {
            'name': 'Denver',
            'lat': 39.73916667,
            'long': -104.99027778,
            'lxy': [86, 118]
        },
        {
            'name': 'Dutch Harbor',
            'lat': 53.90277778,
            'long': -166.51833333,
            'lxy': [16, 100]
        },
        {
            'name': 'Gander',
            'lat': 48.95694444,
            'long': -54.60888889,
            'lxy': [146, 102]
        },
        {
            'name': 'Godthaab (Nuuk)',
            'lat': 64.18138889,
            'long': -51.69416667,
            'lxy': [156, 76]
        },
        {
            'name': 'Gorki',
            'lat': 55.5080,
            'long': 37.7775,
            'lxy': [278, 84]
        },
        {
            'name': 'Hong Kong',
            'lat': 22.3193,
            'long': 114.1694,
            'lxy': [358, 138]
        },
        {
            'name': 'Honolulu',
            'lat': 21.30694444,
            'long': -157.85833333,
            'lxy': [30, 148]
        },
        {
            'name': 'Karachi',
            'lat': 24.8607,
            'long': 67.0011,
            'lxy': [300, 140]
        },
        {
            'name': 'Leningrad (St. Petersburg)',
            'lat': 59.9343,
            'long': 30.3351,
            'lxy': [252, 84]
        },
        {
            'name': 'Lima',
            'lat': -12.05,
            'long': -77.03333333,
            'lxy': [128, 188]
        },
        {
            'name': 'Lisbon',
            'lat': 38.7223,
            'long': -9.1393,
            'lxy': [206, 124]
        },
        {
            'name': 'London',
            'lat': 51.5074,
            'long': -0.1278,
            'lxy': [214, 100]
        },
        {
            'name': 'Los Angeles',
            'lat': 34.05,
            'long': -118.25,
            'lxy': [70, 130]
        },
        {
            'name': 'Madrid',
            'lat': 40.4168,
            'long': -3.7038,
            'lxy': [214, 122]
        },
        {
            'name': 'Manila',
            'lat': 14.5995,
            'long': 120.9842,
            'lxy': [366, 154]
        },
        {
            'name': 'Mexico City',
            'lat': 19.43333333,
            'long': -99.13333333,
            'lxy': [98, 148]
        },
        {
            'name': 'Moscow',
            'lat': 55.7558,
            'long': 37.6173,
            'lxy': [264, 88]
        },
        {
            'name': 'New York',
            'lat': 40.66111111,
            'long': -73.94388889,
            'lxy': [128, 118]
        },
        {
            'name': 'Oslo',
            'lat': 59.9139,
            'long': 10.7522,
            'lxy': [232, 86]
        },
        {
            'name': 'Ottawa',
            'lat': 45.42472222,
            'long': -75.695,
            'lxy': [124, 108]
        },
        {
            'name': 'Panama',
            'lat': 8.96666667,
            'long': -79.53333333,
            'lxy': [124, 166]
        },
        {
            'name': 'Paris',
            'lat': 48.8566,
            'long': 2.3522,
            'lxy': [222, 110]
        },
        {
            'name': 'Peking (Beijing)',
            'lat': 39.9042,
            'long': 116.4074,
            'lxy': [366, 114]
        },
        {
            'name': 'Reykjavik',
            'lat': 64.1466,
            'long': -21.9426,
            'lxy': [188, 72]
        },
        {
            'name': 'Rio de Janeiro',
            'lat': -22.90833333,
            'long': -43.19638889,
            'lxy': [170, 196]
        },
        {
            'name': 'Rome',
            'lat': 41.9028,
            'long': 12.4964,
            'lxy': [236, 122]
        },
        {
            'name': 'San Francisco',
            'lat': 37.77750000,
            'long': -122.41638889,
            'lxy': [66, 122]
        },
        {
            'name': 'San Juan',
            'lat': 18.40638889,
            'long': -66.06388889,
            'lxy': [146, 150]
        },
        {
            'name': 'Santiago',
            'lat': -33.45,
            'long': -70.66666667,
            'lxy': [136, 212]
        },
        {
            'name': 'Seattle',
            'lat': 47.60972222,
            'long': -122.33305556,
            'lxy': [66, 112]
        },
        {
            'name': 'Solomon Islands',
            'lat': -9.6457,
            'long': 160.1562,
            'lxy': [412, 176]
        },
        {
            'name': 'Stockholm',
            'lat': 59.3293,
            'long': 18.0686,
            'lxy': [240, 88]
        },
        {
            'name': 'Sydney',
            'lat': -33.8688,
            'long': 151.2093,
            'lxy': [402, 214]
        },
        {
            'name': 'Tokyo',
            'lat': 35.6762,
            'long': 139.6503,
            'lxy': [392, 118]
        },
        {
            'name': 'Tripoli',
            'lat': 32.8872,
            'long': 13.1913,
            'lxy': [244, 136]
        },
        {
            'name': 'Vladivostok',
            'lat': 43.1198,
            'long': 131.8869,
            'lxy': [388, 104]
        }
    ]

def load_data():

    tzlocal = pytz.timezone('US/Eastern')
    tzutc = pytz.timezone('UTC')
    DIR_MAIN = Path(os.path.dirname(os.path.realpath(__file__))).parent

    file_name = DIR_MAIN / 'src' / 'sun_times.json'
    data = read_data(file_name)

    if data:
        cities = data['cities']
    else:
        cities = generate_city_info()

    for city in cities:
        print(f"Retrieving data for {city['name']}...", end='')
        now = datetime.utcnow().replace(tzinfo=tzutc).astimezone(tzlocal)
        data = json.loads(requests.get(f"https://api.sunrise-sunset.org/json?lat={city['lat']}&lng={city['long']}").text)
        sunrise_raw = datetime.strptime(data['results']['sunrise'], '%I:%M:%S %p')
        sunset_raw = datetime.strptime(data['results']['sunset'], '%I:%M:%S %p')
        sunrise = now.replace(hour=sunrise_raw.hour, minute=sunrise_raw.minute, second=sunrise_raw.second, microsecond=0, tzinfo=pytz.timezone('UTC'))
        sunset = now.replace(hour=sunset_raw.hour, minute=sunset_raw.minute, second=sunset_raw.second, microsecond=0, tzinfo=pytz.timezone('UTC'))
        city['sunrise'] = datetime.strftime(sunrise.astimezone(tzlocal), '%Y-%m-%d %H:%M:%S%z')
        city['sunset'] = datetime.strftime(sunset.astimezone(tzlocal), '%Y-%m-%d %H:%M:%S%z')
        print('Done')

    print('Saving JSON file...', end='')
    timestamp = datetime.strftime(datetime.now().date(), '%Y-%m-%d')
    info = {
        'timestamp': timestamp,
        'cities': cities
    }
    write_data(file_name, info)
    
    print('Done')
    return info

def read_data(file_name):

    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def write_data(file_name, info):

    with open(file_name, 'w') as f:
        json.dump(info, f)