from .ray import *
from .utils import *

class lambertian:
    def __init__(self, a):
        self.albedo = a
    def scatter(self, rin, rec, attenuation, scattered):
        tar = rec.p + rec.normal + random_unit_sphere()
        scattered = ray(rec.p, tar - rec.p)
        attenuation = self.albedo
        return True


class metal:
    def __init__(self, a):
        self.albedo = a
    def scatter(self, rin:ray, rec, attenuation, scattered):
        r_in_dir = rin.direction()
        r_in_dir.make_unit_vector()
        reflected = reflect(r_in_dir, rec.normal)
        scattered = ray(rec.p, reflected)
        attenuation = self.albedo
        return scattered.direction().dot(rec.normal) > 0