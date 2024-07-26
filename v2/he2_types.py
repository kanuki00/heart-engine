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
    def __mul__(self, other):
        return vector3(self.x*other, self.y*other, self.z*other)
    def __truediv__(self, other):
        return vector3(self.x/other, self.y/other, self.z/other)
    def __add__(self, other):
        return vector3(self.x+other.x, self.y+other.y, self.z+other.z)
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
    def normal(self):
        ab = self.b - self.a
        ac = self.c - self.a
        return normalized(cross(ab, ac))
        
class boundbox:
    def __init__(self, in_a, in_b):
        self.a = in_a
        self.b = in_b
        
def cross(v1, v2):
    x = v1.y*v2.z-v1.z*v2.y
    y = v1.z*v2.x-v1.x*v2.z
    z = v1.x*v2.y-v1.y*v2.x
    return vector3(x, y, z)
    
def dot(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z
    
def normalized(v):
    return v/v.len()

def point_in_triangle(point, tri): # could we make this faster?
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
        
def barycoords(point, tri):
    u = triangle(point, tri.b, tri.c).get_area() / tri.get_area()
    v = triangle(point, tri.c, tri.a).get_area() / tri.get_area()
    w = triangle(point, tri.a, tri.b).get_area() / tri.get_area()
    return vector3(u, v, w)
        
def line_plane_intersect(line_start, line_end, plane_point, plane_normal):
    epsilon = 0.0001
    w = line_end - plane_point
    u = line_end - line_start
    dot1 = dot(u, plane_normal)
    dot2 = dot(plane_normal, w)
    if dot1 > -epsilon and dot1 < epsilon:
        return None
    f = dot2/dot1
    return (u*-f)+line_end
        
def safedivide(a, b):
    if b == 0:
        return a
    return a/b
    
def project_vec3_vec3(dest, source):
    d = dot(dest, source)
    f = d / dest.len()
    return normalized(dest)*f
    
def pp_helper(right, up, proj, plane_loc, ogvert, cam_loc):
    to_p = proj-plane_loc
    xdot = dot(right, proj)
    xsign = safedivide(xdot, abs(xdot))
    x = project_vec3_vec3(right, to_p).len()/right.len() * xsign
    ydot = dot(up, proj)
    ysign = safedivide(ydot, abs(ydot))
    y = project_vec3_vec3(up, to_p).len()/up.len() * ysign
    z = -((ogvert-cam_loc).len())
    return vector3(x, y, z)

def perspective_project(camera, triangles): #TODO camera
    cam_loc = vector3(2.8, -4.6, 2) # placeholder
    cam_plane_normal = vector3(-0.48878, 0.797416, -0.353874) # placeholder
    cam_plane_loc = cam_loc + cam_plane_normal * 4
    cam_right_vec = normalized(cross(cam_plane_normal, vector3(0,0,1)))
    cam_up_vec = cross(cam_right_vec, cam_plane_normal)
    result = []
    for tri in triangles:
        result_tri = triangle(vector3(0,0,0), vector3(0,0,0), vector3(0,0,0))
        proj_a = line_plane_intersect(tri.a, cam_loc, cam_plane_loc, cam_plane_normal)
        proj_b = line_plane_intersect(tri.b, cam_loc, cam_plane_loc, cam_plane_normal)
        proj_c = line_plane_intersect(tri.c, cam_loc, cam_plane_loc, cam_plane_normal)
        result_tri.a = pp_helper(cam_right_vec, cam_up_vec, proj_a, cam_plane_loc, tri.a, cam_loc)
        result_tri.b = pp_helper(cam_right_vec, cam_up_vec, proj_b, cam_plane_loc, tri.b, cam_loc)
        result_tri.c = pp_helper(cam_right_vec, cam_up_vec, proj_c, cam_plane_loc, tri.c, cam_loc)
        result.append(result_tri)
    return result