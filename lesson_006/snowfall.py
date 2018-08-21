import simple_draw as sd

blizzard = {'x': [],
            'y': [],
            'lens': [],
            'delta': [],
            'factors': []}


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


def draw_snowflakes(color):
    for i, x in enumerate(blizzard['x']):
        if blizzard['y'][i] > 20:
            sd.snowflake(sd.get_point(x, blizzard['y'][i]),
                         blizzard['lens'][i],
                         color,
                         blizzard['factors'][i][0],
                         blizzard['factors'][i][1],
                         blizzard['factors'][i][2])


def move_snowflakes():
    for i, x in enumerate(blizzard['x']):
        x += sd.randint(-100, 100)
        blizzard['y'][i] -= blizzard['delta'][i]


# сделал список из индексов дошедших до дна снежинок, чтобы их число не расло в
# геометрической прогрессии ¯\_(ツ)_/¯
# TODO: так они всё равно будут копиться в blizzard. Можно их оттуда просто выкидывать
bottomed = []


def bottom_count():
    count = 0
    for i,y in enumerate(blizzard['y']):  # TODO: пробел
        if y < 20:
            if i not in bottomed:
                count += 1
                bottomed.append(i)
    return count


def add_snowflakes(count):
    for _ in range(count):
        create_snowflakes(1)
