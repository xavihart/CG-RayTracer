from .ray import *
from .vec3 import *
class camera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect):
        u, v, w = vec3(), vec3(), vec3()
        theta = vfov * math.pi / 180
        half_h = math.tan(theta / 2)
        half_w = aspect * half_h
        self.origin = lookfrom 
        w = lookfrom - lookat
        u = vup.cross(w)
        w.make_unit_vector()
        u.make_unit_vector()
        v = w.cross(u)
        self.lower_left_corner = self.origin - u.mul(half_w) - v.mul(half_h) - w
        self.horizontal = u.mul(2 * half_w)
        self.vertical  = v.mul(2 * half_h)
    def get_ray(self, s, t):
        return ray(self.origin, self.lower_left_corner + self.horizontal.mul(s) + self.vertical.mul(t) - self.origin)

    