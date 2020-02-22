import json, os, pytz, requests
import backup_data
from datetime import date, datetime, timedelta

def get_next_event(cities, now):
    min_diff = 9999
    event = None
    location = None

    for city in cities:

        sunrise = datetime.strptime(city['sunrise'], '%Y-%m-%d %H:%M:%S%z')
        sunset = datetime.strptime(city['sunset'], '%Y-%m-%d %H:%M:%S%z')

        if sunrise > now:
            diff = sunrise - now
            if diff.seconds < min_diff:
                min_diff = (sunrise - now).seconds
                event = 'sunrise'
                location = city['name']

        if sunset > now:
            diff = sunset - now
            if diff.seconds < min_diff:
                min_diff = (sunset - now).seconds
                event = 'sunset'
                location = city['name']

    return (event, location)

def read_data(file_name):

    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def write_data(file_name, info):

    with open(file_name, 'w') as f:
        json.dump(info, f)

def load_data():

    tzlocal = pytz.timezone('US/Eastern')
    tzutc = pytz.timezone('UTC')
    
    file_name = 'sun_times.json'
    data = read_data(file_name)

    if data:
        cities = data['cities']
    else:
        cities = backup_data.generate_city_info()

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
