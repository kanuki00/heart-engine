import sys
import json
from he2_types import vector2
from he2_types import vector3
from he2_types import triangle
from he2_types import cross
from he2_types import dot
from he2_types import point_in_triangle

render_resolution = vector2(100, 50)
frame = {}
# Debug, del later
frame_example = {"78,47":vector3(255, 255, 0),"0,0":vector3(255, 0, 0), "34,5":vector3(0, 128, 0)}
frame_example["5,27"] = vector3(255, 0, 255)
# debug end

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
        
def rasterize_pixel(in_pixel, in_frame, in_triangles):
    global render_resolution
    result = vector3(0,0,0)
    test_x = in_pixel.x/render_resolution.x
    test_y = in_pixel.y/render_resolution.y
    test_loc = vector3(test_x*2-1, test_y*2-1, 0)
    for tri in in_triangles:
        tri2D = tri.omit_z()
        # TODO triangle bounding box optimization
        if point_in_triangle(test_loc, tri2D):
            result = vector3(255, 255, 255)
    pixel_keyform = "%d,%d" % (in_pixel.x, in_pixel.y)
    in_frame[pixel_keyform] = result
        
def main():
    global render_resolution
    global frame
    persp_proj_tris = [triangle(vector3(0, 0.5, 0), vector3(-0.66, -0.33, 0), vector3(0.66, -0.33, 0))]
    for x in range(render_resolution.x):
        for y in range(render_resolution.y):
            rasterize_pixel(vector2(x, y), frame, persp_proj_tris)
    draw_frame(frame)
    print("%fms" % 0.0)
if __name__=="__main__":
    main()
#     print(dot(vector3(0,0,1), vector3(0,1,0)))
#     print(cross(vector3(0,0,1), vector3(0,1,0)).to_string())