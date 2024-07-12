import random
import math
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
        print("%s%s" % (rgbcode(), line))
        
def randcolorframe():
    global screensize
    for i in range(screensize.height):
        line = ""
        for j in range(screensize.width):
            set_nprgb(rand255(),rand255(),rand255())
            line += rgbcode()+"A"
        print("%s" % (line))    

## MAIN ##
input()
print(home)
solidcolorframe(255,255,255)

input()
print(home)
solidcolorframe(0,0,0)

input()
print(home)
randcolorframe()

input()
