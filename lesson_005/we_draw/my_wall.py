import simple_draw as sd


def draw_wall(x_start, y_start, x_end, y_end):
    y_step = (y_end - y_start) // 12
    x_step = (x_end - x_start) // 6
    y_levels = list(range(y_start, y_end, y_step))
    points = []
    for x_step in range(x_start, x_end, x_step):
        step = y_step
        x = x_step
        for y in y_levels:
            points.append(sd.get_point(x, y))
            x += step
            points.append(sd.get_point(x, y))
            step = -step
        sd.lines(points, sd.COLOR_BLACK)
        points = []
        step = y_step
        x += step
        for y in y_levels:
            points.append(sd.get_point(x, y))
            x -= step
            points.append(sd.get_point(x, y))
            step = -step
        sd.lines(points, sd.COLOR_BLACK)
        points = []
