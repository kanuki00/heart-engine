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
        self.transform = None
        
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
        raise Exceptrion("v is not a vector3")
    npa = v.asnp()
    return np.linalg.norm(npa, ord=1)

## GLOBAL VARS ##
nprgb = rgb()
home = "\033[H"
screensize = vec2D(60, 20)
exe_time_limit = 10
game_modules = []

## FUNCS ##
def set_nprgb(new_r, new_g, new_b):
    global nprgb
    nprgb.r = new_r
    nprgb.g = new_g
    nprgb.b = new_b

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
    
def rasterizeframe(triangles):
    global screensize
    sys.stdout.write(home)
    canvas_size = vec2D(2., 2.)
    step_x = canvas_size[0] / screensize[0]
    step_y = canvas_size[1] / screensize[1]
    for i in reversed(range(screensize[1])): # screensize Y
        for j in range(screensize[0]): # screensize X
            x = step_x*j-canvas_size[0]/2
            y = step_y*i-canvas_size[1]/2
            depth = 0 # TODO
            normal = vector3 # TODO
            for k in triangles:
                if get_point_in_tri2D(vector3(x, y, 0), k):
                    set_nprgb(255, 255, 255)
                    break
                else:
                    set_nprgb(0, 0, 0)
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

# def get_area(tri):
#     ab = tri.b-tri.a
#     ac = tri.c-tri.a
#     cross = np.cross(ab, ac)
#     return abs(cross/2)
    
def get_point_in_tri2D(point, tri):
    tri_a = triangle(point, tri.a, tri.b)
    tri_b = triangle(point, tri.b, tri.c)
    tri_c = triangle(point, tri.c, tri.a)
    comboarea = tri_a.area2D() + tri_b.area2D() + tri_c.area2D()
    diff = tri.area2D() - comboarea
    tol = 0.0001
    if diff > -tol and diff < tol:
        return True
    else:
        return False

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
                rasterizeframe([triangle(vector3(0, 0.8, 0), vector3(-0.5, -0.2, 0), vector3(0.5, -0.2, 0)), triangle(vector3(-0.9, 0.2, 0), vector3(-1, -0.2, 0), vector3(-0.8, -0.2, 0))])
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