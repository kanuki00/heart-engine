import math
import sys


class vector4:
    x = 0.0
    y = 0.0
    z = 0.0
    w = 0.0

    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, other):
        return vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __mul__(self, other):
        return vector4(self.x * other, self.y * other, self.z * other, self.w * other)

    def comp_by_idx(self, i):
        match i:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.z
            case 3:
                return self.w

    def print(self):
        sys.stdout.write("[%f %f %f %f]\n" % (self.x, self.y, self.z, self.w))


class matrix4x4:
    #             I    J     K     T
    r1 = vector4(1, 0, 0, 0)
    r2 = vector4(0, 1, 0, 0)
    r3 = vector4(0, 0, 1, 0)
    r4 = vector4(0, 0, 0, 1)

    def __init__(self):
        pass

    def print(self):
        sys.stdout.write(
            "[%f %f %f %f]\n" % (self.r1.x, self.r1.y, self.r1.z, self.r1.w) +
            "[%f %f %f %f]\n" % (self.r2.x, self.r2.y, self.r2.z, self.r2.w) +
            "[%f %f %f %f]\n" % (self.r3.x, self.r3.y, self.r3.z, self.r3.w) +
            "[%f %f %f %f]\n" % (self.r4.x, self.r4.y, self.r4.z, self.r4.w) +
            "\n"
        )


class vector8:
    x = 0.0
    y = 0.0
    z = 0.0
    w = 0.0

    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0

    def __init__(self, x, y, z, w, a, b, c, d):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __add__(self, other):
        return vector8(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w, self.a + other.a, self.b + other.b, self.c + other.c, self.d + other.d)

    def __mul__(self, other):
        return vector8(self.x * other, self.y * other, self.z * other, self.w * other, self.a * other, self.b * other, self.c * other, self.d * other)

    def comp_by_idx(self, i):
        match i:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.z
            case 3:
                return self.w

    def get_left_side(self):
        return vector4(self.x, self.y, self.z, self.w)

    def print(self):
        sys.stdout.write("[%f %f %f %f | %f %f %f %f]\n" % (self.x, self.y, self.z, self.w, self.a, self.b, self.c, self.d))


class matrix4x8:
    # [1 0 0 0 | 1 0 0 0]
    # [0 1 0 0 | 0 1 0 0]
    # [0 0 1 0 | 0 0 1 0]
    # [0 0 0 1 | 0 0 0 1]

    r1 = vector8(1, 0, 0, 0, 1, 0, 0, 0)
    r2 = vector8(0, 1, 0, 0, 0, 1, 0, 0)
    r3 = vector8(0, 0, 1, 0, 0, 0, 1, 0)
    r4 = vector8(0, 0, 0, 1, 0, 0, 0, 1)

    # initializing with two 4x4 matrices
    def __init__(self, left, right):
        self.r1 = vector8(left.r1.x, left.r1.y, left.r1.z, left.r1.w, right.r1.x, right.r1.y, right.r1.z, right.r1.w)
        self.r2 = vector8(left.r2.x, left.r2.y, left.r2.z, left.r2.w, right.r2.x, right.r2.y, right.r2.z, right.r2.w)
        self.r3 = vector8(left.r3.x, left.r3.y, left.r3.z, left.r3.w, right.r3.x, right.r3.y, right.r3.z, right.r3.w)
        self.r4 = vector8(left.r4.x, left.r4.y, left.r4.z, left.r4.w, right.r4.x, right.r4.y, right.r4.z, right.r4.w)

    def get_row_by_index(self, index):
        match index:
            case 0:
                return self.r1
            case 1:
                return self.r2
            case 2:
                return self.r3
            case 3:
                return self.r4

    def set_row_by_idx(self, index, new_row_value):
        match index:
            case 0:
                self.r1 = new_row_value
                return
            case 1:
                self.r2 = new_row_value
                return
            case 2:
                self.r3 = new_row_value
                return
            case 3:
                self.r4 = new_row_value
                return

    def print(self):
        sys.stdout.write(
            "[%f %f %f %f | %f %f %f %f]\n" % (self.r1.x, self.r1.y, self.r1.z, self.r1.w, self.r1.a, self.r1.b, self.r1.c, self.r1.d) +
            "[%f %f %f %f | %f %f %f %f]\n" % (self.r2.x, self.r2.y, self.r2.z, self.r2.w, self.r2.a, self.r2.b, self.r2.c, self.r2.d) +
            "[%f %f %f %f | %f %f %f %f]\n" % (self.r3.x, self.r3.y, self.r3.z, self.r3.w, self.r3.a, self.r3.b, self.r3.c, self.r3.d) +
            "[%f %f %f %f | %f %f %f %f]\n" % (self.r4.x, self.r4.y, self.r4.z, self.r4.w, self.r4.a, self.r4.b, self.r4.c, self.r4.d)
        )

    def get_right_side(self):
        result = matrix4x4()
        result.r1 = vector4(self.r1.a, self.r1.b, self.r1.c, self.r1.d)
        result.r2 = vector4(self.r2.a, self.r2.b, self.r2.c, self.r2.d)
        result.r3 = vector4(self.r3.a, self.r3.b, self.r3.c, self.r3.d)
        result.r4 = vector4(self.r4.a, self.r4.b, self.r4.c, self.r4.d)
        return result


