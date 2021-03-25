from copy import deepcopy
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
    CORRECT_INPUTS = [
        "Привет",  # для этого случая будет проверяться вызывалась ли соответствующая функция

        "Помощь",
        "Заказ",
        "Канск",
        "Москва",
        "Рим",
        "0-06-2021",
        "02-06-2028",
        "02-06-2021",
        "170621MOWRO",
        "170621MOWROM",
        "6",
        "парочку",
        "3",
        "qwertyuiop",
        "ок",
        "Я стесняюсь писать свой номер телефона",
        "9876543210",

    ]

    # Работа хэндлеров проверяется на соответствии того, какой информацией наполнены ответы бота той информации
    # о маршрутах которая находится в json файле. Если файл удалить, маршруты будут сгенерированы автоматически заново
    # но тесты поломаются :(
    routes = get_random_departures()
    rt_dict = None
    for flight in routes[CORRECT_INPUTS[4]][CORRECT_INPUTS[5]]['flights']:
        if flight['id'] == CORRECT_INPUTS[10]:
            rt_dict = flight
            break

    EXPECTED_CORRECT_OUTPUTS = [
        bot_utils.DEFAULT_ANSWER,
        bot_utils.SCENARIOS['order']['steps']['step1']['text'][0],
        bot_utils.SCENARIOS['order']['steps']['step1']['failure_text'][0].format(cities=', '.join(bot_utils.CITIES)),
        bot_utils.SCENARIOS['order']['steps']['step2']['text'][0].format(from_=CORRECT_INPUTS[4]),
        bot_utils.SCENARIOS['order']['steps']['step3']['text'][0].format(from_=CORRECT_INPUTS[4],
                                                                         to=CORRECT_INPUTS[5]),
        bot_utils.SCENARIOS['order']['steps']['step3']['failure_text'][0],
        bot_utils.SCENARIOS['order']['steps']['step3']['failure_text'][1],
        bot_utils.SCENARIOS['order']['steps']['step5']['text'][0][:30],
        bot_utils.SCENARIOS['order']['steps']['step5']['failure_text'][0],
        bot_utils.SCENARIOS['order']['steps']['step6']['text'][0].format(
            route_description=f'{rt_dict["id"]} - {rt_dict["dow"]}, {rt_dict["date"]} {rt_dict["time"]}'),
        bot_utils.SCENARIOS['order']['steps']['step6']['failure_text'][0],
        bot_utils.SCENARIOS['order']['steps']['step6']['failure_text'][0],
        bot_utils.SCENARIOS['order']['steps']['step7']['text'][0],
        bot_utils.SCENARIOS['order']['steps']['step8']['text'][0].format(
            route_description=f'{rt_dict["id"]} - {rt_dict["dow"]}, {rt_dict["date"]} {rt_dict["time"]}',
            seats=CORRECT_INPUTS[13],
            total_cost=int(CORRECT_INPUTS[13]) * int(rt_dict['cost']),
            comment=CORRECT_INPUTS[14])[:80],
        bot_utils.SCENARIOS['order']['steps']['step9']['text'][0],
        bot_utils.SCENARIOS['order']['steps']['step9']['failure_text'][0],
        bot_utils.SCENARIOS['order']['steps']['step10']['text'][0].format(phone=CORRECT_INPUTS[17]),

    ]

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

        for input_text in self.CORRECT_INPUTS:
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

        assert send_mock.call_count == len(self.CORRECT_INPUTS)

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
