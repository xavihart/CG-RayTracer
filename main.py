from tools.utils import *
from tools.vec3 import *
from tools.ray import *
import numpy as np
import sys
import os


h = 10

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
a = np.zeros([h, 2*h*3])

file_pth = "results/2.ppm"

def color(r):
    a = r.direction()
    a.make_unit_vector()
    white = vec3(1,1,1)
    blue = vec3(0.5, 0.7, 1.0)
    t = 0.5 * (a.y() + 1.0)
    print(t)
    return white.mul(1-t) + blue.mul(t)


lower_left_corner = vec3(-2, -1, -1)
horizontal = vec3(4, 0, 0)
vertical = vec3(0, 2, 0)
origin = vec3(0, 0, 0)

nx, ny = a.shape[0], a.shape[1] // 3
print(nx, ny)
for i in range(nx):
    for j in range(ny-1, -1, -1):
        u = i / nx
        v = j / ny
        r = ray(origin, lower_left_corner + horizontal.mul(0) + vertical.mul(0))
        pp = r.direction()
        col = color(r)
        ir, ig, ib = int(255.99 * col.x()), int(255.99 * col.y()), int(255.99 * col.z())
        a[i][j*3], a[i][j*3+1], a[i][j*3+2] = ir, ig, ib
        
save_ppm(file_pth, a)


