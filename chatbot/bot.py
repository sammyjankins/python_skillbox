import logging.config
from random import randint

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from log_config import log_config

try:
    import settings
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')

# Вынес операции из урока в log_config и сделал их в виде дикт-конфига.
logging.config.dictConfig(log_config)
log = logging.getLogger('vk_bot_logger')


class Bot:
    """
    Echo bot for vk.com

    Use Python 3.7
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

    def run(self):
        """
        Running bot
        :return: None
        """
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception as exc:
                log.exception(exc)

    def on_event(self, event):
        """
        Processing of incoming events
        :param event: VkBotEventType
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.info(f"Sending message back: {event.object['message']['text']}")
            self.api.messages.send(message=event.object['message']['text'],
                                   random_id=randint(0, 2 ** 20),
                                   peer_id=event.object['message']['peer_id'])
        else:
            log.info(f"Can't handle this type of event: {event.type}")


if __name__ == '__main__':
    # configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
