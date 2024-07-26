import sys
import random
import math
import datetime as dt
from datetime import datetime
import json

import numpy as np
import quaternion

# Konsole complete zoom out perfect square is 4x7

def vec2D(x, y):
    return np.array([x, y])

## CLASSES
class vector3:
    x = 0.0
    y = 0.0
    z = 0.0
    def __init__(self, inx, iny, inz):
        self.x = inx
        self.y = iny
        self.z = inz
    def __sub__(self, o):
        res = self.asnp() - o.asnp()
        return vector3(res[0], res[1], res[2])
    def __mul__(self, other):
        return vector3(self.x*other, self.y*other, self.z*other)
    def __truediv__(self, other):
        return vector3(self.x/other, self.y/other, self.z/other)
    def __add__(self, other):
        return vector3(self.x+other.x, self.y+other.y, self.z+other.z)
    def maprgb(self):
        # clamping with np.clip because color will always be 0 if r, g or b is negative
        return vector3(np.clip(0, self.x*255, 255), np.clip(0, self.y*255, 255), np.clip(0, self.z*255, 255))
    def print(self):
        print("X=%f, Y=%f, Z=%f" % (self.x, self.y, self.z))
    def as2D(self):
        return vector3(self.x, self.y, 0)
    def asnp(self):
        return np.array([self.x, self.y, self.z])
        
class triangle:
    a = vector3
    b = vector3
    c = vector3
    def __init__(self, ina, inb, inc):
        if isinstance(ina, vector3) == False or isinstance(inb, vector3) == False or isinstance(inc, vector3) == False:
            raise Exception("value(s) is not a vector3!")
        self.a = ina
        self.b = inb
        self.c = inc
    def area2D(self):
        a2D = self.a.as2D()
        b2D = self.b.as2D()
        c2D = self.c.as2D()
        ab = b2D - a2D
        ac = c2D - a2D
        cross = mcross(ab, ac)
        return abs(mlength(cross) / 2)
    def normal(self):
        ab = self.b - self.a
        ac = self.c - self.a
        cross = mcross(ab, ac)
        return mnormalized(cross)

class bary_res:
    def __init__(self, in_triangle, barycoord):
        self.in_triangle = in_triangle
        self.barycoord = barycoord
        
class rgb:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

class res:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        
class tri2D:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

class transform:
    pass

class gameobj_def:
    def __init__(self):
        self.transform = transform
        
## VECTORMATH
def mcross(a, b):
    if isinstance(a, vector3) and isinstance(b, vector3):
        npa_a = a.asnp()
        npa_b = b.asnp()
        res = np.cross(npa_a, npa_b)
        return vector3(res[0], res[1], res[2])
    else:
        raise Exception("a or b was not a vector3")

def mlength(v):
    if isinstance(v, vector3) == False:
        raise Exception("v is not a vector3")
    return math.sqrt(mdotproduct(v, v))
    
def mnormalized(v):
    if isinstance(v, vector3) == False:
        raise Exception("v is not a vector3")
    return v/mlength(v)
        
def mdotproduct(a, b):
    if isinstance(a, vector3) == False or isinstance(b, vector3) == False:
        raise Exception("a or b was not a vector3")
    return a.x*b.x + a.y*b.y + a.z*b.z
  
def get_point_in_tri2D(point, tri):
    tri_a = triangle(point, tri.a, tri.b)
    tri_b = triangle(point, tri.b, tri.c)
    tri_c = triangle(point, tri.c, tri.a)
    comboarea = tri_a.area2D() + tri_b.area2D() + tri_c.area2D()
    bary = vector3(tri_b.area2D()/tri.area2D(), tri_c.area2D()/tri.area2D(), tri_a.area2D()/tri.area2D())
    diff = tri.area2D() - comboarea
    tol = 0.0001
    if diff > -tol and diff < tol:
        return bary_res(True, bary)
    else:
        return bary_res(False, bary)
     
def line_plane_intersect(line_start, line_end, plane_point, plane_normal):
    epsilon = 0.0001
    w = line_end - plane_point
    u = line_end - line_start
    dot1 = mdotproduct(u, plane_normal)
    dot2 = mdotproduct(plane_normal, w)
    if dot1 > -epsilon and dot1 < epsilon:
        return None
    f = dot2/dot1
    return (u*-f)+line_end
    
def safedivide(a, b):
    if b == 0:
        return a
    return a/b
    
def project_vec3_vec3(dest, source):
    d = mdotproduct(dest, source)
    f = d / mlength(dest)
    return mnormalized(dest)*f
    
