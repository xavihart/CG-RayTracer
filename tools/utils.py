from .vec3 import *
from .aabb import *
import numpy as np
import os 


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
    while p.squared_length() >= 1:
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
              
        