from copy import deepcopy
from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch, Mock

from vk_api.bot_longpoll import VkBotMessageEvent

import bot_utils
from aviabase import get_random_departures
from bot import Bot


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new', 'object': {
        'message': {'date': 1598455693, 'from_id': 7136548, 'id': 105, 'out': 0, 'peer_id': 7136548, 'text': 'lslls',
                    'conversation_message_id': 103, 'fwd_messages': [], 'important': False, 'random_id': 0,
                    'attachments': [], 'is_hidden': False},
        'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'], 'keyboard': True,
                        'inline_keyboard': True, 'carousel': False, 'lang_id': 0}}, 'group_id': 197725410,
                 'event_id': '95d7dcdce59ab9a3576139461610e56c0d43e165'}

    # Для проверки реакции на корректный ввод. Проверяем что хэндлеры обрабатывают наш ввод и бот выдает сообщения
    # последовательно по сценарию. В некоторых случаях проверяется начало получаемого от бота сообщения на совпадение
    # с ожидаемым от него текстом.

    # Работа хэндлеров проверяется на соответствии того, какой информацией наполнены ответы бота той информации
    # о маршрутах которая находится в json файле.

    # города для проверки (подбираем города, с учетом, что как минимум с между двумя из них нет маршрута)
    routes = get_random_departures()
    cities = list(bot_utils.CITIES)

    no_route_city = None
    city_from = None
    city_to = None
    for city in cities:
        city_from = city
        rt_dict = routes[city_from]
        city_to = list(rt_dict)[0]

        # ищем город, в который не будет рейса
        no_route_set = (set(cities) - {city for city in rt_dict} - {city_from})
        if no_route_set:
            no_route_city = no_route_set.pop()
            break

    print(f'from: {city_from}, to: {city_to}, except: {no_route_city}')

    # готовим даты для проверки
    today = datetime.today()
    late_date = (today + timedelta(weeks=200)).strftime('%d-%m-%Y')
    past_date = (today - timedelta(days=1)).strftime('%d-%m-%Y')
    regular_date = (today + timedelta(weeks=1)).strftime('%d-%m-%Y')

    INPUTS = [
        "Привет",  # для этого случая будет проверяться вызывалась ли соответствующая функция

        "Помощь",

        # города без маршрута
        "Заказ",
        "Простоквашино",
        city_from,
        no_route_city,

        # города
        "Заказ",
        city_from,
        city_to,

        # даты, заканчивая на прошедшей (остается возможность выбрать рейс)
        "0-06-2021",  # некорректная дата
        late_date,  # поздняя дата
        past_date,  # прошедшая дата

        # корректная дата
        "Заказ",
        city_from,
        city_to,
        regular_date,

        # рейсы
        "8",
        "первый",
        "1",

        # места
        "6",
        "парочку",
        "3",

        # коммент
        "qwertyuiop",

        # исправление даты
        "дата",
        regular_date,
        "1",
        "3",

        # исправление мест
        "места",
        "3",

        # исправление коммента
        "комментарий",
        "Новый коммент",

        "ок",
        "Я стесняюсь писать свой номер телефона",
        "9876543210",

    ]

    EXPECTED_CORRECT_OUTPUTS = [
        bot_utils.DEFAULT_ANSWER,

        # сценарий с городами, между которыми нет маршрута
        bot_utils.SCENARIOS['order']['steps']['step1']['text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step1']['failure_text']['regular'].format(
            cities=', '.join(bot_utils.CITIES)),
        bot_utils.SCENARIOS['order']['steps']['step2']['text']['regular'].format(from_=city_from),
        bot_utils.SCENARIOS['order']['steps']['step4']['text']['regular'],

        # сценарий с городами, между которыми есть маршрут
        bot_utils.SCENARIOS['order']['steps']['step1']['text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step2']['text']['regular'].format(from_=city_from),
        bot_utils.SCENARIOS['order']['steps']['step3']['text']['regular'].format(from_=city_from,
                                                                                 to=city_to),

        # даты заканчивая на прошедшей
        bot_utils.SCENARIOS['order']['steps']['step3']['failure_text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step3']['failure_text']['late_date'],
        bot_utils.SCENARIOS['order']['steps']['step5']['text']['past_date'][:30],

        # корректная дата
        bot_utils.SCENARIOS['order']['steps']['step1']['text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step2']['text']['regular'].format(from_=city_from),
        bot_utils.SCENARIOS['order']['steps']['step3']['text']['regular'].format(from_=city_from,
                                                                                 to=city_to),
        bot_utils.SCENARIOS['order']['steps']['step5']['text']['regular'][:30],

        # рейсы
        bot_utils.SCENARIOS['order']['steps']['step5']['failure_text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step5']['failure_text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step6']['text']['regular'].format(
            route_description=Mock())[:10],

        # места
        bot_utils.SCENARIOS['order']['steps']['step6']['failure_text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step6']['failure_text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step7']['text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step8']['text']['regular'].format(
            route_description=Mock(), seats=Mock(), total_cost=Mock(), comment=Mock())[:10],

        # исправление даты
        bot_utils.SCENARIOS['order']['steps']['step3']['text']['regular'].format(from_=city_from,
                                                                                 to=city_to),
        bot_utils.SCENARIOS['order']['steps']['step5']['text']['regular'][:30],
        bot_utils.SCENARIOS['order']['steps']['step6']['text']['regular'].format(
            route_description=Mock())[:10],
        bot_utils.SCENARIOS['order']['steps']['step8']['text']['regular'].format(
            route_description=Mock(), seats=Mock(), total_cost=Mock(), comment=Mock())[:10],

        # исправление мест
        bot_utils.SCENARIOS['order']['steps']['step6']['text']['regular'].format(
            route_description=Mock())[:10],
        bot_utils.SCENARIOS['order']['steps']['step8']['text']['regular'].format(
            route_description=Mock(), seats=Mock(), total_cost=Mock(), comment=Mock())[:10],

        # исправление комментария
        bot_utils.SCENARIOS['order']['steps']['step7']['text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step8']['text']['regular'].format(
            route_description=Mock(), seats=Mock(), total_cost=Mock(), comment=Mock())[:10],

        bot_utils.SCENARIOS['order']['steps']['step9']['text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step9']['failure_text']['regular'],
        bot_utils.SCENARIOS['order']['steps']['step10']['text']['regular'].format(phone=INPUTS[-1]),

    ]

    print(f"INPUTS = {len(INPUTS)}, OUTPUTS = {len(EXPECTED_CORRECT_OUTPUTS)}")

    def test_run(self):
        count = 5
        events = [{}] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call({})
                # assert bot.on_event.call_count == count

    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []

        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.default_answer_method = [Mock(), Mock()]
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []

        output_iterator = iter(self.EXPECTED_CORRECT_OUTPUTS)

        for call in send_mock.call_args_list:
            args, kwargs = call
            print(f'Реальный ответ: {kwargs["message"]}\n')
            try:
                print(f'Ожидаемый ответ: {next(output_iterator)}\n')
            except StopIteration:
                pass
            real_outputs.append(kwargs['message'])

        assert all([x[0].startswith(x[1]) for x in zip(real_outputs[1:], self.EXPECTED_CORRECT_OUTPUTS)])
        assert sum([mock.call_count for mock in bot.default_answer_method]) == 1
