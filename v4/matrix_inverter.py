import math
import sys


class vec4:
    x: float
    y: float
    z: float
    w: float

    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, other):
        return vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __mul__(self, other: float):
        return vec4(self.x * other, self.y * other, self.z * other, self.w * other)

    def __truediv__(self, other: float):
        return vec4(self.x / other, self.y / other, self.z / other, self.w / other)

    def get_comp(self, comp_idx: int) -> float:
        match comp_idx:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.z
            case 3:
                return self.w

    def to_string(self):
        return "[%f %f %f %f]" % (self.x, self.y, self.z, self.w)

    def print(self):
        sys.stdout.write(self.to_string())
# end vector4


class mat4x4:
    # columns of matrix
    i: vec4
    j: vec4
    k: vec4
    l: vec4

    def __init__(self):
        pass

    def get_row(self, row_idx: int) -> vec4:
        match row_idx:
            case 0:
                return vec4(self.i.x, self.j.x, self.k.x, self.l.x)
            case 1:
                return vec4(self.i.y, self.j.y, self.k.y, self.l.y)
            case 2:
                return vec4(self.i.z, self.j.z, self.k.z, self.l.z)
            case 3:
                return vec4(self.i.w, self.j.w, self.k.w, self.l.w)

    def set_row(self, row_idx: int, new_value: vec4) -> None:
        match row_idx:
            case 0:
                self.i.x = new_value.x
                self.j.x = new_value.y
                self.k.x = new_value.z
                self.l.x = new_value.w
                return
            case 1:
                self.i.y = new_value.x
                self.j.y = new_value.y
                self.k.y = new_value.z
                self.l.y = new_value.w
                return
            case 2:
                self.i.z = new_value.x
                self.j.z = new_value.y
                self.k.z = new_value.z
                self.l.z = new_value.w
                return
            case 3:
                self.i.w = new_value.x
                self.j.w = new_value.y
                self.k.w = new_value.z
                self.l.w = new_value.w
                return

    def print(self) -> None:
        sys.stdout.write(
            "%s\n" % (self.get_row(0).to_string()) +
            "%s\n" % (self.get_row(1).to_string()) +
            "%s\n" % (self.get_row(2).to_string()) +
            "%s\n" % (self.get_row(3).to_string()))
# end mat4x4


# def dot(v1: vec4, v2: vec4):
#     return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z + v1.w * v2.w
#
#
# def length(v: vec4):
#     return math.sqrt(dot(v, v))

def det(matrix: mat4x4) -> float:
    workpiece: mat4x4 = matrix
    for i in range(4):
        row_original_view: vec4 = workpiece.get_row(i)
        ct: float = row_original_view.get_comp(i)
        oneified: vec4 = row_original_view / ct
        for j in range(i+1, 4):
            row: vec4 = workpiece.get_row(j)
            to_null: float = row.get_comp(i)
            row_result = row - oneified * to_null
            workpiece.set_row(j, row_result)
        workpiece.print()
        sys.stdout.write("\n")

    result: float = 1.0
    for i in range(4):
        result *= workpiece.get_row(i).get_comp(i)
    return result

#  test matrix 4x4 no. 1:
#  1.45   2.0   -1.0    5.2
#  2.0    5.0    6.0    2.0
# -7.0	-19.3    2.0   -7.31
#  8.98   0.0    6.43   1.0
#  Determinant should equal -4845.9069749999999996

m = mat4x4()
m.l = vec4(5.2, 2.0, -7.31, 1.0)
m.k = vec4(-1.0, 6.0, 2.0, 6.43)
m.j = vec4(2.0, 5.0, -19.3, 0.0)
m.i = vec4(1.45, 2.0, -7.0, 8.98)

#m.print()
print(det(m))
