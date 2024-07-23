import sys
from he2_types import vector3
from he2_types import triangle

render_resolution = vector3(100, 50, 0)
frame = {}
frame_example = {"78,47":vector3(255, 255, 0),"0,0":vector3(255, 0, 0), "34,5":vector3(0, 128, 0)}

def draw(color):
    rgb_t = (color.x, color.y, color.z)
    fg_code = "\033[38;2;%d;%d;%dm" % rgb_t
    bg_code = "\033[48;2;%d;%d;%dm" % rgb_t
    reset = "\033[0m"
    sys.stdout.write(fg_code+bg_code+"A"+reset)

def draw_frame(in_frame):
    global render_resolution
    sys.stdout.write("\033[H")
    for y in reversed(range(render_resolution.y)):
        for x in range(render_resolution.x):
            try:
                key = "%d,%d" % (x, y)
                draw(in_frame[key])
            except KeyError:
                draw(vector3(0,0,0))
        sys.stdout.write("\n")
        
draw_frame(frame_example)