import sys


class vector3:
    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        return vector3(self.x * other, self.y * other, self.z * other)

    def print(self):
        sys.stdout.write("[%f %f %f]\n" % (self.x, self.y, self.z))


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

    def print(self):
        sys.stdout.write("[%f %f %f %f]\n" % (self.x, self.y, self.z, self.w))


class matrix3x3:
    #             I    J     K
    r1 = vector3(1, 0, 0)
    r2 = vector3(0, 1, 0)
    r3 = vector3(0, 0, 1)

    def __init__(self):
        pass

    def print(self):
        sys.stdout.write("[%f %f %f]\n" % (self.r1.x, self.r1.y, self.r1.z))
        sys.stdout.write("[%f %f %f]\n" % (self.r2.x, self.r2.y, self.r2.z))
        sys.stdout.write("[%f %f %f]\n" % (self.r3.x, self.r3.y, self.r3.z))


class matrix4x4:
    #             I    J     K     T
    r1 = vector4(1, 0, 0, 0)
    r2 = vector4(0, 1, 0, 0)
    r3 = vector4(0, 0, 1, 0)
    r4 = vector4(0, 0, 0, 1)

    def __init__(self):
        pass

    def print(self):
        sys.stdout.write("[%f %f %f %f]\n" % (self.r1.x, self.r1.y, self.r1.z, self.r1.w))
        sys.stdout.write("[%f %f %f %f]\n" % (self.r2.x, self.r2.y, self.r2.z, self.r2.w))
        sys.stdout.write("[%f %f %f %f]\n" % (self.r3.x, self.r3.y, self.r3.z, self.r3.w))
        sys.stdout.write("[%f %f %f %f]\n" % (self.r4.x, self.r4.y, self.r4.z, self.r4.w))


# Gauss Jordan Elimination Method
def invert_matrix3x3(in_matrix):
    # Reduction order 0 to 8
    # [6  5  4]
    # [0  7  3]
    # [1  2  8]
    left_side = in_matrix
    right_side = matrix3x3()

    if left_side.r2.x != 0:
        l_candidates = [left_side.r1, left_side.r3]
        r_candidates = [right_side.r1, right_side.r3]
        l_cand = None
        r_cand = None
        for i in range(len(l_candidates)):
            l_c = l_candidates[i]
            r_c = r_candidates[i]
            if l_c.x != 0:
                l_cand = l_c
                r_cand = r_c
                break
        multiplier = -left_side.r2.x / l_cand.x
        to_add_l = l_cand * multiplier
        to_add_r = r_cand * multiplier

        # sys.stdout.write("target: ")
        # left_side.r2.print()
        # sys.stdout.write("cand: ")
        # l_cand.print()
        # sys.stdout.write("mult: ")
        # print(multiplier)
        # sys.stdout.write("to add left side: ")
        # to_add_l.print()
        # sys.stdout.write("to add right side: ")
        # to_add_r.print()
        # sys.stdout.write("left side result: ")
        # (left_side.r2 + to_add_l).print()
        # sys.stdout.write("right side result: ")
        # (right_side.r2 + to_add_r).print()

        left_side.r2 = left_side.r2 + to_add_l
        right_side.r2 = right_side.r2 + to_add_r

        left_side.print()
        sys.stdout.write("\n")
        right_side.print()
        sys.stdout.write("\n")

    if left_side.r3.x != 0:
        l_candidates = [left_side.r1, left_side.r2]
        r_candidates = [right_side.r1, right_side.r2]
        l_cand = None
        r_cand = None
        for i in range(len(l_candidates)):
            l_c = l_candidates[i]
            r_c = r_candidates[i]
            if l_c.x != 0:
                l_cand = l_c
                r_cand = r_c
                break
        multiplier = -left_side.r3.x / l_cand.x
        to_add_l = l_cand * multiplier
        to_add_r = r_cand * multiplier

        left_side.r3 = left_side.r3 + to_add_l
        right_side.r3 = right_side.r3 + to_add_r

        left_side.print()
        sys.stdout.write("\n")
        right_side.print()
        sys.stdout.write("\n")

def invert_matrix4x4(matrix):
    # Reduction order 0 to 15
    # [12 11  9  8]
    # [ 0 13 10  7]
    # [ 1  4 14  6]
    # [ 2  3  5 15]

    left_side = matrix
    right_side = matrix4x4()

    # 1 out of 16
    if matrix.r2.x != 0:
        l_candidates = [left_side.r1, left_side.r3, left_side.r4]
        r_candidates = [right_side.r1, right_side.r3, right_side.r4]
        l_cand = None
        r_cand = None
        for i in range(len(l_candidates)):
            l_c = l_candidates[i]
            r_c = r_candidates[i]
            if l_c.x != 0:
                l_cand = l_c
                r_cand = r_c
                break
        multiplier = -matrix.r2.x / l_cand.x
        to_add_l = l_cand*multiplier
        to_add_r = r_cand*multiplier

        l_cand.print()
        print(multiplier)
        matrix.r2.print()
        to_add_l.print()

        (left_side.r2 + to_add_l).print()
        (right_side.r2 + to_add_r).print()

    return matrix4x4()


# m = matrix4x4()
# m.r1 = vector4(1, 2, -1, 0)
# m.r2 = vector4(2, 5, 1, 0)
# m.r3 = vector4(-1, -2, 2, 0)
# m.r4 = m.r4
#
# im = invert_matrix4x4(m)
# sys.stdout.write("\n\n\n")
# m.print()
# sys.stdout.write("\n")
# im.print()

m = matrix3x3()
m.r1 = vector3(1, 2, -1)
m.r2 = vector3(2, 5, 1)
m.r3 = vector3(-1, -2, 2)

invert_matrix3x3(m)
