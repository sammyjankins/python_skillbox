import simple_draw as sd

ray_list = []


def generate_rays(x, y, size):
    for _ in range(10):
        rand_x = sd.random_number(x - size - 100, x + size + 100)
        rand_y = sd.random_number(y - size - 100, y + size + 100)
        ray_list.append(sd.get_point(rand_x, rand_y))


generate_rays(0, 0, 0)


def draw_sun(x, y, size):
    center = sd.get_point(x, y)
    for i in range(10):
        sd.line(center, ray_list[i - 1], sd.background_color, 5)
    sd.circle(center, size, width=0)
    ray_list.clear()
    generate_rays(x, y, size)
    for i in range(10):
        sd.line(center, ray_list[i - 1], sd.COLOR_YELLOW, 5)
