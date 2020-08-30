from .ray import *
from .vec3 import *
from .utils import *
class camera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect, aperture, focus_dist, t0_, t1_):
        self.len_radius = aperture / 2
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
        self.lower_left_corner = self.origin - u.mul(half_w * focus_dist) - v.mul(half_h * focus_dist) - w.mul(focus_dist)
        self.horizontal = u.mul(2 * half_w * focus_dist)
        self.vertical  = v.mul(2 * half_h * focus_dist)
        self.u = u
        self.v = v
        self.w = w
        self.t0 = t0_
        self.t1 = t1_
    def get_ray(self, s, t):
        rd = random_in_unit_disk()
        rd = rd.mul(self.len_radius)
        offset = self.u.mul(rd.x()) + self.v.mul(rd.y())
        interval_t = self.t0 + (self.t1 - self.t0) * np.random.uniform(0, 1)
        return ray(self.origin + offset, self.lower_left_corner + self.horizontal.mul(s) +  \
            self.vertical.mul(t) - self.origin - offset, interval_t)

    