import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)


def draw_rainbow(x_left, x_right, y_left, y_right, colors=rainbow_colors):
    for color in colors:
        sd.ellipse(sd.get_point(x_left, y_left),
                   sd.get_point(x_right, y_right),
                   color,
                   20)
        x_left += 15
        y_right -= 15
