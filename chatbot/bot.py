# -*- coding: utf-8 -*-


import logging.config
from pprint import pprint
from random import randint

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import handlers
from bot_utils import SCENARIOS, INTENTS
from log_config import log_config
# import twisted
from mark.mark import gen_funny

try:
    import settings
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')

# Вынес операции из урока в log_config и сделал их в виде дикт-конфига.
logging.config.dictConfig(log_config)
log = logging.getLogger('vk_bot_logger')


class UserState:
    """Состояние пользователя внутри сценария."""

    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or dict()


class Bot:
    """
    Echo bot for vk.com

    Use Python 3.7.6
    """

    def __init__(self, group_id, token):
        """

        :param group_id: id of group on vk
        :param token: access token of group on vk
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=self.token)
        self.api = self.vk.get_api()
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.user_states = dict()  # user -> UserState
        # self.default_answer_method = twisted.get_answer
        self.default_answer_method = gen_funny

    def run(self):
        """
        Running bot
        :return: None
        """
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
                pprint(event)
            except Exception as exc:
                log.exception(exc)

    def on_event(self, event):
        """
        Processing of incoming events
        :param event: VkBotEventType
        :return: None
        """

        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info(f"Can't handle this type of event: {event.type}")
            return

        pprint(event.object)

        user_id = event.object['message']['peer_id']
        text = event.object['message']['text']

        if user_id in self.user_states:
            text_to_send = self.continue_scenario(user_id=user_id,
                                                  text=text)
        else:
            for intent in INTENTS:
                log.debug(f'User gets {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(intent['scenario'], user_id)
                    break
            else:
                # Два варианта ответа по умолчанию - случайная фраза из текстов песен, либо фраза,
                # построенная цепями Маркова.

                # text_to_send = twisted.get_answer()
                text_to_send = self.default_answer_method()  # Марков

        self.api.messages.send(message=text_to_send,
                               random_id=randint(0, 2 ** 20),
                               peer_id=user_id)

    def start_scenario(self, scenario_name, user_id):
        scenario = SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.user_states[user_id] = UserState(scenario_name=scenario_name,
                                              step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = SCENARIOS[state.scenario_name]['steps']

        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        if handler(text, state.context):
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                state.step_name = step['next_step']
            else:
                log.info('Зарегистрирован: {name} - {email}'.format(**state.context))
                self.user_states.pop(user_id)
        else:
            text_to_send = step['failure_text'].format(**state.context)

        return text_to_send


if __name__ == '__main__':
    # configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
