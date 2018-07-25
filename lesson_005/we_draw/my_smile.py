import simple_draw as sd


def draw_face(x, y, color, blink=False):
    left_point = sd.get_point(x, y)
    right_point = sd.get_point(x + 110, y + 90)
    sd.ellipse(left_point, right_point, color, 2)
    sd.circle(sd.get_point(x + 30, y + 60), 8, color, 2)
    if blink:
        sd.circle(sd.get_point(x + 80, y + 60), 8, sd.COLOR_WHITE, 2)
        sd.line(sd.get_point(x + 70, y + 60), sd.get_point(x + 90, y + 60), color, 2)
    else:
        sd.line(sd.get_point(x + 70, y + 60), sd.get_point(x + 90, y + 60), sd.COLOR_WHITE, 2)
        sd.circle(sd.get_point(x + 80, y + 60), 8, color, 2)
    points = [sd.get_point(x + 20, y + 30),
              sd.get_point(x + 45, y + 20),
              sd.get_point(x + 65, y + 20),
              sd.get_point(x + 90, y + 30)]
    sd.lines(points, color)
