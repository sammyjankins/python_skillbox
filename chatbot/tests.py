from copy import deepcopy
from pprint import pprint
from unittest import TestCase
from unittest.mock import patch, Mock

from vk_api.bot_longpoll import VkBotMessageEvent

import bot_utils
from bot import Bot


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new', 'object': {
        'message': {'date': 1598455693, 'from_id': 7136548, 'id': 105, 'out': 0, 'peer_id': 7136548, 'text': 'lslls',
                    'conversation_message_id': 103, 'fwd_messages': [], 'important': False, 'random_id': 0,
                    'attachments': [], 'is_hidden': False},
        'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link'], 'keyboard': True,
                        'inline_keyboard': True, 'carousel': False, 'lang_id': 0}}, 'group_id': 197725410,
                 'event_id': '95d7dcdce59ab9a3576139461610e56c0d43e165'}
    INPUTS = [
        "Привет",  # для этого случая будет проверяться вызывалась ли соответствующая функция
        "А когда?",
        "Где будет конференция?",
        "Зарегистрируй меня",
        "Вениамин",
        "мой адрес email@email",
        "email@email.ru",
    ]
    EXPECTED_OUTPUTS = [
        bot_utils.INTENTS[0]['answer'],
        bot_utils.INTENTS[1]['answer'],
        bot_utils.SCENARIOS['registration']['steps']['step1']['text'],
        bot_utils.SCENARIOS['registration']['steps']['step2']['text'],
        bot_utils.SCENARIOS['registration']['steps']['step2']['failure_text'],
        bot_utils.SCENARIOS['registration']['steps']['step3']['text'].format(name='Вениамин', email='email@email.ru')
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

        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['message']['text'] = input_text
            events.append(VkBotMessageEvent(event))
            pprint(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.default_answer_method = Mock()
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []

        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])

        assert real_outputs[1:] == self.EXPECTED_OUTPUTS
        assert bot.default_answer_method.call_count == 1
