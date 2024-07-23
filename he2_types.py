import math

class vector2:
    def __init__(self, in_x, in_y):
        self.x = in_x
        self.y = in_y

class vector3:
    def __init__(self, in_x, in_y, in_z):
        self.x = in_x
        self.y = in_y
        self.z = in_z
    def __sub__(self, other):
        x = self.x-other.x
        y = self.y-other.y
        z = self.z-other.z
        return vector3(x, y, z)
    def len(self):
        return math.sqrt(dot(self, self))
    def to_string(self):
        return "x: %f, y: %f, z: %f" % (self.x, self.y, self.z)
        
class triangle:
    def __init__(self, in_a, in_b, in_c):
        self.a = in_a
        self.b = in_b
        self.c = in_c
    def omit_z(self):
        oza = vector3(self.a.x, self.a.y, 0)
        ozb = vector3(self.b.x, self.b.y, 0)
        ozc = vector3(self.c.x, self.c.y, 0)
        return triangle(oza, ozb, ozc)
    def get_area(self):
        ab = self.b-self.a
        ac = self.c-self.a
        c = cross(ab, ac)
        return abs(c.len()*0.5)
        
def cross(v1, v2):
    x = v1.y*v2.z-v1.z*v2.y
    y = v1.z*v2.x-v1.x*v2.z
    z = v1.x*v2.y-v1.y*v2.x
    return vector3(x, y, z)
    
def dot(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

def point_in_triangle(point, tri):
    tri_a = triangle(point, tri.a, tri.b)
    tri_b = triangle(point, tri.b, tri.c)
    tri_c = triangle(point, tri.c, tri.a)
    comboarea = tri_a.get_area() + tri_b.get_area() + tri_c.get_area()
    diff = tri.get_area() - comboarea
    epsilon = 0.0001
    if diff > -epsilon and diff < epsilon:
        return True
    else:
        return False