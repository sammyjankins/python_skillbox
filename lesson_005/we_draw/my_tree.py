import simple_draw as sd


def draw_bunches(start_point, angle, length):
    if length < 7:
        return
    v1 = sd.get_vector(start_point=start_point, angle=angle, length=length, width=3)
    if length > 20:
        v1.draw(sd.COLOR_DARK_YELLOW)
    else:
        v1.draw(sd.COLOR_DARK_GREEN)
    next_point = v1.end_point
    next_angle1 = angle - (30 + 30 * 0.01 * sd.random_number(-40, 40))
    next_angle2 = angle + (30 + 30 * 0.01 * sd.random_number(-40, 40))
    next_length = length * (.75 + .75 * 0.01 * sd.random_number(-20, 20))
    draw_bunches(start_point=next_point, angle=next_angle1, length=next_length)
    draw_bunches(start_point=next_point, angle=next_angle2, length=next_length)
