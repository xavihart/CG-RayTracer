from .vec3 import *
from .aabb import *
import numpy as np
import os 
import cv2


def save_ppm(file_path, ppm_mat):
    # ppm_mat is a numpy array
    f = open(file_path, "w")
    f.write("P3\n")
    size = ppm_mat.shape
    f.write(str(size[1]//3)+" "+str(int(size[0])))
    f.write("\n255\n")
    for i in range(size[0]):
        for j in range(size[1]):
            f.write(str(int(ppm_mat[i][j]))+" ")
        f.write("\n")
    f.close()

def random_unit_sphere():
    p = vec3(1, 1, 1)
    while p.squared_length() >= 0.5:
        p = vec3(np.random.uniform(0, 1), np.random.uniform(0, 1), np.random.uniform(0, 1)) \
            .mul(2) - vec3(1, 1, 1)
    return p 

def reflect(v:vec3, n:vec3) -> vec3:
    """
    param:
    v : ray-in
    n : normal of the incidence point
    """
    return v - n.mul(2*v.dot(n))


def refract(v:vec3, n:vec3, ni_over_nt, args:dict) -> bool:
    """
    param:
    v : input light
    n : normal for incidence point
    ni_over_nt : sin(ni) / sin(nt) 
    args: dict {'refracted': ?}
    """
    v.make_unit_vector()
    dt = v.dot(n)
    discriminant = 1.0 - (ni_over_nt ** 2) * (1 - dt ** 2)
    if discriminant > 0:
        args['refracted'] = (v - n.mul(dt)).mul(ni_over_nt) - n.mul(math.sqrt(discriminant))
        return True
    else:
        return False
def random_in_unit_disk():
    p = vec3()
    p = vec3(np.random.uniform(0, 1), np.random.uniform(0, 1), 0).mul(2) - vec3(1, 1, 0)
    while True:
        a = p.dot(p)
        if a < 1:
            break
        else:
            p = vec3(np.random.uniform(0, 1), np.random.uniform(0, 1), 0).mul(2) - vec3(1, 1, 0)
    return p
            

def surrounding_bbx(box1:aabb, box2:aabb):
    small = vec3(min(box1._min.x(), box2._min.x()), \
                 min(box1._min.x(), box2._min.y()), \
                 min(box1._min.x(), box2._min.y()))
    large = vec3(max(box1._min.x(), box2._min.x()), \
                 max(box1._min.x(), box2._min.y()), \
                 max(box1._min.x(), box2._min.y()))
    return aabb(small, large)
              

def perlin_generate()->list: 
        l = []
        for _ in range(256):
            rnd_vec = vec3(np.random.uniform(0, 1) * 2 - 1, np.random.uniform(0, 1) * 2 - 1, np.random.uniform(0, 1) * 2 - 1)
            rnd_vec.make_unit_vector()
            l.append(rnd_vec)
        return l
def permute(p:list, n:int):
    # randomly permuate list p
    for i in range(n - 1, 0, -1):
        tar = int(np.random.uniform(0, 1) * (i + 1))
        p[i], p[tar] = p[tar], p[i]
    return 
def perlin_generate_perm():
    p = []
    for i in range(256):
        p.append(i)
    permute(p, 256)
    return p


def nl(x):
    # def a nolinear function
    return (x ** 2) * (3 - 2 * x)     

def trilinear_interpolation(c, u, v, w):
    accum = 0.0
    uu, vv, ww = nl(u), nl(v), nl(w)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                wt = vec3(u-i, v-j, w-k)
                accum += (i*uu+(1-i)*(1-uu)) * (j*vv+(1-j)*(1-vv)) * (k*ww+(1-k)*(1-ww)) * c[i][j][k].dot(wt)
    return accum

def get_sphere_uv(p:vec3):
    """
    param: p, point on the sphere
    return u, v, which determine the 
           coordinate of sphere into 2-D
    """
    phi = math.atan2(p.z(), p.x())
    theta = math.asin(p.y())
    u = 1 - (phi + math.pi) / (math.pi * 2)
    v = (theta + math.pi / 2) / (math.pi)
    return u, v

def image_flatten(pth):
    """
    param: 
    pth : the path for the image, suposed to be *.jpg
    return : a flattened image listed obj
    e.g. 
    get_sphere_uv((rec.p-center)/radius, rec.u, rec.v);
    """
    tar = cv2.imread(pth)
    shp = tar.shape
    tar = np.array(tar)
    tar = tar[:, :, [2, 1, 0]] # cv2 defualt : BGR 
    tar = tar.flatten()
    return tar, shp



