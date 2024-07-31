import sys
from timeit import default_timer as timer


class v3:
    def __init__(self, in_x, in_y, in_z):
        self.x = in_x
        self.y = in_y
        self.z = in_z


start = timer()

data = [8] * 5000

for d in data:
    d *= 3

end = timer()
sys.stdout.write("\033[0m" + str(round((end - start) * 1000, 3)) + "ms       \n")
