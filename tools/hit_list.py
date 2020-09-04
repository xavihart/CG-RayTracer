from .sphere import sphere, moving_sphere, xy_rect, yz_rect, xz_rect, flip_normals, rotate_y
from .sphere import hit_record
from .vec3 import *
from .utils import *
class sphere_list:
    def __init__(self, sp_list_):
        self.sp_list = sp_list_
        self.list_size = len(sp_list_)

    def bbx(self, t0:float, t1:float)->aabb:
        res = aabb()
        if  self.list_size < 1:
            return (False, res)
        first_true, res = self.sp_list[0].bbx(t0, t1)
        if not first_true:
            return (False, res)
        for i in range(1, len(sphere_list)):
            f, b = self.sp_list[i].bbx(t0, t1)
            if not f:
                return (False, res)
            else:
                res = surrounding_bbx(res, b)
        return (True, res)

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
