import sys
import engine_types as et


def home():
    sys.stdout.write("\033[H")


def draw(color):
    rgb_t = (color.x, color.y, color.z)
    fg_code = "\033[38;2;%d;%d;%dm" % rgb_t
    bg_code = "\033[48;2;%d;%d;%dm" % rgb_t
    reset = "\033[0m"
    sys.stdout.write(fg_code + bg_code + "A" + reset)


def draw_frame(frame_buffer, rend_resolution):
    home()
    for y in reversed(range(rend_resolution.y)):
        for x in range(rend_resolution.x):
            try:
                key = "%d,%d" % (x, y)
                draw(frame_buffer[key])
            except KeyError:
                draw(et.vector3(0, 0, 0))
        sys.stdout.write("\n")
