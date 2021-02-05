# -*- coding: utf-8 -*-
# ==================================================
#
# !!! PYTHON 3.7.6 !!!
# Оригинальный алгоритм:
# https://github.com/maryszmary/Algorithm-Testament
#
# ==================================================
import os
import pickle
import re
from pprint import pprint
from string import punctuation

import markovify
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

nltk.download('punkt')
nltk.download('stopwords')
stopset = stopwords.words('russian')
punct = list(punctuation)


def clear_text(txt):
    first = [re.sub(r'[0-9]+.?', '', val) for val in txt.split('\n\n')]
    second = [re.sub(r'\xa0', ' ', val) for val in first]
    return '\n\n'.join(second).replace('=', '')


# за основу взяты:
# 1 - Энциклопедия экстремальных ситуаций, А. Гостюшин
# 2 - Сатанинская библия, А. Лавей
# 3 - Несколько книг по садоводству, имена авторов забыл

with open('extrim.txt', encoding='utf8') as f:
    txt_1 = clear_text(f.read())

with open('lavey.txt', encoding='cp1251') as f:
    txt_2 = clear_text(f.read())

with open('sad.txt', encoding='utf8') as f:
    txt_3 = clear_text(f.read())

text = txt_1 + txt_2 + txt_3
text_m = markovify.Text(text)
with open('lm.bin', 'wb') as f:
    pickle.dump(text_m, f)

# ВАЖНО:
# для переформирования датасета (при изменении источников текста) нужно удалить папку data
path = 'data'
filename = 'text_garbage'
if not os.path.exists(path):
    print('CREATE AND SAVE TO CSV...')
    base = sent_tokenize(txt_3)
    modifier = sent_tokenize(txt_1 + txt_2)

    sentences = base + modifier
    labels = ['base'] * len(base) + ['modifier'] * len(modifier)

    df = pd.DataFrame({'sentences': sentences, 'labels': labels})
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(f'{filename}.csv', index=False)

    os.mkdir(path)
    os.rename(f'{filename}.csv', f'{path}/{filename}.csv')
else:
    print('READING FROM CVS...')
    df = pd.read_csv(f'{path}/{filename}.csv')

X_train, X_test, y_train, y_test = train_test_split(df['sentences'], df['labels'], test_size=0.2, random_state=42)


def my_preprocessor(in_text):
    in_text = word_tokenize(in_text.lower())
    return [w for w in in_text if w not in stopset + punct]


def is_funny(sent, model, min_p, max_p):
    return min_p < model.predict_proba([sent])[0][1] < max_p


def console_test():
    while True:
        answer = input('\nВведите что угодно либо "стоп"\n>> ')
        if answer == 'стоп':
            print('Ну ок...')
            break
        else:
            pprint(gen_funny())


def gen_funny():
    while True:
        try:
            sent = text_m.make_sentence()
            if is_funny(sent, ppl, 0.30, 0.98):
                return sent
        except AttributeError as e:
            print(e)
            continue


ppl = Pipeline(
    [('vect', TfidfVectorizer(min_df=5, tokenizer=my_preprocessor)),
     ('nb', MultinomialNB())]
)
ppl.fit(X_train, y=y_train)

print(classification_report(y_test, ppl.predict(X_test)))
print(accuracy_score(y_test, ppl.predict(X_test)))

with open('algtest_classifyer.clf', 'wb') as f:
    pickle.dump(ppl, f)

if __name__ == '__main__':
    console_test()
