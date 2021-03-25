# -*- coding: utf-8 -*-


# заполняется заранее, чтобы пользователь долго не ждал ответа
import re
from collections import deque
from pprint import pprint
from random import choice
from threading import Thread, Lock
from time import sleep

import requests
from bs4 import BeautifulSoup

twisted_words = deque()


# фильтрация ненормативной лексики

def decipher_word(word_):
    """Для расшифровки таинственного текстового файла..."""
    word_ = word_[::-1]
    i = sum(map(str.isdigit, word_))
    decoded = chr(int(word_[:i]))
    if len(word_) > i + 1:
        decoded += word_[-1]
    if len(word_) > i:
        decoded += word_[i + 1:-1] + word_[i:i + 1]
    return decoded


def decipher_this(string):
    return ' '.join(map(decipher_word, string.split()))


with open('foul_language_for_filter.txt', mode='r', encoding='utf8') as file:
    foul_language = file.read()
    foul_words = [decipher_this(value) for value in foul_language.split(', ')][:-2]


def foul_filter(text):
    """Фильтр неугодных словечек"""
    text = text.lower()  # проверяемое слово
    words = foul_words  # список искомых слов

    for word in words:
        for part in range(len(text)):
            fragment = text[part: part + len(word)]
            if distance(fragment, word) <= len(word) * 0.25:
                return False
    return True


def distance(a, b):
    """Расстояние Левенштейна для выявления похожих слов
    https://en.wikipedia.org/wiki/Levenshtein_distance"""
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


global_url = 'https://altwall.net/'

# если хотите попробовать другую группу, линк вставлять сюда
band = 'mutanthvlam'
band_url = f'{global_url}texts.php?show={band}'
response = requests.get(band_url)
response.encoding = 'windows-1251'

lyrics_soup = BeautifulSoup(response.text, features='html.parser')
lyrics_table = lyrics_soup.find('table', attrs={'class': 'texts_table'})
links = [f'{global_url}{tag.attrs["href"]}' for tag in lyrics_table.find_all('a')]


def twisted_answer():
    """Эксперимент... вместо дефолтного ответа случайная фраза из текстов песен
    пропущеная через фильтр дурного лексикона."""
    text_url = choice(links)
    txt_response = requests.get(text_url)
    txt_response.encoding = 'windows-1251'
    text_soup = BeautifulSoup(txt_response.text, features='html.parser')
    raw_text = str(text_soup.find('article').contents[1]).split('<br/>')

    re_text = re.compile(r'[\w\s?.,!:"-]+[^\r]')

    clear_lines = [re.match(re_text, x).group()
                   for x in raw_text
                   if re.match(re_text, x)]

    out_lines = []

    while len(out_lines) != 3:
        line = choice(clear_lines)
        if foul_filter(line):
            out_lines.append(line)

    return ' '.join(out_lines)


class FillThis(Thread):
    """Заполнение "ответов по умолчанию" """

    def __init__(self, container, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container = container

    def run(self):
        while True:
            if len(self.container) < 10:
                self.container.append(twisted_answer())
            else:
                sleep(5)
                print(twisted_words)
                continue


def get_answer():
    return twisted_words.popleft()


def all_artist_lyrics():
    """Сохраняет все тексты исполнителя в {band}.txt в одну кучу."""
    txt = []
    for link in links:
        txt_response = requests.get(link)
        txt_response.encoding = 'windows-1251'
        text_soup = BeautifulSoup(txt_response.text, features='html.parser')
        raw_text = str(text_soup.find('article').contents[1]).split('<br/>')

        re_text = re.compile(r'[\w\s?.,!:"-]+[^\r]')

        clear_lines = [re.match(re_text, x).group()
                       for x in raw_text
                       if re.match(re_text, x)]
        txt.append('\n'.join(clear_lines))
    with open(f'{band}.txt', mode='w', encoding='utf8') as f:
        f.write('\n'.join(txt))


# filler = FillThis(twisted_words)
# lock = Lock()
# with lock:
#     filler.start()
if __name__ == '__main__':
    pass
