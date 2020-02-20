import curses, json, os, pytz, requests
import backup_data
from datetime import datetime, timedelta

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

def main(stdscr, cities):
    global tzlocal
    global tzutc
    max_name_len = max([len(x['name']) for x in cities])
    keycode_q = 113
    keycode_r = 114

    stdscr.timeout(10)
    curses.use_default_colors()
    curses.init_pair(1, -1, -1) # <-Default
    curses.init_pair(2, 8, -1) # <-Gray
    curses.init_pair(3, 14, -1) # <-Yellow
    curses.init_pair(4, 11, -1) # <-Teal
    curses.init_pair(5, 28, -1) # <-Green
    curses.init_pair(6, 4, -1) # <-Red
    curses.init_pair(7, 32, -1) # <-Light blue
    stdscr.clear()

    while stdscr.getch() not in (keycode_q, keycode_r):
        stdscr.timeout(10000)
        now = datetime.utcnow().replace(tzinfo=tzutc).astimezone(tzlocal)
        
        for i, city in enumerate(cities):
            sunrise = datetime.strptime(city['sunrise'], '%Y-%m-%d %H:%M:%S%z')
            sunset = datetime.strptime(city['sunset'], '%Y-%m-%d %H:%M:%S%z')
            c = int(bool(sunrise < now < sunset or sunset < sunrise < now)) + 2
            stdscr.addstr(str(c) + ', ' + city['name'])
            curses.napms(20000) # TODO: WTF is going on
            stdscr.addstr(i, 0, city['name'] + ''.join([' ' for _ in range(max_name_len - len(city['name']))]), curses.color_pair(c))
            stdscr.addstr(' ↑', curses.color_pair(3))
            stdscr.addstr(f'{city["sunrise"].split(" ")[-1].split("-")[0]}  ', curses.color_pair(1))
            stdscr.addstr('↓', curses.color_pair(2))
            stdscr.addstr(f'{city["sunset"].split(" ")[-1].split("-")[0]}', curses.color_pair(1))
            stdscr.refresh()
        stdscr.addstr(len(cities) + 1, 0, 'Last updated ')
        stdscr.addstr(datetime.strftime(now, '%Y-%m-%d %H:%M:%S (UTC%z)'), curses.color_pair(5))

        stdscr.addstr('.\nThe next event is a ', curses.color_pair(1))
        event, location = get_next_event(cities, now)
        event_time_str = next((x[event] for x in cities if x['name'] == location), None)
        event_time = datetime.strptime(event_time_str, '%Y-%m-%d %H:%M:%S%z')
        arr_time = str(event_time - now).split(':')
        time_until_event = f'{arr_time[0]}h {arr_time[1]}m {round(float(arr_time[2]))}s'
        stdscr.addstr(event, curses.color_pair(3 if event == 'sunrise' else 6))
        stdscr.addstr(' in ', curses.color_pair(1))
        stdscr.addstr(location, curses.color_pair(7))
        stdscr.addstr(', occurring ', curses.color_pair(1))
        stdscr.addstr(time_until_event, curses.color_pair(5))
        stdscr.addstr(' from the last update.', curses.color_pair(1))

        arr_time = str(event_time - now.replace(second=0)).split(':')
        ms_left = (int(arr_time[0]) * 3600 + int(arr_time[1]) * 60) * 1000
        if ms_left < 60000:
            stdscr.addstr(f"\nNext update scheduled for {datetime.strftime(now + timedelta(seconds=5), '%Y-%m-%d %H:%M:%S (UTC%z)')}.", curses.color_pair(2))
            stdscr.timeout(5000)
        else:
            stdscr.addstr(f"\nNext update scheduled for {datetime.strftime(now.replace(second=0) + timedelta(milliseconds=ms_left), '%Y-%m-%d %H:%M:%S (UTC%z)')}.", curses.color_pair(2))
            stdscr.timeout(ms_left)

        stdscr.addstr('\nPress ', curses.color_pair(1))
        stdscr.addstr('[R]', curses.color_pair(4))
        stdscr.addstr(' to refresh or ', curses.color_pair(1))
        stdscr.addstr('[Q]', curses.color_pair(4))
        stdscr.addstr(' to quit.', curses.color_pair(1))

def read_data(file_name):
    try:
        with open(file_name, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def write_data(file_name, info):
    with open(file_name, 'w') as f:
        json.dump(info, f)

if __name__ == '__main__':

    global tzlocal
    global tzutc
    tzlocal = pytz.timezone('US/Eastern')
    tzutc = pytz.timezone('UTC')
    
    file_name = 'sun_times.json'

    data = read_data(file_name)
    if data:
        cities = data['cities']
        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d').date()
    else:
        cities = backup_data.generate_city_info()
        timestamp = datetime.strptime('1985-4-5', '%Y-%m-%d').date()

    # Sort cities by longitude
    sorted_cities = sorted(cities, key=lambda k: k['long'])

    if timestamp < datetime.now().date():
        if timestamp.year == 1985:
            print('Sunrise/sunset data file not found. Querying database for current times...')
        else:
            print(f'Sunrise/sunset data is not from today (last timestamp {timestamp}). Querying database for current times...')

        for city in sorted_cities:
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
        info = {
            'timestamp': datetime.strftime(datetime.now().date(), '%Y-%m-%d'),
            'cities': cities
        }
        write_data(file_name, info)
        print('Done')
    else:
        print(f'Sunrise/sunset data is current. Last load: {timestamp}')

    #curses.wrapper(main, sorted_cities)
