from .vec3 import *
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
