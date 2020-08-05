from tools.utils import *
from tools.vec3 import *
from tools.ray import *
from tools.hit_list import *
from tools.camera import *
from tools.material import *
import numpy as np
import sys
import os
import time
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--r", default=10, type=int, help="the resolution of the image generated")
parser.add_argument("--ns", default=1, type=int, help="iteration times for background diffusion")
parser.add_argument("--name", default="2", type=str, help="set the name for saving the image")
args = parser.parse_args()


h = args.r
MAXNUM = 1e9
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
a = np.zeros([h, 2*h*3])
time_st = time.time()

print("NOTE: The resolution of your image is:[{} * {}]".format(h, h * 2))

file_pth = os.path.join("./results", "{}.ppm".format(args.name))

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



'''
def color1(r, obj):
    """
    param:
    r : ray 
    obj : hitable object list ,a list of sphere for example
    """
    hit_rec = hit_record(0, 0, vec3(0, 0, 0))
    (hit_rec, f) = obj.hit(r, 0.0001, 1e9 + 7)
    if f:
        #hit_rec.normal.show()
        #return vec3(hit_rec.normal.x()+1, hit_rec.normal.y()+1, hit_rec.normal.z()+1).mul(0.5)
        tar = hit_rec.p + hit_rec.normal + random_unit_sphere()
        return color(ray(hit_rec.p, tar - hit_rec.p), obj).mul(0.5)
    else:
        unit_dir = r.direction()
        unit_dir.make_unit_vector()
        t = 0.5 * (unit_dir.y() + 1)
        return vec3(1 ,1, 1).mul(1 - t) + vec3(0.5, 0.7, 1.0).mul(t)
'''

def color(r, objs, dep):
    rec = hit_record()
    (rec, f) = objs.hit(r, 0.001, MAXNUM)
    # r.direction().show()
    if f:
        attenuation = vec3()
        scattered = ray()
        # print("#####################2")
        args = {'rec':rec, 'attenuation':attenuation, 'scattered':scattered}
        if dep < 50 and rec.mat.scatter(r, args):
            return color(args['scattered'], objs, dep + 1) * args['attenuation']
        else:
            return vec3(0, 0, 0)
    else:
        unit_dir = r.direction()
        # print("#####################")
        # r.direction().show()
        unit_dir.make_unit_vector()
        t = 0.5 * (unit_dir.y() + 1)
        return vec3(1 ,1, 1).mul(1 - t) + vec3(0.5, 0.7, 1.0).mul(t)

    



def main():
    #lower_left_corner = vec3(-2, -1, -1)
    cam = camera()
    ny, nx = a.shape[0], a.shape[1] // 3
    ns = args.ns
    print("shape:", nx, ny)
    l = []
    ## sphere properties
    sphere_cen = [vec3(0,0,-1), vec3(0, -100.5, -1), vec3(1, 0, -1), vec3(-1, 0, -1)]
    sphere_rad = [0.5, 100, 0.5, 0.5]
    sphere_mat = [metal(vec3(0.8, 0.3, 0.3)), lambertian(vec3(0.8, 0.8, 0.0)), \
        metal(vec3(0.8, 0.6, 0.2)), metal(vec3(0.8, 0.8, 0.8))]
    
    assert len(sphere_cen) == len(sphere_mat) and len(sphere_cen) == len(sphere_rad)

    for i in range(len(sphere_mat)):
        l.append(sphere(sphere_cen[i], sphere_rad[i], sphere_mat[i]))
    
    sp_l = sphere_list(l)

    for i in tqdm(range(nx)):
        for j in range(ny-1, -1, -1):
            u = i / nx
            v = j / ny
            col = vec3(0, 0, 0)
            for _ in range(ns):
                u_, v_ = -1, -1
                while u_ > 1 or u_ < 0:
                    u_ = u + np.random.uniform(0, 1e-4)
                while v_ > 1 or v_ < 0:
                    v_ = v + np.random.uniform(0, 1e-4)
                r_ = cam.get_ray(u_, v_)
                # print("$$$$$$$$$$$")
                # print(u_, v_)
                # r_.direction().show()

                col = col + color(r_, sp_l, 0)
                
            col = col.div(ns)
            col = vec3(math.sqrt(col.x()), math.sqrt(col.y()), math.sqrt(col.z()))
            # r = ray(origin, lower_left_corner + horizontal.mul(u) + vertical.mul(v))
            # p = r.point_at_parameter(2.0)
            # col = color(r, sp_l)
            ir, ig, ib = int(255.99 * col.x()), int(255.99 * col.y()), int(255.99 * col.z())
            a[ny - 1 - j][i * 3], a[ny - 1 - j][i * 3 + 1], a[ny - 1 - j][i * 3 + 2] = ir, ig, ib

    save_ppm(file_pth, a)
    time_ed = time.time()
    print("Time consm:", (time_ed - time_st) / 60, "min")
main()