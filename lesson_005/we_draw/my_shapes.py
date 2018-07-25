import simple_draw as sd


def draw_shapes(point, sides, angle_step, angle=0, length=200, color=sd.COLOR_BLACK, width=1):
    if sides is 1:
        return point
    v1 = sd.get_vector(start_point=point, angle=angle, length=length, width=width)
    v1.draw(color)
    point = draw_shapes(point=v1.end_point,
                        sides=sides - 1,
                        angle_step=angle_step,
                        angle=angle + angle_step,
                        length=length,
                        color=color,
                        width=width)
    return point


def triangle(point, angle=0, length=200, color=sd.COLOR_BLACK, width=10):
    width = width
    sides = 3
    angle_step = 360 / sides
    end_point = draw_shapes(point, sides, angle_step, angle, length, color=color, width=width)
    sd.line(point, end_point, color, width=width)
