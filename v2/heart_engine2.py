import sys
import json
import datetime as dt
from he2_types import vector2
from he2_types import vector3
from he2_types import triangle
from he2_types import boundbox
from he2_types import cross
from he2_types import dot
from he2_types import point_in_triangle
from he2_types import perspective_project
from he2_types import normalized
from he2_types import barycoords

render_resolution = vector2(200, 110)
pixel_list = []
frame = {}
exe_time_limit = 30 # seconds

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

def draw_frame():
    global render_resolution
    global frame
    sys.stdout.write("\033[H")
    for y in reversed(range(render_resolution.y)):
        for x in range(render_resolution.x):
            try:
                key = "%d,%d" % (x, y)
                draw(frame[key])
            except KeyError:
                draw(vector3(0,0,0))
        sys.stdout.write("\n")
        
def make_pixel_list(resolution):
    result = []
    for x in range(resolution.x):
        for y in range(resolution.y):
            result.append(vector2(x, y))
    return result
    
def get_bounds(tris):
    result = []
    for tri in tris:
        ax = min(tri.a.x, tri.b.x, tri.c.x)
        ay = max(tri.a.y, tri.b.y, tri.c.y)
        bx = max(tri.a.x, tri.b.x, tri.c.x)
        by = min(tri.a.y, tri.b.y, tri.c.y)
        result.append(boundbox(vector2(ax, ay), vector2(bx, by)))
    return result

def loadmeshjson(file):
    with open(file) as meshfile:
        raw_data = json.load(meshfile)
        result = []
        for tri in raw_data["Triangles"]:
            a = tri["A"]
            b = tri["B"]
            c = tri["C"]
            r_tri = triangle(vector3(a[0], a[1], a[2]), vector3(b[0], b[1], b[2]), vector3(c[0], c[1], c[2]))
            result.append(r_tri)
        return result
        
def rasterize_pixel(in_pixel, in_proj_triangles, in_triangles, in_tri_bounds):
    global render_resolution
    global frame
    result = vector3(0,0,0)
    test_x = in_pixel.x/render_resolution.x
    test_y = in_pixel.y/render_resolution.y
    test_loc = vector3(test_x*2-1, test_y*2-1, 0)
    shallowest = -10000000000 # TODO
    #was_drawn = False # TODO
    for i in range(len(in_proj_triangles)):
        p_tri = in_proj_triangles[i]
        p_tri2D = p_tri.omit_z()
        tri = in_triangles[i]
        bb = in_tri_bounds[i]
        if test_loc.x<bb.a.x or test_loc.x>bb.b.x or test_loc.y<bb.b.y or test_loc.y> bb.a.y:
            # skipping point in tri if test location is not in triangle bounding box
            continue
        if point_in_triangle(test_loc, p_tri2D):
            bary = barycoords(test_loc, p_tri2D)
            depth = p_tri.a.z*bary.x + p_tri.b.z*bary.y + p_tri.c.z*bary.z
            if depth > shallowest:
                shallowest = depth
                n = tri.normal()
                shade = max(dot(n, normalized(vector3(0.35, -0.2, 1.0))), 0)
                col = int(shade*255)
                result = vector3(col, col, col)
    pixel_keyform = "%d,%d" % (in_pixel.x, in_pixel.y)
    frame[pixel_keyform] = result # setting a dict key that doesn't exist adds the key to the dict

def render_frame(tris):
    rend_start_time = dt.datetime.now()
    global pixel_list
    # Step 1: perspective projection
    persp_proj_tris = perspective_project(None, tris)
    # Step 2: getting projected triangle's bounding boxes
    ppt_bounds = get_bounds(persp_proj_tris)
    # Step 3: rasterize pixel and write it into framebuffer
    for i in range(len(pixel_list)):
        pixel = pixel_list[i]
        rasterize_pixel(pixel, persp_proj_tris, tris, ppt_bounds)
    # Step 4: draw the frame buffer to the screen
    draw_frame()
    sys.stdout.write(str((dt.datetime.now() - rend_start_time)/dt.timedelta(milliseconds=1))+"ms    \n")
        
def main():
    exe_start_time = dt.datetime.now()
    global pixel_list
    global exe_time_limit
    pixel_list = make_pixel_list(render_resolution)
    clock = 0
    while dt.datetime.now() - exe_start_time < dt.timedelta(seconds=exe_time_limit):
        tris = loadmeshjson("weird_mesh.json")
        for t in tris:
            t.a = t.a + vector3(0,0,-0.011)*clock
            t.b = t.b + vector3(0,0,-0.011)*clock
            t.c = t.c + vector3(0,0,-0.011)*clock
        render_frame(tris)
        clock += 1
    
if __name__=="__main__":
    exit(main())