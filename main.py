from tools.utils import *
from tools.vec3 import *
from tools.ray import *
from tools.hit_list import *
from tools.camera import *
import numpy as np
import sys
import os
import timer


h = 100

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
a = np.zeros([h, 2*h*3])

file_pth = "results/2.ppm"

def hit_sphere(c, rad, r):
    """
    c : vec3, center 
    r : float, radius
    r : ray
    """
    oc = r.origin() - c
    a = r.direction()
    a = a.dot(a)
    b = 2 * oc.dot(r.direction()) 
    c = oc.dot(oc) - rad * rad
    disc =  b*b - 4*a*c
    if disc <  0:
        return -1
    else:
        return (-b - math.sqrt(disc)) / (2 * a)


def color(r, obj):
    """
    param:
    r : ray 
    obj : hitable object list ,a list of sphere for example
    """
    hit_rec = hit_record(0, 0, vec3(0, 0, 0))
    (hit_rec, f) = obj.hit(r, 0, 1e9 + 7)
    if f:
        #hit_rec.normal.show()
        return vec3(hit_rec.normal.x()+1, hit_rec.normal.y()+1, hit_rec.normal.z()+1).mul(0.5)
    else:
        unit_dir = r.direction()
        unit_dir.make_unit_vector()
        t = 0.5 * (unit_dir.y() + 1)
        return vec3(1 ,1, 1).mul(1 - t) + vec3(0.5, 0.7, 1.0).mul(t)

def main():
    lower_left_corner = vec3(-2, -1, -1)
    cam = camera()
    ny, nx = a.shape[0], a.shape[1] // 3
    ns = 100
    print("shape:", nx, ny)
    l = [sphere(vec3(0, -100.5, -1), 100), sphere(vec3(0, 0, -1), 0.5)]
    sp_l = sphere_list(l)
    for i in range(nx):
        for j in range(ny-1, -1, -1):
            u = i / nx
            v = j / ny
            col = vec3(0, 0, 0)
            for s in range(ns):
                u_, v_ = -1, -1
                while u_ > 1 or u_ < 0:
                    u_ = u + np.random.uniform(0, 1e-2)
                while v_ > 1 or v_ < 0:
                    v_ = v + np.random.uniform(0, 1e-2)
                #print(u_, v_)
                r_ = cam.get_ray(u_, v_)
                col = col + color(r_, sp_l)
                
            col = col.div(ns)
            # r = ray(origin, lower_left_corner + horizontal.mul(u) + vertical.mul(v))
            # p = r.point_at_parameter(2.0)
            # col = color(r, sp_l)
            ir, ig, ib = int(255.99 * col.x()), int(255.99 * col.y()), int(255.99 * col.z())
            a[ny - 1 - j][i * 3], a[ny - 1 - j][i * 3 + 1], a[ny - 1 - j][i * 3 + 2] = ir, ig, ib

    save_ppm(file_pth, a)
    


main()