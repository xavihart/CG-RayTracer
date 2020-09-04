from .vec3 import *
from .utils import *
import numpy as np

class perlin:
    def __init__(self):
        self.perm_x = perlin_generate_perm()
        self.perm_y = perlin_generate_perm()
        self.perm_z = perlin_generate_perm()
        self.ranfloat = perlin_generate()

    def noise(self, p:vec3):
        u, v, w = p.x() - math.floor(p.x()), p.y() - math.floor(p.y()), p.z() - math.floor(p.z())
        i, j, k = math.floor(p.x()), math.floor(p.y()), math.floor(p.z())
        # u, v, w = nl(u), nl(v), nl(w)
        c = [[[vec3() for j in range(2)] for i in range(2)] for k in range(2)]
        # add trilinear interpolation
        for bi in range(2):
            for bj in range(2):
                for bk in range(2):
                    c[bi][bj][bk] = self.ranfloat[self.perm_x[(i+bi)&255] ^ self.perm_y[(j+bj)&255] ^ self.perm_z[(k+bk)&255]]
        return trilinear_interpolation(c, u, v, w)

    def turb(self, p:vec3, dp=3):
        accum = 0
        tmp_p = p
        w = 1.0
        for _ in range(dp):
            accum += w * self.noise(tmp_p)
            w *= 0.5
            tmp_p = tmp_p.mul(2)
        return abs(accum)
        
    
            