def pp_helper(right, up, proj, plane_loc, ogvert, cam_loc):
    to_p = proj-plane_loc
    xdot = mdotproduct(right, proj)
    xsign = safedivide(xdot, abs(xdot))
    x = mlength(project_vec3_vec3(right, to_p))/mlength(right) * xsign
    ydot = mdotproduct(up, proj)
    ysign = safedivide(ydot, abs(ydot))
    y = mlength(project_vec3_vec3(up, to_p))/mlength(up) * ysign
    z = -mlength(ogvert-cam_loc)
    return vector3(x, y, z)

def perspective_project(camera, triangles):
    cam_loc = vector3(2.8, -4.6, 2) # placeholder
    cam_plane_normal = vector3(-0.48878, 0.797416, -0.353874) # placeholder
    cam_plane_loc = cam_loc + cam_plane_normal * 4
    cam_right_vec = mnormalized(mcross(cam_plane_normal, vector3(0,0,1)))
    cam_up_vec = mcross(cam_right_vec, cam_plane_normal)
    result = []
    for tri in triangles:
        result_tri = triangle(vector3(0,0,0), vector3(0,0,0), vector3(0,0,0))
        proj_a = line_plane_intersect(tri.a, cam_loc, cam_plane_loc, cam_plane_normal)
        proj_b = line_plane_intersect(tri.b, cam_loc, cam_plane_loc, cam_plane_normal)
        proj_c = line_plane_intersect(tri.c, cam_loc, cam_plane_loc, cam_plane_normal)
#         a_x = mlength(project_vec3_vec3(cam_right_vec, proj_a-cam_plane_loc))/mlength(cam_right_vec)
#         a_y = mlength(project_vec3_vec3(cam_up_vec, proj_a-cam_plane_loc))/mlength(cam_up_vec)
#         a_z = -mlength(tri.a-cam_loc)
#         result_tri.a = vector3(a_x, a_y, a_z)
        result_tri.a = pp_helper(cam_right_vec, cam_up_vec, proj_a, cam_plane_loc, tri.a, cam_loc)
        result_tri.b = pp_helper(cam_right_vec, cam_up_vec, proj_b, cam_plane_loc, tri.b, cam_loc)
        result_tri.c = pp_helper(cam_right_vec, cam_up_vec, proj_c, cam_plane_loc, tri.c, cam_loc)
        result.append(result_tri)
    return result

## GLOBAL VARS ##
nprgb = rgb()
home = "\033[H"
screensize = vec2D(100, 40)
exe_time_limit = 20
game_modules = []

## FUNCS ##
def set_nprgb(new_rgb):
    global nprgb
    nprgb.r = new_rgb.x
    nprgb.g = new_rgb.y
    nprgb.b = new_rgb.z

def rgbcode():
    global nprgb
    t = (nprgb.r, nprgb.g, nprgb.b, nprgb.r, nprgb.g, nprgb.b)
    return "\033[38;2;%d;%d;%dm\033[48;2;%d;%d;%dm" % t
    
def rand255():
    return math.trunc(random.random()*255)

def solidcolorframe(new_r, new_g, new_b):
    global screensize
    set_nprgb(new_r, new_g, new_b)
    for i in range(screensize.height):
        line = ""
        for j in range(screensize.width):
            line += "A"
        sys.stdout.write("%s%s\n" % (rgbcode(), line))
        
def randcolorframe():
    global screensize
    sys.stdout.write(home)
    for i in range(screensize[1]):
        line = ""
        for j in range(screensize[0]):
            set_nprgb(rand255(),rand255(),rand255())
            line += rgbcode()+"A"
        sys.stdout.write("%s\n" % (line))    
    sys.stdout.write("\033[0m")
    
def rasterizeframe(proj_tris, tris):
    global screensize
    sys.stdout.write(home)
    canvas_size = vec2D(2., 1.5)
    step_x = canvas_size[0] / screensize[0]
    step_y = canvas_size[1] / screensize[1]
    for i in reversed(range(screensize[1])):    # screensize Y
        for j in range(screensize[0]):          # screensize X
            x = step_x*j-canvas_size[0]/2
            y = step_y*i-canvas_size[1]/2
            shallowest = -10000000000
            was_drawn = False
            for k in range(len(proj_tris)):
                ptri = proj_tris[k]
                tri = tris[k]
                result = get_point_in_tri2D(vector3(x, y, 0), ptri)
                if result.in_triangle:
                    depth = ptri.a.z*result.barycoord.x + ptri.b.z*result.barycoord.y + ptri.c.z*result.barycoord.z
                    if depth > shallowest:
                        shallowest = depth
                        set_nprgb(tri.normal().maprgb())
                        was_drawn = True
                elif was_drawn == False:
                    set_nprgb(vector3(60, 60, 60))
            sys.stdout.write(rgbcode()+"A")
        sys.stdout.write("\n")
    sys.stdout.write("\033[0m") # reset colors so that any normal text after frame will be printed properly
    
