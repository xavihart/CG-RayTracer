from .sphere import sphere
from .sphere import hit_record

class sphere_list:
    def __init__(self, sp_list_):
        self.sp_list = sp_list_
    def hit(self, r, tmin, tmax, rec):
        tmp_rec = hit_record
        hit_anything = False
        closest = tmax
        for i in range(len(self.sp_list)):
            if self.sp_list[i].hit(r, tmin, closest, tmp_rec):
                hit_anything = True
                closest = tmp_rec.t
                rec = tmp_rec
        return hit_anything
