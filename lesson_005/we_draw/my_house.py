import simple_draw as sd
from .my_wall import draw_wall
from .my_shapes import triangle


def draw_house(x_start, y_start, x_end, y_end):
    y_step = (y_end - y_start) // 12
    x_step = (x_end - x_start) // 6
    wall_point = (x_start + (x_end - x_start) / 2) + y_step

    # roof
    x_roof = x_start
    y_roof = y_end - y_step // 2
    roof_len = x_end - x_start + x_step
    roof_step = roof_len // 20
    roof_width = roof_len // 10
    for _ in range(6):
        triangle(sd.get_point(x_roof, y_roof), 0, roof_len, color=sd.COLOR_DARK_YELLOW, width=roof_width)
        x_roof += 1.5 * roof_step
        y_roof += 1.5 * roof_step
        roof_len -= 3 * roof_step
        roof_width += roof_step

    # wall
    sd.line(sd.get_point(wall_point, y_start),
            sd.get_point(wall_point, y_end - y_step // 2),
            sd.COLOR_ORANGE,
            x_end - x_start + x_step)
    draw_wall(x_start, y_start, x_end, y_end)
    sd.line(sd.get_point(x_start, y_start), sd.get_point(x_start, y_end - y_step // 2), sd.COLOR_BLACK)
    sd.line(sd.get_point(x_start, y_end - y_step // 2), sd.get_point(x_end + x_step, y_end - y_step // 2),
            sd.COLOR_BLACK)
    sd.line(sd.get_point(x_end + x_step, y_end - y_step // 2), sd.get_point(x_end + x_step, y_start), sd.COLOR_BLACK)
    sd.line(sd.get_point(x_end + x_step, y_start), sd.get_point(x_start, y_start), sd.COLOR_BLACK)

    # window
    sd.line(sd.get_point(x_start + 4 * x_step - y_step, y_start + 4 * y_step),
            sd.get_point(x_start + 4 * x_step - y_step, y_end - 5 * y_step // 2), sd.COLOR_WHITE, x_step * 4)
