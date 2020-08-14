
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
        return vec3(0.5, 0.5, 0.9).mul(0.5 * (1 + math.cos(self.scale * p.z() + 10 * self.noise.turb(p))))
        