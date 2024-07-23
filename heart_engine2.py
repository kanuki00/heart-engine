import sys
import json
import datetime as dt
from he2_types import vector2
from he2_types import vector3
from he2_types import triangle
from he2_types import cross
from he2_types import dot
from he2_types import point_in_triangle

render_resolution = vector2(100, 50)
pixel_list = []
frame = {}
exe_time_limit = 10 # seconds

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
        
def make_pixel_list(resolution):
    result = []
    for x in range(resolution.x):
        for y in range(resolution.y):
            result.append(vector2(x, y))
    return result
        
def rasterize_pixel(in_pixel, in_triangles):
    global render_resolution
    global frame
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
    frame[pixel_keyform] = result # setting a dict key that doesn't exist adds the key to the dict
    
def pixel_worker(in_start, in_end, tris):
    global pixel_list
    end = min(in_end, len(pixel_list))
    for i in range(in_start, end):
        pixel = pixel_list[i]
        rasterize_pixel(pixel, tris)    
        
def render_frame():
    rend_start_time = dt.datetime.now()
    global render_resolution
    global frame
    
    persp_proj_tris = [
        triangle(vector3(0, 0.5, 0), vector3(-0.66, -0.33, 0), vector3(0.66, -0.33, 0)),
        triangle(vector3(0.5, 0.7, 0), vector3(0.1, 0.5, 0), vector3(0.8, -0.33, 0))
        ]
    
    px_max = render_resolution.x*render_resolution.y
    #pixel_worker(2000, px_max-2000, persp_proj_tris)
    pixel_worker(0, px_max, persp_proj_tris)
    
    draw_frame(frame)
    sys.stdout.write(str((dt.datetime.now() - rend_start_time)/dt.timedelta(milliseconds=1))+"ms    \n")    
        
def main():
    exe_start_time = dt.datetime.now()
    global pixel_list
    global exe_time_limit
    pixel_list = make_pixel_list(render_resolution)
    while dt.datetime.now() - exe_start_time < dt.timedelta(seconds=exe_time_limit):
        render_frame()
    
if __name__=="__main__":
    main()
