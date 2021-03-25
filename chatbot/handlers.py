import re
from datetime import datetime

from aviabase import get_random_departures
from bot_utils import CITIES

re_name = re.compile(r'^[\w\-\s]{3,40}$')
re_email = re.compile(r"\b(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)\b")
re_city_patterns = {
    city: re.compile(r'{}'.format(re.sub(r'[- ]', '', city.lower()[:-2 if len(city) > 5 else None])))
    for city in CITIES}
routes = get_random_departures()


def handle_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handle_email(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context['email'] = matches[0]
        return True
    else:
        return False


def handle_city_from(text, context):
    return handle_city(text, context, 'from_')


def handle_city_to(text, context):
    return handle_city(text, context, 'to')


def handle_city(text, context, context_key):
    if not context.get('cities'):
        context['cities'] = ', '.join(CITIES)
    for key in re_city_patterns:
        if re.search(re_city_patterns[key], re.sub(r'[- ]', '', text.lower())):
            context[context_key] = key
            print(', '.join([x for x in routes[context['from_']]]))
            if context_key == 'to' and not bool(routes[context['from_']].get(context['to'])):
                context['step_index'] = 1
            else:
                context['step_index'] = 0
            return True
    return False


def check_future_date(user_date, flight_date):
    return datetime.fromisoformat(flight_date) >= datetime.fromisoformat(user_date)


def handle_date(text, context):
    try:
        day, month, year = text.split('-')
        iso_format = f'{year}-{month}-{day}'
        date = datetime.fromisoformat(iso_format)
        if date < datetime.today():
            context['text_index'] = 1
        flights = routes[context['from_']][context['to']]['flights']
        for flight in flights:
            if check_future_date(iso_format, flight['date']):
                flight_index = flights.index(flight)
                break
        else:
            context['failure_index'] = 1
            return False
        context['next_five'] = {flight['id']: flight for flight in flights[flight_index: flight_index + 5]}
        context['msg_five'] = '\n\n'.join(
            [f'{context["next_five"][flight]["id"]} - {context["next_five"][flight]["dow"]}'
             f', {context["next_five"][flight]["date"]} '
             f'{context["next_five"][flight]["time"]}\n'
             f'Стоимость рейса: {context["next_five"][flight]["cost"]}'
             for flight in context['next_five']])
        return True
    except ValueError:
        return False


def handle_route(text, context):
    if text in context['next_five']:
        route = context['next_five'][text]
        context.update({'route_id': text,
                        'route_description': f'{route["id"]} - {route["dow"]}, {route["date"]} {route["time"]}',
                        'route_cost': route["cost"]})

        return True


def handle_seats(text, context):
    if text.isdigit():
        if 1 <= int(text) <= 5:
            context['seats'] = int(text)
            context['total_cost'] = context['route_cost'] * context['seats']
            if context.get('comment'):
                context['step_index'] = 1
            return True


def handle_comment(text, context):
    context['comment'] = text
    return True


def handle_confirm(text, context):
    if 'ок' in text.lower():
        pass
    elif 'дат' in text.lower():
        context['step_index'] = 1
    elif 'мест' in text.lower():
        context['step_index'] = 2
    elif 'коммент' in text.lower():
        context['step_index'] = 3
    else:
        return False
    return True


def handle_phone(text, context):
    clear_phone = re.sub(r'\D', '', text)
    result = re.match(r'^[78]?\d{10}$', clear_phone)
    if bool(result):
        context['phone'] = result.group()
    return bool(result)
