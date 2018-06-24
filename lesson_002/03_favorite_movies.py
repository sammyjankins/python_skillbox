#!/usr/bin/env python3
# -*- coding: utf-8 -*-

my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'

first_comma = my_favorite_movies.find(',')
last_comma = my_favorite_movies.rfind(',')
print(my_favorite_movies[:first_comma])
print(my_favorite_movies[last_comma:].strip(', '))
print(my_favorite_movies[first_comma:my_favorite_movies.find(',', first_comma+1)].strip(', '))
print(my_favorite_movies[my_favorite_movies.rfind(',', 0, last_comma):last_comma].strip(', '))
