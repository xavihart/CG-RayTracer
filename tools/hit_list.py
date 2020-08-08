from .sphere import sphere, moving_sphere
from .sphere import hit_record
from .vec3 import *
class sphere_list:
    def __init__(self, sp_list_):
        self.sp_list = sp_list_
    def hit(self, r, tmin, tmax):
        tmp_rec = hit_record(0, 0, vec3(0, 0, 0))
        rec = hit_record(0, 0, vec3(0, 0, 0))
        hit_anything = False
        closest = tmax
        for i in range(len(self.sp_list)):
            #print(self.sp_list[i].hit(r, tmin, closest))
            (tmp_rec, f) = self.sp_list[i].hit(r, tmin, closest)
            if f and closest > tmp_rec.t:
                hit_anything = True
                closest = tmp_rec.t
                rec = tmp_rec
        return (rec, hit_anything)
