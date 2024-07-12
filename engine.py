import sys
import random
import math
import datetime as dt
from datetime import datetime
import json

# Konsole complete zoom out perfect square is 4x7

## CLASSES
class rgb:
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0

class res:
    def __init__(self, w, h):
        self.width = w
        self.height = h

## GLOBAL VARS ##
nprgb = rgb()
home = "\033[H"
screensize = res(60, 20)
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
    for i in range(screensize.height):
        line = ""
        for j in range(screensize.width):
            set_nprgb(rand255(),rand255(),rand255())
            line += rgbcode()+"A"
        sys.stdout.write("%s\n" % (line))    

## MAIN ##
def main():
    global game_modules
    args = sys.argv[1:]
    with open(args[0]+"/world1.json") as worldfile:
        wdata = json.load(worldfile)
        for obj in wdata["content"]:
            if obj["code"] != None:
                path = args[0]+"."+obj["code"]
                game_modules.append(__import__(path, globals(), locals(), [obj["code"]], 0))
            
        starttime = datetime.now()
        while datetime.now() - starttime < dt.timedelta(seconds=exe_time_limit):
            sys.stdout.write(home)
            randcolorframe()
            for m in game_modules:
                m.gameobj.tick()
        sys.stdout.write(home)

if __name__ == "__main__":
    exit(main())
