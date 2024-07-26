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


class quaternion:
    def __init__(self, in_x, in_y, in_z, in_w):
        self.x = in_x
        self.y = in_y
        self.z = in_z
        self.w = in_w

    def __mul__(self, other):
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return quaternion(x, y, z, w)
    def __truediv__(self, other):
        x = self.x/other
        y = self.y/other
        z = self.z/other
        w = self.w/other
        return quaternion(x, y, z, w)


class triangle:
    normal = vector3(0, 0, 0)

    def __init__(self, in_a, in_b, in_c):
        self.a = in_a
        self.b = in_b
        self.c = in_c

    def compute_normal(self):
        ab = self.b - self.a
        ac = self.c - self.a
        return normalized(cross(ab, ac))

    def to_string(self):
        return "Triangle\nA: Vector3 %s\nB: Vector3 %s\nC: Vector3 %s" % (
            self.a.to_string(), self.b.to_string(), self.c.to_string())


class camera:
    def __init__(self, in_loc, in_rot):
        self.loc = in_loc
        self.rot = in_rot

    def forward_vec(self):
        return rotate(vector3(0, 0, -1), normalized(self.rot))

    def up_vec(self):
        return rotate(vector3(0, 1, 0), normalized(self.rot))

    def right_vec(self):
        return rotate(vector3(1, 0, 0), normalized(self.rot))


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
    if isinstance(v1, vector3) and isinstance(v2, vector3):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
    if isinstance(v1, quaternion) and isinstance(v2, quaternion):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z + v1.w * v2.w


def vector_length(v):
    return math.sqrt(dot(v, v))


def normalized(v):
    return v / vector_length(v)


def rotate(v, q):
    r = vector3(q.x, q.y, q.z)
    s = q.w
    m = math.pow(q.x, 2) + math.pow(q.y, 2) + math.pow(q.z, 2) + math.pow(q.w, 2)
    return v + cross(r * 2, (v * s + cross(r, v)) / m)


def rotate_tri(tri, q):
    a = rotate(tri.a, q)
    b = rotate(tri.b, q)
    c = rotate(tri.c, q)
    return triangle(a, b, c)


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
        return vector3(0.333, 0.333, 0.334)
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


def perspective_project_v1(camera, triangles):  # TODO camera
    cam_plane_normal = camera.forward_vec()
    cam_plane_loc = camera.loc + cam_plane_normal * 4
    cam_right_vec = camera.right_vec()
    cam_up_vec = camera.up_vec()
    result = []
    for tri in triangles:
        result_tri = triangle(vector3(0, 0, 0), vector3(0, 0, 0), vector3(0, 0, 0))
        proj_a = line_plane_intersect(tri.a, camera.loc, cam_plane_loc, cam_plane_normal)
        proj_b = line_plane_intersect(tri.b, camera.loc, cam_plane_loc, cam_plane_normal)
        proj_c = line_plane_intersect(tri.c, camera.loc, cam_plane_loc, cam_plane_normal)
        result_tri.a = pp_helper(cam_right_vec, cam_up_vec, proj_a, cam_plane_loc, tri.a, camera.loc)
        result_tri.b = pp_helper(cam_right_vec, cam_up_vec, proj_b, cam_plane_loc, tri.b, camera.loc)
        result_tri.c = pp_helper(cam_right_vec, cam_up_vec, proj_c, cam_plane_loc, tri.c, camera.loc)
        result.append(result_tri)
    return result


def perspective_project_v2(camera, triangles):  # TODO
    result = []
    for tri in triangles:
        tri_vert_list = [tri.a, tri.b, tri.c]
        rtvl = []
        for vert in tri_vert_list:
            # do projections
            proj_vert = vert
            rtvl.append(proj_vert)
        result.append(triangle(rtvl[0], rtvl[1], rtvl[2]))
    return result
