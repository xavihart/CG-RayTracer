from tools.utils import *
from tools.vec3 import *
from tools.ray import *
from tools.hit_list import *
from tools.camera import *
from tools.material import *
from tools.aabb import *
from tools.texture import *
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

file_pth = os.path.join("./results/nxt_week", "{}.ppm".format(args.name))

def two_spheres():
    checker = checker_texture(constant_texture(vec3(0.2, 0.3, 0.1)), constant_texture(vec3(0.9, 0.9, 0.9)))
    l = []
    l.append(sphere(vec3(0, -10, 0), 10, lambertian(checker)))
    l.append(sphere(vec3(0, 10, 0), 10, lambertian(checker)))
    return l
def two_spheres_perlin():
    tex = noise_texture(3)
    l = []
    l.append(sphere(vec3(0, -1000, 0), 1000, lambertian(tex)))
    l.append(sphere(vec3(0, 2, 0), 2, lambertian(tex)))
    return l

def generate_random_spheres():
    """
    using methods from the book 11 * 11 grids
    return sphere list
    """

    obj_list = []
    n = 5
    # cen_list.append(vec3(0, -1000, 0))
    # rad_list.append(1000)
    # mat_list.append(lambertian(vec3(0.5, 0.5, 0.5)))
    checker = checker_texture(constant_texture(vec3(0.2, 0.3, 0.1)), constant_texture(vec3(0.9, 0.9, 0.9)))
    obj_list.append(sphere(vec3(0, -1000, 0), 1000, lambertian(checker)))
    for a in range(-n, n):
        for b in range(-n, n):
            p = np.random.uniform(0, 1)
            cent = vec3(a + 0.9 * np.random.uniform(0, 1), 0.2, b + np.random.uniform(0, 1))
            if (cent - vec3(4, 0.2, 0)).length() > 0.9:
                if p < 0.8:
                    # cen_list.append(cent)
                    # rad_list.append(0.2)
                    vp = vec3(np.random.uniform(0, 1) ** 2, np.random.uniform(0, 1) ** 2, np.random.uniform(0, 1) ** 2)
                    m = lambertian(constant_texture(vp))
                    # moving.append[1]
                    cent_end = cent + vec3(0, 0.5 * np.random.uniform(0, 1), 0)
                    obj_list.append(moving_sphere(cent, cent_end, 0, 1, 0.2, m))
                elif p < 0.95:
                    #moving.append(0)
                    #cen_list.append(cent)
                    #rad_list.append(0.2)
                    mat = metal(vec3((np.random.uniform(0, 1) + 1 ) / 2 , (np.random.uniform(0, 1) + 1 ) / 2, (np.random.uniform(0, 1) + 1 ) / 2), \
                        np.random.uniform(0, 1) * 0.5)
                    obj_list.append(sphere(cent, 0.2, mat))
                else:
                    # moving.append(0)
                    # cen_list.append(cent)
                    # rad_list.append(0.2)
                    # mat_list.append(dielectric(1.5))
                    obj_list.append(sphere(cent, 0.2, dielectric(1.5)))
    cen_list, rad_list, mat_list = [], [], []
    cen_list += [vec3(0, 1, 0), vec3(-4, 1, 0), vec3(4, 1, 0)]
    rad_list += [1, 1, 1]
    mat_list += [dielectric(1.5), lambertian(constant_texture(vec3(0.4, 0.2, 0.1))), metal(vec3(0.7, 0.6, 0.5), 0.0)]
    for i in range(len(cen_list)):
        obj_list.append(sphere(cen_list[i], rad_list[i], mat_list[i]))
    
    return obj_list
    

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
        # print(t)
        return vec3(1 ,1, 1).mul(1 - t) + vec3(0.5, 0.7, 1.0).mul(t)

    



def main():
    #lower_left_corner = vec3(-2, -1, -1)
    ny, nx = a.shape[0], a.shape[1] // 3
    aperture = 0
    """ two green grid spheres
    look_from = vec3(13, 2, 3)
    look_at = vec3(0, 0, 0)
    dist_to_focus = 10
    """
    look_from = vec3(13, 2, 3)
    look_at = vec3(0, 0, 0)
    dist_to_focus = 10

    cam = camera(look_from, look_at, vec3(0, 1, 0), 30, nx / ny, aperture, dist_to_focus, 0, 1)    
    ns = args.ns
    l = []
    ## sphere properties list

    """
    cen_list = [(i * 0.2 - 0.6, 0) for i in range(7)] + [(i * 0.2 - 0.6, -1.2) for i in range(7)] \
        + [(-0.6, -0.2 - i * 0.2) for i in range(5)] + [(0.6, -0.2 - i * 0.2) for i in range(5)] + [(-0.4 + i * 0.2, -0.6) for i in range(5)] \
             + [(i * 0.2 - 1.2, 0.4) for i in range(13)]


    sphere_cen = []
    ceng = 5
    for c in range(ceng):
        sphere_cen = sphere_cen +  [vec3(i, 0.1 * c, j) for (i, j) in cen_list]

    sphere_cen += [vec3(0, -100.5, -1)]
    sphere_rad = [0.1 for i in range(len(cen_list))] * ceng + [100]
    sphere_mat = ([metal(vec3(0.9, 0.1, 0.9), 0) for i in range(len(cen_list) - 13)] + [lambertian(vec3(0.1, 0.5, 0.4)) for i in range(13)]) * ceng + [lambertian(vec3(0.8, 0.8, 0.0))]
    
   
    sphere_cen = [vec3(0,0,-1), vec3(0, -100.5, -1), vec3(1, 0, -1), vec3(-1, 0, -1)]
    sphere_rad = [0.5, 100, 0.5, 0.5]
    sphere_mat = [lambertian(vec3(0.1, 0.2, 0.5)), lambertian(vec3(0.8, 0.8, 0.0)), \
        metal(vec3(0.8, 0.6, 0.2), 0), dielectric(1.5)]
    """

    l = two_spheres_perlin()
    # assert len(sphere_cen) == len(sphere_mat) and len(sphere_cen) == len(sphere_rad)
    print("You generated {} spheres at all".format(len(l)))

    # for i in range(len(sphere_mat)):
    #   l.append(sphere(sphere_cen[i], sphere_rad[i], sphere_mat[i]))
    
    sp_l = sphere_list(l)

    for i in tqdm(range(nx)):
        for j in range(ny-1, -1, -1):
            u = i / nx
            v = j / ny
            col = vec3(0, 0, 0)
            # background diffusion
            """
            for _ in range(ns):
                u_, v_ = -1, -1
                while u_ > 1 or u_ < 0:
                    u_ = u + np.random.uniform(0, 1e-5)
                while v_ > 1 or v_ < 0:
                    v_ = v + np.random.uniform(0, 1e-5)
                # get sight
                r_ = cam.get_ray(u_, v_)
                # print(r_.time())
                col = col + color(r_, sp_l, 0)
            # gamma repair
            col = col.div(ns)
            """
            r = cam.get_ray(u, v)
            col = col + color(r, sp_l, 0)
            col = vec3(math.sqrt(col.x()), math.sqrt(col.y()), math.sqrt(col.z()))
            ir, ig, ib = int(255.99 * col.x()), int(255.99 * col.y()), int(255.99 * col.z())
            a[ny - 1 - j][i * 3], a[ny - 1 - j][i * 3 + 1], a[ny - 1 - j][i * 3 + 2] = ir, ig, ib
    # save image as *.ppm 
    save_ppm(file_pth, a)
    time_ed = time.time()
    print("Time consm:", (time_ed - time_st) / 60, "min")
main()