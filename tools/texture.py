
from .vec3 import *
from .utils import *
from .ray import *
from .perlin import *

class texture:
    def __init__(self):
        pass
    def value(self, u, v, p):
        pass


class constant_texture(texture):
    # const texture, const color
    def __init__(self, c):
        self.color = c
    def value(self, u:float, v:float, p:vec3)->vec3:
        return self.color

class checker_texture(texture):
    def __init__(self, t0:texture, t1:texture):
        self.odd = t0
        self.even = t1
    def value(self, u, v, p:vec3)->vec3:
        sines = math.sin(10*p.x()) * math.sin(10*p.y()) * math.sin(10*p.z())
        if sines < 0:
            return self.odd.value(u, v, p)
        else:
            return self.even.value(u, v, p)
    
class noise_texture(texture):
    def __init__(self, sc):
        self.noise = perlin()
        self.scale = sc
    def value(self, u, v, p):
        return vec3(1, 1, 1).mul(0.5 * (1 + math.cos(self.scale * p.z() + 10 * self.noise.turb(p))))

class image_texture(texture):
    def __init__(self, pixels, A, B):
        """
        param:
        pixels : a flattened image pixels, [1*(n*m)]
        A : NX
        B : NY
        """
        self.data = pixels
        self.nx, self.ny = B, A
    def value(self, u, v, p:vec3):
        i, j = u  * self.nx, (1 - v) * self.ny - 0.001
        i, j = int(i), int(j)
        i = 0 if i < 0 else i
        j = 0 if j < 0 else j
        i = self.nx - 1 if i > self.nx - 1 else i
        j = self.ny - 1 if j > self.ny - 1 else j
        #print(i, j, "---------")
        r = int(self.data[3*i + 3*self.nx*j]) / 255.0
        g = int(self.data[3*i + 3*self.nx*j + 1]) / 255.0
        b = int(self.data[3*i + 3*self.nx*j + 2]) / 255.0
        # print(r, g, b)
        return vec3(r, g, b)


    