import math


class vector3:
    def __init__(self, in_x, in_y, in_z):
        self.x = in_x
        self.y = in_y
        self.z = in_z

    def __add__(self, other):
        return vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return vector3(self.x / other, self.y / other, self.z / other)

    def to_string(self):
        return "x: %f, y: %f, z: %f" % (self.x, self.y, self.z)


class triangle:
    normal = vector3(0, 0, 0)

    def __init__(self, in_a, in_b, in_c):
        self.a = in_a
        self.b = in_b
        self.c = in_c

    def compute_normal(self):
        ab = self.b - self.a
        ac = self.c - self.a
        self.normal = normalized(cross(ab, ac))
        return self.normal

    def to_string(self):
        return "Triangle\nA: Vector3 %s\nB: Vector3 %s\nC: Vector3 %s" % (
            self.a.to_string(), self.b.to_string(), self.c.to_string())


class bounds:
    def __init__(self, in_a, in_b):
        self.a = in_a
        self.b = in_b


def cross(v1, v2):
    x = v1.y * v2.z - v1.z * v2.y
    y = v1.z * v2.x - v1.x * v2.z
    z = v1.x * v2.y - v1.y * v2.x
    return vector3(x, y, z)


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def vector_length(v):
    return math.sqrt(dot(v, v))


def normalized(v):
    return v / vector_length(v)

def vec3_to_rgb(v):
    r = max(v.x * 255, 0)
    g = max(v.y * 255, 0)
    b = max(v.z * 255, 0)
    return vector3(r, g, b)

def bary_coords(point, tri):
    try:
        u = tri_area_fast(triangle(point, tri.b, tri.c)) / tri_area_fast(tri)
        v = tri_area_fast(triangle(point, tri.c, tri.a)) / tri_area_fast(tri)
        w = tri_area_fast(triangle(point, tri.a, tri.b)) / tri_area_fast(tri)
    except ZeroDivisionError:
        return vector3(0.333, 0.333, 0.333)
    return vector3(u, v, w)


def triangle_omit_z(tri):
    a = vector3(tri.a.x, tri.a.y, 0)
    b = vector3(tri.b.x, tri.b.y, 0)
    c = vector3(tri.c.x, tri.c.y, 0)
    return triangle(a, b, c)


def triangle_area(tri):
    ab = tri.b - tri.a
    ac = tri.c - tri.a
    c = cross(ab, ac)
    return abs(vector_length(c) * 0.5)


def tri_area_fast(tri):
    ab = tri.b - tri.a
    ac = tri.c - tri.a
    return abs(vector_length(cross(ab, ac)))


def point_in_triangle_v1(point, tri):
    tri_a = triangle(point, tri.a, tri.b)
    tri_b = triangle(point, tri.b, tri.c)
    tri_c = triangle(point, tri.c, tri.a)
    comboarea = triangle_area(tri_a) + triangle_area(tri_b) + triangle_area(tri_c)
    diff = triangle_area(tri) - comboarea
    epsilon = 0.0001
    if -epsilon < diff < epsilon:
        return True
    else:
        return False


def edgefunc(in_a, in_b, in_p):
    side = (in_p.x - in_a.x) * (in_b.y - in_a.y) - (in_p.y - in_a.y) * (in_b.x - in_a.x)
    return side <= 0


def point_in_triangle_v2(point, tri):
    if not edgefunc(tri.a, tri.b, point):
        return False
    if not edgefunc(tri.b, tri.c, point):
        return False
    if not edgefunc(tri.c, tri.a, point):
        return False
    return True


def line_plane_intersect(line_start, line_end, plane_point, plane_normal):
    epsilon = 0.0001
    w = line_end - plane_point
    u = line_end - line_start
    dot1 = dot(u, plane_normal)
    dot2 = dot(plane_normal, w)
    if -epsilon < dot1 < epsilon:
        return None
    f = dot2 / dot1
    return (u * -f) + line_end


def safedivide(a, b):
    if b == 0:
        return a
    return a / b


def project_vec3_vec3(dest, source):
    d = dot(dest, source)
    f = d / vector_length(dest)
    return normalized(dest) * f


def pp_helper(right, up, proj, plane_loc, ogvert, cam_loc):
    to_p = proj - plane_loc
    xdot = dot(right, proj)
    xsign = safedivide(xdot, abs(xdot))
    x = vector_length(project_vec3_vec3(right, to_p)) / vector_length(right) * xsign
    ydot = dot(up, proj)
    ysign = safedivide(ydot, abs(ydot))
    y = vector_length(project_vec3_vec3(up, to_p)) / vector_length(up) * ysign
    z = -(vector_length(ogvert - cam_loc))
    return vector3(x, y, z)


def perspective_project(camera, triangles):  # TODO camera
    cam_loc = vector3(2.8, -4.6, 2)  # placeholder
    cam_plane_normal = vector3(-0.48878, 0.797416, -0.353874)  # placeholder
    cam_plane_loc = cam_loc + cam_plane_normal * 4
    cam_right_vec = normalized(cross(cam_plane_normal, vector3(0, 0, 1)))
    cam_up_vec = cross(cam_right_vec, cam_plane_normal)
    result = []
    for tri in triangles:
        result_tri = triangle(vector3(0, 0, 0), vector3(0, 0, 0), vector3(0, 0, 0))
        proj_a = line_plane_intersect(tri.a, cam_loc, cam_plane_loc, cam_plane_normal)
        proj_b = line_plane_intersect(tri.b, cam_loc, cam_plane_loc, cam_plane_normal)
        proj_c = line_plane_intersect(tri.c, cam_loc, cam_plane_loc, cam_plane_normal)
        result_tri.a = pp_helper(cam_right_vec, cam_up_vec, proj_a, cam_plane_loc, tri.a, cam_loc)
        result_tri.b = pp_helper(cam_right_vec, cam_up_vec, proj_b, cam_plane_loc, tri.b, cam_loc)
        result_tri.c = pp_helper(cam_right_vec, cam_up_vec, proj_c, cam_plane_loc, tri.c, cam_loc)
        result.append(result_tri)
    return result
