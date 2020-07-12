from .ray import *
import copy
class hit_record:
    def __init__(self, t_=0, p_=0, n_=vec3(0, 0, 0)):
        self.t = t_
        self.p = p_
        self.normal = n_


class sphere:
    def __init__(self, cen_, rad_):
        self.cen = cen_
        self.rad = rad_
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
                #rec.normal.show()
                #print("1")
                return (rec, True)
            tmp = (-b + math.sqrt(disc)) / a
            if tmp < t_max and tmp > t_min:
                rec.t = tmp
                rec.p = r.point_at_parameter(tmp)
                rec.normal = (rec.p - self.cen).div(self.rad)
                #rec.normal.show()
                #print("2")
                return (rec, True)
        return (rec, False)

if __name__ == "__main__":
    hit_rec = hit_record(0,0,vec3(0,0,0))
    s1 = sphere(vec3(0, 0, 0), 2)
    ra = ray(vec3(0, 0, 0), vec3(1, 1, 1))
    a = s1.hit(ra, -1.14, 1.14, hit_rec)
    print(a)
