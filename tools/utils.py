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

    
    