def loadworld(dir, file):
    global game_modules
    wdata = json.load(file)
    for obj in wdata["content"]:
        if obj["code"] != None:
            path = dir+"."+obj["code"]
            game_modules.append(__import__(path, globals(), locals(), [obj["code"]], 0))
    
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

## MAIN ##
def main():
    global game_modules
    args = sys.argv[1:]
    gamedir = ""
    if len(args) > 0:
        gamedir = args[0]
    try:
        with open(gamedir+"/world1.json") as worldfile:
            loadworld(gamedir, worldfile)
            starttime = datetime.now()
            prev = datetime.now()
            while datetime.now() - starttime < dt.timedelta(seconds=exe_time_limit):
                sys.stdout.write(home)
                # ticking game objects
                for m in game_modules:
                    m.gameobj.tick()
                # producing frame
                testtris = [
                     triangle(vector3(0, 0.4, 0.1), vector3(-0.1, -0.15, 0.15), vector3(0.6, 0, -0.3)),
                     triangle(vector3(0.2, 0.4, 0.1), vector3(-0.2, 0, -0.1), vector3(0.35, -0.3, 0))
                     ]
                tris = loadmeshjson("weird_mesh.json")
                projectedtris = perspective_project(None, tris)
                rasterizeframe(projectedtris, tris)
                # printing frametime    
                sys.stdout.write(str((datetime.now() - prev)/dt.timedelta(milliseconds=1))+"ms\n")
                prev = datetime.now()
            sys.stdout.write(home)
    except FileNotFoundError:
        sys.stdout.write("Error: No game folder specified!\n")

if __name__ == "__main__":
    exit(main())
    # TESTING, DELETE LATER
#     quat1 = np.quaternion(0, 0, 1, 1)
#     quat1 = np.normalized(quat1)
#     print(quat1)
    #tri1 = tri2D(vec2D(0, 1), vec2D(-0.5, 0.), vec2D(0.5, 0.))
    #print(get_area(tri1))
    #print(get_point_in_tri2D(vec2D(0, 0), tri1))


    #canvas_size = vec2D(2., 2.)
    #step_x = canvas_size[0] / screensize[0]
    #step_y = canvas_size[1] / screensize[1]
    #testpoint = vec2D(step_x/2-canvas_size[0]/2, step_y/2-canvas_size[1]/2)
    #testpoint[0] += step_x*30
    #testpoint[1] += step_y*10
    #print(step_x)
    #print(step_y)
    #print(testpoint)
    #for i in range(screensize[0]):
    #    print(step_x*i)
    
    #mcross(vector3(1,0,0), vector3(0,2,0)).print()
    #mnormalized(vector3(4, 1, 0)).print()
#     testtris = [
#     triangle(vector3(0, 0.4, 0.1), vector3(-0.1, -0.15, 0.15), vector3(0.6, 0, -0.3)),
#     triangle(vector3(0.2, 0.4, 0.1), vector3(-0.2, 0, -0.1), vector3(0.35, -0.3, 0))
#     ]
#     rasterizeframe(testtris)
#     p1 = vector3(-3.09749, 0.61573, 2.01537)
#     p2 = vector3(-0.442901, -0.968565, 6.14963)
#     p_co = vector3(-1.26795, -1.05232, 3.1233)
#     p_n = vector3(0.427481, -1.60776, 2.27372)
#     line_plane_intersect(p1, p2, p_co, p_n).print()
#     v1 = vector3(-1.6118, 0.78488, 0.865926)
#     v2 = vector3(-0.761052, -0.066383, 1.05817)
#     project_vec3_vec3(v1, v2).print()
#     persp_tris = perspective_project(None, testtris)
#     print(testtris)
#     print(persp_tris)
#     v1 = vector3(-1.6, 0.78, 0.86)
#     v2 = vector3(-0.76, -0.06, 1.05)
#     mcross(v1, v2).print()
    #print(loadmeshjson("game1/cube_mesh.json"))