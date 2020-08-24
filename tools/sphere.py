from .ray import *
from .material import *
import copy
from .aabb import *
from .utils import *
class hit_record:
    def __init__(self, t_=0, p_=vec3(0, 0, 0), n_=vec3(0, 0, 0), mat_=lambertian(vec3(0, 0, 0)), u_=0, v_=0):
        self.t = t_
        self.p = p_
        self.normal = n_
        self.mat = mat_
        self.u, self.v = u_, v_

class sphere:
    def __init__(self, cen_, rad_, mat_):
        self.cen = cen_
        self.rad = rad_
        self.mat = mat_
    def bbx(self, t0, t1):
        # return a AABB box from this function
        r = self.rad 
        c = self.cen
        box = aabb(c - vec3(r, r, r), c + vec3(r, r, r))
        return (True, box)

    def hit(self, r, t_min, t_max):
        oc = r.origin() - self.cen
        a = r.direction()
        a = a.dot(a)
        b = oc.dot(r.direction()) 
        c = oc.dot(oc) - self.rad * self.rad
        disc = b ** 2 - a * c
        rec = hit_record(0, 0, vec3(0, 0, 0))
        if disc > 0:
            tmp = (-b - math.sqrt(disc)) / a
            if tmp < t_max and tmp > t_min:
                rec.t = tmp
                rec.p = r.point_at_parameter(tmp)
                rec.normal = (rec.p - self.cen).div(self.rad)
                rec.mat = self.mat
                rec.u, rec.v = get_sphere_uv((rec.p - self.cen).div(self.rad))
                #rec.normal.show()
                #print("1")
                return (rec, True)
            tmp = (-b + math.sqrt(disc)) / a
            if tmp < t_max and tmp > t_min:
                rec.t = tmp
                rec.p = r.point_at_parameter(tmp)
                rec.normal = (rec.p - self.cen).div(self.rad)
                rec.mat = self.mat
                rec.u, rec.v = get_sphere_uv((rec.p - self.cen).div(self.rad))
                #rec.normal.show()
                #print("2")
                return (rec, True)
        return (rec, False)


class moving_sphere():
    def __init__(self, cen1_, cen2_, t1_, t2_, r, mat_):
        self.cen1 = cen1_
        self.cen2 = cen2_
        self.t1 = t1_
        self.t2 = t2_
        self.mat = mat_
        self.rad = r
    def bbx(self, t0, t1):
        # return a AABB box at certain time
        r = self.rad 
        c1, c2 = self.center(t0), self.center(t1)
        box1 = aabb(c1 - vec3(r, r, r), c1 + vec3(r, r, r))
        box2 = aabb(c2 - vec3(r, r, r), c2 + vec3(r, r, r))
        return (True, surrounding_bbx(box1, box2))
    def hit(self, r:ray, t_min:float, t_max:float)->(hit_record, bool):
        rt = r.time()
        oc = r.origin() - self.center(rt)
        a = r.direction()
        a = a.dot(a)
        b = oc.dot(r.direction()) 
        c = oc.dot(oc) - self.rad * self.rad
        disc = b ** 2 - a * c
        rec = hit_record(0, 0, vec3(0, 0, 0))
        if disc > 0:
            tmp = (-b - math.sqrt(disc)) / a
            if tmp < t_max and tmp > t_min:
                rec.t = tmp
                rec.p = r.point_at_parameter(tmp)
                rec.normal = (rec.p - self.center(rt)).div(self.rad)
                rec.mat = self.mat
                rec.u, rec.v = get_sphere_uv((rec.p - self.cen1).div(self.rad))
                #rec.normal.show()
                #print("1")
                return (rec, True)
            tmp = (-b + math.sqrt(disc)) / a
            if tmp < t_max and tmp > t_min:
                rec.t = tmp
                rec.p = r.point_at_parameter(tmp)
                rec.normal = (rec.p - self.center(rt)).div(self.rad)
                rec.mat = self.mat
                rec.u, rec.v = get_sphere_uv((rec.p - self.cen1).div(self.rad))
                #rec.normal.show()
                #print("2")
                return (rec, True)
        return (rec, False)
        
    def center(self, t):
        return self.cen1 + (self.cen2 - self.cen1).mul(((t - self.t1) / (self.t2 - self.t1)))





if __name__ == "__main__":
    hit_rec = hit_record(0,0,vec3(0,0,0))
    
