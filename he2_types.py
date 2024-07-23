class vector3:
    def __init__(self, in_x, in_y, in_z):
        self.x = in_x
        self.y = in_y
        self.z = in_z
    def to_string(self):
        return "x: %f, y: %f, z: %f" % (self.x, self.y, self.z)
        
class triangle:
    def __init__(self, in_a, in_b, in_c):
        self.a = in_a
        self.b = in_b
        self.c = in_c