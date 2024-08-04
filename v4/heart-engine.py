import json
import sys
import random
import math
from timeit import default_timer as timer


# types
class vec3:
    def __init__(self, in_x, in_y, in_z):
        self.x = in_x
        self.y = in_y
        self.z = in_z

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return vec3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return vec3(self.x / other, self.y / other, self.z / other)


class tri:
    col = vec3(255, 0, 0)

    def __init__(self, in_a, in_b, in_c):
        self.a = in_a
        self.b = in_b
        self.c = in_c

    def no_z(self):
        nza = vec3(self.a.x, self.a.y, 0.0)
        nzb = vec3(self.b.x, self.b.y, 0.0)
        nzc = vec3(self.c.x, self.c.y, 0.0)
        return tri(nza, nzb, nzc)


# math
def edge_func(in_a, in_b, in_p):
    side = (in_p.x - in_a.x) * (in_b.y - in_a.y) - (in_p.y - in_a.y) * (in_b.x - in_a.x)
    return side <= 0


def point_in_triangle(p, in_tri):
    if not edge_func(in_tri.a, in_tri.b, p):
        return False
    if not edge_func(in_tri.b, in_tri.c, p):
        return False
    if not edge_func(in_tri.c, in_tri.a, p):
        return False
    return True


def cross(v1, v2):
    x = v1.y * v2.z - v1.z * v2.y
    y = v1.z * v2.x - v1.x * v2.z
    z = v1.x * v2.y - v1.y * v2.x
    return vec3(x, y, z)


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def vec3_len(v):
    return math.sqrt(dot(v, v))


def get_bc_coords(p, t):
    t_para_area = vec3_len(cross(t.b - t.a, t.c - t.a))
    w_area = vec3_len(cross(t.b - t.a, p - t.a))
    u_area = vec3_len(cross(t.c - t.b, p - t.b))
    v_area = vec3_len(cross(t.a - t.c, p - t.c))
    return vec3(u_area / t_para_area, v_area / t_para_area, w_area / t_para_area)


# rendering
def load_mesh(path):
    with open(path, "r") as file:
        result = []
        data = json.load(file)
        for ind in data["indices"]:
            data_a = data["vertices"][ind[0]]
            data_b = data["vertices"][ind[1]]
            data_c = data["vertices"][ind[2]]
            a = vec3(data_a[0], data_a[1], data_a[2])
            b = vec3(data_b[0], data_b[1], data_b[2])
            c = vec3(data_c[0], data_c[1], data_c[2])
            result.append(tri(a, b, c))
        return result


def rasterize(resolution, proj_tris, world_tris):
    res_buffer = [vec3(0, 0, 0)] * resolution.x * resolution.y
    for y in range(resolution.y):
        for x in range(resolution.x):
            tp_x = float(x) / float(resolution.x)
            tp_y = float(y) / float(resolution.y)
            tp = vec3(tp_x * 2.0 - 1.0, tp_y * -2.0 + 1.0, 0.0)  # test point
            shallowest = -1000000000.0
            for t in range(len(proj_tris)):
                p_tri = proj_tris[t]
                if point_in_triangle(tp, p_tri):
                    p_tri_2d = p_tri.no_z()
                    bc = get_bc_coords(tp, p_tri_2d)
                    fragment_depth = p_tri.a.z*bc.x + p_tri.b.z*bc.y + p_tri.c.z*bc.z
                    if fragment_depth > shallowest:
                        shallowest = fragment_depth
                        res_buffer[y * resolution.x + x] = p_tri.col
    return res_buffer


def draw_frame_buffer(resolution, f_buffer):
    sys.stdout.write("\033[H")
    for y in range(resolution.y):
        for x in range(resolution.x):
            color = f_buffer[y * resolution.x + x]
            code_tail = ";".join([str(color.x), str(color.y), str(color.y)]) + "m"
            fg_code = "\033[38;2;" + code_tail
            bg_code = "\033[48;2;" + code_tail
            sys.stdout.write(fg_code + bg_code + "A")
        sys.stdout.write("\033[0m\n")


def main():
    exe_time = 10
    render_resolution = vec3(100, 50, 0)
    frame_buffer = [vec3(0, 0, 0)] * render_resolution.x * render_resolution.y
    tris = load_mesh("test_mesh2.json")
    for t in tris:
        t.col = vec3(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    exe_time_start = timer()
    while timer() - exe_time_start < exe_time:
        time_start = timer()
        # rendering start
        #proj_tris = [
        #    tri(vec3(0.0, 0.5, 0.0), vec3(-0.5, -0.5, 0.0), vec3(0.5, -0.5, 0.0)),
        #    tri(vec3(1.0, 0.5, 0.0), vec3(0.0, 0.5, 0.0), vec3(0.5, -0.5, 0.0))
        #]
        frame_buffer = rasterize(render_resolution, tris, tris)
        draw_frame_buffer(render_resolution, frame_buffer)
        # rendering end
        time_end = timer()
        sys.stdout.write(str((time_end - time_start) * 1000) + "ms\n")


if __name__ == "__main__":
    exit(main())
