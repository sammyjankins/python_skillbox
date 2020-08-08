from random import randint

import vk_api
from vk_api import bot_longpoll

from chatbot._token import token

group_id = 197725410


class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=self.token)
        self.api = self.vk.get_api()
        self.long_poller = bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception as exc:
                print(exc)

    def on_event(self, event):
        if event.type == bot_longpoll.VkBotEventType.MESSAGE_NEW:
            self.api.messages.send(message=event.object['message']['text'],
                                   random_id=randint(0, 2 ** 20),
                                   peer_id=event.object['message']['peer_id'])

        else:
            print("Can't handle this type of event: ", event.type)


if __name__ == '__main__':
    bot = Bot(group_id, token)
    bot.run()
