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

    def print(self):
        sys.stdout.write("[%f, %f, %f]" % (self.x, self.y, self.z))


class vec4:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0
    def __init__(self, in_x, in_y, in_z, in_w):
        self.x = in_x
        self.y = in_y
        self.z = in_z
        self.w = in_w

class tri:
    def __init__(self, in_a, in_b, in_c):
        self.a = in_a
        self.b = in_b
        self.c = in_c

    def no_z(self):
        nza = vec3(self.a.x, self.a.y, 0.0)
        nzb = vec3(self.b.x, self.b.y, 0.0)
        nzc = vec3(self.c.x, self.c.y, 0.0)
        return tri(nza, nzb, nzc)


def empty_tri():
    return tri(vec3(0, 0, 0), vec3(0, 0, 0), vec3(0, 0, 0))


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


def get_tri_normal(t: tri):
    normal: vec3 = cross(t.b-t.a, t.c-t.a)
    return normal / vec3_len(normal)


def vec3_to_rgb(v: vec3):
    r: float = v.x * 255.0
    g: float = v.y * 255.0
    b: float = v.z * 255.0
    r = max(0.0, r)
    g = max(0.0, g)
    b = max(0.0, b)
    return vec3(int(r), int(g), int(b))


def initialize_matrix(size: int) -> list[list[float]]:
    result = []
    for r in range(size):
        row = []
        for c in range(size):
            row.append(0.0)
        result.append(row)
    return result

def cofactor(A, temp, p, q, n):

    i = 0
    j = 0

    # Looping for each element of the matrix
    for row in range(n):

        for col in range(n):

            # Copying into temporary matrix only those element
            # which are not in given row and column
            if row != p and col != q:

                temp[i][j] = A[row][col]
                j += 1

                # Row is filled, so increase row index and
                # reset col index
                if j == n - 1:
                    j = 0
                    i += 1


# Recursive function for finding determinant of matrix.
#  n is current dimension of A[][].
def determinant(in_matrix, n):
    # Initialize result
    det = 0

    # Base case : if matrix contains single element
    if n == 1:
        return in_matrix[0][0]

    # To store cofactors
    temp = initialize_matrix(4)

    # To store sign multiplier
    sign = 1

    # Iterate for each element of first row
    for f in range(n):

        # Getting Cofactor of A[0][f]
        cofactor(in_matrix, temp, 0, f, n)
        det += sign * in_matrix[0][f] * determinant(temp, n - 1)

        # terms are to be added with alternate sign
        sign = -sign

    return det


# Function to get adjoint of A[N][N] in adj[N][N].
def adjoint(in_matrix, adj):

    # if N == 1:
    #     adj[0][0] = 1
    #     return

    # temp is used to store cofactors of A[][]
    temp = initialize_matrix(4)

    for i in range(4):
        for j in range(4):
            # Get cofactor of A[i][j]
            cofactor(in_matrix, temp, i, j, 4)

            # sign of adj[j][i] positive if sum of row
            # and column indexes is even.
            sign = [1, -1][(i + j) % 2]

            # Interchanging rows and columns to get the
            # transpose of the cofactor matrix
            adj[j][i] = (sign)*(determinant(temp, 4-1))


# Function to calculate and store inverse, returns false if
# matrix is singular
def inverse(in_matrix):

    result = initialize_matrix(4)
    # Find determinant of A[][]
    det = determinant(in_matrix, 4)
    if det == 0:
        print("Singular matrix, can't find its inverse")
        return result

    # Find adjoint
    adj = []
    for i in range(4):
        adj.append([0 for _ in range(4)])
    adjoint(in_matrix, adj)

    # Find Inverse using formula "inverse(A) = adj(A)/det(A)"
    for i in range(4):
        for j in range(4):
            result[i][j] = adj[i][j] / det

    return result


def rotate(v: vec3, q: vec4):
    r = vec3(q.x, q.y, q.z)
    s = q.w
    m = math.pow(q.x, 2) + math.pow(q.y, 2) + math.pow(q.z, 2) + math.pow(q.w, 2)
    return v + cross(r * 2, (v * s + cross(r, v)) / m)


def create_transform_matrix(in_translation: vec3, in_rotation: vec4, in_scale: vec3):
    i_hat: vec3 = rotate(vec3(1.0, 0.0, 0.0), in_rotation)
    j_hat: vec3 = rotate(vec3(0.0, 1.0, 0.0), in_rotation)
    k_hat: vec3 = rotate(vec3(0.0, 0.0, 1.0), in_rotation)
    result_matrix = initialize_matrix(4)
    result_matrix[0] = [i_hat.x, j_hat.x, k_hat.x, in_translation.x]
    result_matrix[1] = [i_hat.y, j_hat.y, k_hat.y, in_translation.y]
    result_matrix[2] = [i_hat.z, j_hat.z, k_hat.z, in_translation.z]
    result_matrix[3] = [0.0, 0.0, 0.0, 1.0]
    return result_matrix


