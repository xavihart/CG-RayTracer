from .ray import *
from .utils import *

class lambertian:
    def __init__(self, a):
        self.albedo = a
    def scatter(self, rin, args):
        rec = args['rec']
        tar = rec.p + rec.normal + random_unit_sphere()
        args['scattered'] = ray(rec.p, tar - rec.p)
        #print("scattered")
        #scattered.direction().show()
        args['attenuation'] = self.albedo
        return True


class metal:
    def __init__(self, a):
        self.albedo = a
    def scatter(self, rin:ray, args):
        rec = args['rec']
        r_in_dir = rin.direction()
        r_in_dir.make_unit_vector()
        #print("f*******k")
        ##r_in_dir.show()
        ##rec.normal.show()
        reflected = reflect(r_in_dir, rec.normal)
        args['scattered'] = ray(rec.p, reflected)
        args['attenuation'] = self.albedo
        return args['scattered'].direction().dot(rec.normal) > 0