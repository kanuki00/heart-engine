import sys
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
    def __init__(self, in_a, in_b, in_c):
        self.a = in_a
        self.b = in_b
        self.c = in_c


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


# rendering
def rasterize(resolution, proj_tris, world_tris):
    res_buffer = [vec3(0, 0, 0)] * resolution.x * resolution.y
    for y in range(resolution.y):
        for x in range(resolution.x):
            tp_x = float(x) / float(resolution.x)
            tp_y = float(y) / float(resolution.y)
            tp = vec3(tp_x*2.0-1.0, tp_y*-2.0+1.0, 0.0)  # test point
            for t in range(len(proj_tris)):
                p_tri = proj_tris[t]
                if point_in_triangle(tp, p_tri):
                    res_buffer[y*resolution.x + x] = vec3(255, 255, 255)
    return res_buffer


def draw_frame_buffer(resolution, f_buffer):
    sys.stdout.write("\033[H")
    for y in range(resolution.y):
        for x in range(resolution.x):
            color = f_buffer[y*resolution.x + x]
            code_tail = ";".join([str(color.x), str(color.y), str(color.y)])+"m"
            fg_code = "\033[38;2;" + code_tail
            bg_code = "\033[48;2;" + code_tail
            sys.stdout.write(fg_code+bg_code+"A")
        sys.stdout.write("\033[0m\n")


def main():
    exe_time = 10
    render_resolution = vec3(100, 50, 0)
    frame_buffer = [vec3(0, 0, 0)] * render_resolution.x * render_resolution.y

    exe_time_start = timer()
    while timer()-exe_time_start < exe_time:
        time_start = timer()
        # rendering start
        proj_tris = [
            tri(vec3(0.0, 0.5, 0.0), vec3(-0.5, -0.5, 0.0), vec3(0.5, -0.5, 0.0)),
            tri(vec3(1.0, 0.5, 0.0), vec3(0.0, 0.5, 0.0), vec3(0.5, -0.5, 0.0))
        ]
        frame_buffer = rasterize(render_resolution, proj_tris, proj_tris)
        draw_frame_buffer(render_resolution, frame_buffer)
        # rendering end
        time_end = timer()
        sys.stdout.write(str((time_end - time_start) * 1000) + "ms\n")


if __name__ == "__main__":
    exit(main())