def get_msr_cands(exclude, in_mat4x8):
    all_rows = [
        in_mat4x8.r1,
        in_mat4x8.r2,
        in_mat4x8.r3,
        in_mat4x8.r4
    ]
    result = []
    for i in range(len(all_rows)):
        if i != exclude:
            result.append(all_rows[i])
    return result


def dot(v1: vector4, v2: vector4):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z + v1.w * v2.w


def length_v4(v: vector4):
    return math.sqrt(dot(v, v))


# Gauss Jordan Elimination Method
def invert_mat4x4(in_mat4x4):
    table = matrix4x8(in_mat4x4, matrix4x4())
    #sys.stdout.write("Origin\n")
    #table.print()
    #sys.stdout.write("\n")

    # Reduction order A to P
    #    x0 y1 z2 w3
    # r0 [M  L  J  I]
    # r1 [A  N  K  H]
    # r2 [B  E  O  G]
    # r3 [C  D  F  P]
    tar_row_idxs = [
        1, 2, 3, 3, 2, 3,
        2, 1, 0, 0, 1, 0
    ]
    tar_row_comp_idxs = [
        0, 0, 0, 1, 1, 2,
        3, 3, 3, 2, 2, 1
    ]
    for i in range(12):
        target = table.get_row_by_index(tar_row_idxs[i]).comp_by_idx(tar_row_comp_idxs[i])
        if target != 0:
            msr_cands = get_msr_cands(tar_row_idxs[i], table)  # multiplier source row candidates
            mult = 1
            add_cand = vector8(0, 0, 0, 1, 0, 0, 0, 1)
            shortest_len = 1000000000.0
            for c in msr_cands:
                cand_comp = c.comp_by_idx(tar_row_comp_idxs[i])
                if cand_comp != 0:
                    c_len = length_v4(c.get_left_side())
                    if c_len < shortest_len:
                        shortest_len = c_len
                        mult = -target / cand_comp
                        add_cand = c
            to_add = add_cand*mult
            row_result = table.get_row_by_index(tar_row_idxs[i]) + to_add
            table.set_row_by_idx(tar_row_idxs[i], row_result)

            #sys.stdout.write("Pass %d. Row %d, Column %d\n" % (i+1, tar_row_idxs[i]+1, tar_row_comp_idxs[i]+1))
            #table.print()
            #sys.stdout.write("What was added to target's row\n")
            #to_add.print()
            #sys.stdout.write("\n")

    return table.get_right_side()


m = matrix4x4()
m.r1 = vector4(1, 2, -1, 5)
m.r2 = vector4(2, 5, 1, 2)
m.r3 = vector4(-1, -2, 2, -7)
m.r4 = vector4(0, 0, 0, 1)
m.print()

m_i = invert_mat4x4(m)
m_i.print()
