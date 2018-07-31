# -*- coding: utf-8 -*-

import simple_draw as sd

N = 20


def init_snow_params(x_max, y_max, n=N):
    x_levels = []
    y_levels = []
    lengths = []
    delta_y = []
    factors = []
    for _ in range(n):
        x_levels.append(sd.random_number(0, x_max - 6 * x_max // 10))
        y_levels.append(sd.random_number(y_max - y_max // 5, y_max))
        delta_y.append(sd.random_number(y_max // 20, y_max // 12))
        lengths.append(sd.random_number(5, x_max // 50))
        factors.append(((sd.random_number(3, 8) / 10), (sd.random_number(3, 8) / 10), sd.random_number(1, 60)))
    return {"x": x_levels, "y": y_levels, "lens": lengths, "delta": delta_y, "factors": factors}


def draw_snow(x_levels, y_levels, lengths, delta_y, factors):
    for index in range(N):
        if y_levels[index] > 50:
            sd.snowflake(sd.get_point(x_levels[index], y_levels[index]),
                         lengths[index],
                         sd.background_color,
                         factors[index][0],
                         factors[index][1],
                         factors[index][2])
            y_levels[index] -= delta_y[index]
            x_levels[index] += sd.random_number(-50, 50)
        else:
            y_levels[index] = sd.random_number(650, 800)
            delta_y[index] = sd.random_number(20, 60)
            factors[index] = ((sd.random_number(3, 8) / 10), (sd.random_number(3, 8) / 10), sd.random_number(1, 60))
        sd.snowflake(sd.get_point(x_levels[index], y_levels[index]),
                     lengths[index],
                     sd.COLOR_WHITE,
                     factors[index][0],
                     factors[index][1],
                     factors[index][2])
