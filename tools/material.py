from .ray import *
from .utils import *
from .texture import *

class material:
    # base class for all materials
    def scatter(self, rin, args):
        return 
    def emitted(self, u, v, p):
        return vec3(0, 0, 0)



class lambertian(material):
    def __init__(self, a):
        self.albedo = a
    def scatter(self, rin, args):
        rec = args['rec']
        tar = rec.p + rec.normal + random_unit_sphere()
        args['scattered'] = ray(rec.p, tar - rec.p, rin.time())
        #print("scattered")
        #scattered.direction().show()
        args['attenuation'] = self.albedo.value(args['rec'].u, args['rec'].v, args['rec'].p)
        return True


class metal(material):
    def __init__(self, a, f):
        self.albedo = a
        self.fuzz = 1 if f >= 1 else f
    def scatter(self, rin:ray, args):
        rec = args['rec']
        r_in_dir = rin.direction()
        r_in_dir.make_unit_vector()
        reflected = reflect(r_in_dir, rec.normal)
        # take into account the fuzz
        args['scattered'] = ray(rec.p, reflected + random_unit_sphere().mul(self.fuzz)) 
        args['attenuation'] = self.albedo
        return args['scattered'].direction().dot(rec.normal) > 0



class dielectric(material):
    def __init__(self, ri):
        self.ref_idx = ri
        # self.attenuation = a
        # p.s. actually attenuation must be (1, 1, 1)
    def scatter(self, rin:ray, args):
        # in args  = {'rec', 'attenuation', 'scatter'}
        outward_normal = vec3()
        reflected = reflect(rin.direction(), args['rec'].normal)
        attenuation = vec3(1, 1, 1)
        ni_over_nt = 0
        if rin.direction().dot(args['rec'].normal) > 0:
            outward_normal = - args['rec'].normal
            ni_over_nt = self.ref_idx
        else:
            outward_normal = args['rec'].normal
            ni_over_nt = 1.0 / self.ref_idx
        refracted = vec3()
        args['attenuation'] = attenuation
        args_ = {'refracted':refracted}
        f = refract(rin.direction(), outward_normal, ni_over_nt, args_)
        if f:
            args['scattered'] = ray(args['rec'].p, args_['refracted'])
        else:   
            args['scattered'] = ray(args['rec'].p, reflected)
            return False
        return True



            


    