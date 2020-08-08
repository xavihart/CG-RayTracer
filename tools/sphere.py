from .ray import *
from .material import *
import copy

class hit_record:
    def __init__(self, t_=0, p_=vec3(0, 0, 0), n_=vec3(0, 0, 0), mat_=lambertian(vec3(0, 0, 0))):
        self.t = t_
        self.p = p_
        self.normal = n_
        self.mat = mat_

class sphere:
    def __init__(self, cen_, rad_, mat_):
        self.cen = cen_
        self.rad = rad_
        self.mat = mat_
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
                #rec.normal.show()
                #print("1")
                return (rec, True)
            tmp = (-b + math.sqrt(disc)) / a
            if tmp < t_max and tmp > t_min:
                rec.t = tmp
                rec.p = r.point_at_parameter(tmp)
                rec.normal = (rec.p - self.cen).div(self.rad)
                rec.mat = self.mat
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
                #rec.normal.show()
                #print("1")
                return (rec, True)
            tmp = (-b + math.sqrt(disc)) / a
            if tmp < t_max and tmp > t_min:
                rec.t = tmp
                rec.p = r.point_at_parameter(tmp)
                rec.normal = (rec.p - self.center(rt)).div(self.rad)
                rec.mat = self.mat
                #rec.normal.show()
                #print("2")
                return (rec, True)
        return (rec, False)
        
    def center(self, t):
        return self.cen1 + self.cen2.mul(((t - self.t1) / (self.t2 - self.t1)))





if __name__ == "__main__":
    hit_rec = hit_record(0,0,vec3(0,0,0))
    