def transform_vector(v: vec3, in_matrix: list[list[float]]):
    i_hat: vec3 = vec3(in_matrix[0][0], in_matrix[1][0], in_matrix[2][0])
    j_hat: vec3 = vec3(in_matrix[0][1], in_matrix[1][1], in_matrix[2][1])
    k_hat: vec3 = vec3(in_matrix[0][2], in_matrix[1][2], in_matrix[2][2])
    t: vec3 = vec3(in_matrix[0][3], in_matrix[1][3], in_matrix[2][3])
    return i_hat*v.x + j_hat*v.y + k_hat*v.z + t


def perspective_project(v: vec3):
    px = v.x / -v.z
    py = v.y / -v.z
    return vec3(px, py, v.z)


# rendering
def load_mesh(path):
    with open(path, "r") as file:
        data = json.load(file)
        tricount: int = len(data["indices"])
        triangles = []
        for i in range(tricount):
            from_data: tri = empty_tri()
            idx_a: int = data["indices"][i][0]
            from_data.a = vec3(
                data["vertices"][idx_a][0],
                data["vertices"][idx_a][1],
                data["vertices"][idx_a][2])
            idx_b: int = data["indices"][i][1]
            from_data.b = vec3(
                data["vertices"][idx_b][0],
                data["vertices"][idx_b][1],
                data["vertices"][idx_b][2])
            idx_c: int = data["indices"][i][2]
            from_data.c = vec3(
                data["vertices"][idx_c][0],
                data["vertices"][idx_c][1],
                data["vertices"][idx_c][2])
            triangles.append(from_data)
        return triangles


def rasterize(resolution, proj_tris, world_tris):
    res_buffer = [vec3(0, 0, 0)] * resolution.x * resolution.y
    for y in range(resolution.y):
        for x in range(resolution.x):
            tp_x = float(x) / float(resolution.x)
            tp_y = float(y) / float(resolution.y)
            tp = vec3(tp_x * 2.0 - 1.0, tp_y * -2.0 + 1.0, 0.0)  # test point
            shallowest = -1000000000.0
            for t in range(len(proj_tris)):
                p_tri: tri = proj_tris[t]
                if point_in_triangle(tp, p_tri):
                    p_tri_2d = p_tri.no_z()
                    bc = get_bc_coords(tp, p_tri_2d)
                    fragment_depth = p_tri.a.z*bc.x + p_tri.b.z*bc.y + p_tri.c.z*bc.z
                    if fragment_depth > shallowest:
                        shallowest = fragment_depth
                        ws_tri: tri = world_tris[t]
                        color = vec3_to_rgb(get_tri_normal(ws_tri))
                        res_buffer[y * resolution.x + x] = color
    return res_buffer


def draw_frame_buffer(resolution, f_buffer):
    sys.stdout.write("\033[H")
    for y in range(resolution.y):
        for x in range(resolution.x):
            color = f_buffer[y * resolution.x + x]
            code_tail = ";".join([str(color.x), str(color.y), str(color.z)]) + "m"
            fg_code = "\033[38;2;" + code_tail
            bg_code = "\033[48;2;" + code_tail
            sys.stdout.write(fg_code + bg_code + "A")
        sys.stdout.write("\033[0m\n")


def main():
    exe_time = 10
    render_resolution = vec3(100, 50, 0)
    frame_buffer = [vec3(0, 0, 0)] * render_resolution.x * render_resolution.y
    ws_tris = load_mesh("test_mesh2.json")
    exe_time_start = timer()
    while timer() - exe_time_start < exe_time:
        time_start = timer()
        # rendering start
        c_transf = create_transform_matrix(vec3(3.3353, -2.4, 3.7), vec4(0.385971, 0.198576, 0.412145, 0.801081), vec3(1.0, 1.0, 1.0))
        cs_tris = []
        cs_zoom_m = [
            [5.0, 0.0, 0.0, 0.0],
            [0.0, 5.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]
        for t in ws_tris:
            pa = transform_vector(t.a, inverse(c_transf))
            pa = perspective_project(pa)
            pa = transform_vector(pa, cs_zoom_m)

            pb = transform_vector(t.b, inverse(c_transf))
            pb = perspective_project(pb)
            pb = transform_vector(pb, cs_zoom_m)

            pc = transform_vector(t.c, inverse(c_transf))
            pc = perspective_project(pc)
            pc = transform_vector(pc, cs_zoom_m)

            cs_tris.append(tri(pa, pb, pc))

        frame_buffer = rasterize(render_resolution, cs_tris, ws_tris)
        draw_frame_buffer(render_resolution, frame_buffer)
        # rendering end
        time_end = timer()
        sys.stdout.write(str((time_end - time_start) * 1000) + "ms\n")


if __name__ == "__main__":
    exit(main())
