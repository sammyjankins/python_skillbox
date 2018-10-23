import simple_draw as sd

blizzard = {'x': [],
            'y': [],
            'lens': [],
            'delta': [],
            'factors': []}


# заполнение массива (в т.ч. при add)
def create_snowflakes(N):
    for _ in range(N):
        blizzard['x'].append(sd.random_number(0, sd.resolution[0]))
        blizzard['y'].append(sd.random_number(sd.resolution[1] - sd.resolution[1] // 5,
                                              sd.resolution[1]))
        blizzard['lens'].append(sd.random_number(sd.resolution[1] // 20, sd.resolution[1] // 12))
        blizzard['delta'].append(sd.random_number(30, sd.resolution[0] // 7))
        blizzard['factors'].append(((sd.random_number(3, 8) / 10),
                                    (sd.random_number(3, 8) / 10),
                                    sd.random_number(1, 60)))


# отрисовка снежинки
def draw_snowflake(color, index):
    sd.snowflake(sd.get_point(blizzard['x'][index], blizzard['y'][index]),
                 blizzard['lens'][index],
                 color,
                 blizzard['factors'][index][0],
                 blizzard['factors'][index][1],
                 blizzard['factors'][index][2])


# смещение каждой по очереди
def move_snowflakes():
    for i, x in enumerate(blizzard['x']):
        draw_snowflake(sd.background_color, i)
        x += sd.randint(-100, 100)
        blizzard['y'][i] -= blizzard['delta'][i]
        draw_snowflake(sd.COLOR_WHITE, i)


# подсчет падших, чистка blizzard
def bottom_count():
    count = 0
    for i, y in enumerate(blizzard['y']):
        if y < 20:
            draw_snowflake(sd.background_color, i - count)
            for flake in blizzard:
                blizzard[flake].pop(i - count)
            count += 1
    return count
