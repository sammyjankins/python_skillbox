import json
import random
from datetime import datetime, timedelta
from pprint import pprint

from bot_utils import CITIES

WEEKDAYS = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье',
}


def get_random_period():
    periods = ['week', 'weekdays', 'day_of_month', None]
    period = random.choice(periods)
    config = {'period': period,
              'time': {'hour': (random.randint(5, 22)),
                       'minute': random.choice(range(0, 56, 5))}, }
    if period == 'week':
        config.update({'dow': random.randint(0, 6), })
    elif period == 'weekdays':
        config.update({'dow': sorted(random.sample(range(0, 6), random.randint(2, 4))), })
    elif period == 'day_of_month':
        config.update({'dom': sorted(random.sample(range(1, 29), random.randint(2, 4))), })
    return config


def random_cities():
    rand_cities = list(CITIES.copy())
    random.shuffle(rand_cities)
    return rand_cities


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    return sourcedate.replace(year=year, month=month, day=1)


def generate_routes():
    output = dict()
    for city in CITIES:
        output[city] = {
            destination: get_random_period()
            for destination in random_cities()[:-1]
            if city != destination}
    return output


def get_next(route_config, last_dep=None):
    today = datetime.today()
    next_dep_time = last_dep if last_dep else today.replace(hour=route_config['time']['hour'],
                                                            minute=route_config['time']['minute'])

    if route_config['period'] == 'week':

        if last_dep:
            next_dep_time += timedelta(days=7)

        elif today > next_dep_time or today.weekday() != route_config['dow']:
            next_dep_time += (
                timedelta(route_config['dow'] - today.weekday() + 7 * (today.weekday() >= route_config['dow'])))

    elif route_config['period'] == 'weekdays':
        if last_dep:
            next_dep_time += timedelta(days=1)
            while next_dep_time.weekday() not in route_config['dow']:
                next_dep_time += timedelta(days=1)
        else:
            try:
                next_dow = min(filter(lambda x: next_dep_time.weekday() - x < 0, route_config['dow']))
            except ValueError:
                next_dow = route_config['dow'][0]
            next_dep_time += timedelta(
                days=next_dow - next_dep_time.weekday() + 7 * (next_dep_time.weekday() >= next_dow))

    elif route_config['period'] == 'day_of_month':
        for day in route_config['dom']:
            if day > next_dep_time.day:
                next_dep_time = next_dep_time.replace(day=day)
                break
        else:
            next_dep_time = add_months(next_dep_time, 1)
            next_dep_time = next_dep_time.replace(day=route_config['dom'][0])
    else:
        next_dep_time += timedelta(days=random.randint(1, 4))
    return next_dep_time


def construct_flight(time, container, from_, to):
    flight_id = f'{time.strftime("%d%m%y")}{CITIES[from_]}{CITIES[to]}'
    container.append({
        'date': f'{time.strftime("%Y-%m-%d")}',
        'id': flight_id,
        'dow': f'{WEEKDAYS[time.weekday()]}',
        'time': f'{time.strftime("%H:%M")}',
        'cost': random.randint(8000, 80000),
    })


def get_random_departures():
    """
    Генерирует конфиг с маршрутами и сохраняет в json файл, при этом возвращает словарь с маршрутами
    либо, если существует файл, извлекает маршруты и него и возвращает в виде словаря.
    """
    route_dict = get_routes()
    for from_ in route_dict:
        for to in route_dict[from_]:

            route_config = route_dict[from_][to]
            flights = route_config.get('flights')
            if flights is not None:
                for flight in flights:
                    print(flight)
            else:

                flights = list()
                next_dep_time = get_next(route_config)

                while len(flights) != 100:
                    construct_flight(next_dep_time, flights, from_, to)
                    next_dep_time = get_next(route_config, next_dep_time)

                route_config['flights'] = flights
    return route_dict


def get_routes():
    try:
        with open('routes.json', 'r', encoding='utf8') as file:
            return json.load(file)
    except FileNotFoundError:
        route_dict = generate_routes()
        with open('routes.json', 'w', encoding='utf8') as file:
            json.dump(route_dict, file)
        return route_dict


user_test = {
    'from': 'Торонто',
    'to': 'Берлин',
    'when': '05-04-2021',
}


def check_future_date(user_date, flight_date):
    return datetime.fromisoformat(flight_date) >= datetime.fromisoformat(user_date)


def get_next_five(user, route_dict):
    day, month, year = user['when'].split('-')
    iso_format = f'{year}-{month}-{day}'
    flights = route_dict[user['from']][user['to']]['flights']
    flight_index = 0
    for flight in flights:
        if check_future_date(iso_format, flight['date']):
            flight_index = flights.index(flight)
            break
    user['next_five'] = {flight['id']: flight for flight in flights[flight_index: flight_index + 5]}
    return user['next_five']


if __name__ == '__main__':
    routes = get_random_departures()
    pprint(get_next_five(user=user_test, route_dict=routes))
