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

class hitable:
    def __init__(self):
        return 
    def bbx(self):
        return 
    def hit(self, rin, tmin, tmax)->(hit_record, bool):
        return

class sphere(hitable):
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


class moving_sphere(hitable):
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


class xy_rect(hitable):
    def __init__(self, x0_, x1_, y0_, y1_, k_, mat_):
        self.x0 = x0_
        self.x1 = x1_
        self.y0 = y0_
        self.y1 = y1_
        self.k = k_
        self.mat = mat_
    def bbx(self, t0, t1):
        box = aabb(vec3(self.x0, self.y0, self.k-0.0001), \
            vec3(self.x1, self.y1, self.k+0.0001))
        # avoid it to become a 0-width plane
        return (True, box)
    def hit(self, r:ray, t0, t1)->(hit_record, bool):
        x0, x1, y0, y1 = self.x0, self.x1, self.y0, self.y1
        t = (self.k - r.origin().z()) / (r.direction().z() + 0.00001)
        rec = hit_record()
        if t < t0 or t >t1 :
            return (hit_record, False)
        x = r.origin().x() + t * r.direction().x()
        y = r.origin().y() + t * r.direction().y()
        if x > x1 or x < x0 or y < y0 or y > y1:
            return (hit_record, False)
        rec.u = (x - x0) / (x1 - x0)
        rec.v = (y - y0) / (y1 - y0)
        rec.t = t
        rec.mat = self.mat
        rec.p = r.point_at_parameter(t)
        rec.normal = vec3(0, 0, 1) # point up along axis-z
        return (rec, True)

class xz_rect(hitable):
    def __init__(self, x0_, x1_, y0_, y1_, k_, mat_):
        self.x0 = x0_
        self.x1 = x1_
        self.z0 = y0_
        self.z1 = y1_
        self.k = k_
        self.mat = mat_
    def bbx(self, t0, t1):
        box = aabb(vec3(self.x0, self.z0, self.k-0.0001), \
            vec3(self.x1, self.z1, self.k+0.0001))
        # avoid it to become a 0-width plane
        return (True, box)
    def hit(self, r:ray, t0, t1)->(hit_record, bool):
        x0, x1, y0, y1 = self.x0, self.x1, self.z0, self.z1
        rec = hit_record()
        if r.direction().y() == 0:
            return (rec, False) 
        t = (self.k - r.origin().y()) / (r.direction().y())
        if t < t0 or t > t1 :
            return (rec, False)
        x = r.origin().x() + t * r.direction().x()
        y = r.origin().z() + t * r.direction().z()
        if x > x1 or x < x0 or y < y0 or y > y1:
            return (hit_record, False)
        rec.u = (x - x0) / (x1 - x0)
        rec.v = (y - y0) / (y1 - y0)
        rec.t = t
        rec.mat = self.mat
        rec.p = r.point_at_parameter(t)
        rec.normal = vec3(0, 1, 0) # point up along axis-z
        return (rec, True)


class yz_rect(hitable):
    def __init__(self, x0_, x1_, y0_, y1_, k_, mat_):
        self.y0 = x0_
        self.y1 = x1_
        self.z0 = y0_
        self.z1 = y1_
        self.k = k_
        self.mat = mat_
    def bbx(self, t0, t1):
        box = aabb(vec3(self.y0, self.z0, self.k-0.0001), \
            vec3(self.y1, self.z1, self.k+0.0001))
        # avoid it to become a 0-width plane
        return (True, box)
    def hit(self, r:ray, t0, t1)->(hit_record, bool):
        x0, x1, y0, y1 = self.y0, self.y1, self.z0, self.z1
        t = (self.k - r.origin().x()) / (r.direction().x() + 0.00001)
        rec = hit_record()
        if t < t0 or t >t1 :
            return (hit_record, False)
        x = r.origin().y() + t * r.direction().y()
        y = r.origin().z() + t * r.direction().z()
        if x > x1 or x < x0 or y < y0 or y > y1:
            return (hit_record, False)
        rec.u = (x - x0) / (x1 - x0)
        rec.v = (y - y0) / (y1 - y0)
        rec.t = t
        rec.mat = self.mat
        rec.p = r.point_at_parameter(t)
        rec.normal = vec3(1, 0, 0) # point up along axis-z
        return (rec, True)


class flip_normals(hitable):
    def __init__(self, p):
        self.obj = p
    def hit(self, r, tmin, tmax)->(hit_record, bool):
        (rec, f) = self.obj.hit(r, tmin, tmax)
        if f:
            rec.normal =  - rec.normal
            return (rec, True)
        else:
            return (rec, False)
    def bbx(self, t0, t1):
        return self.obj.bbx()
            

class translate(hitable):
    def __init__(self, p:hitable, displacemnet_:vec3):
        self.ptr = p
        self.offset = displacemnet_
    def hit(self, r:ray, tmin, tmax)->(hit_record, bool):
        r_moved = ray(r.origin() - self.offset, r.direction(), r.time())
        (rec, f) = self.ptr.hit(r_moved, tmin, tmax)
        if f:
            rec.p += self.offset
            return (rec, True)
        else:
            return (rec, f)
    def bbx(self, t0, t1)->(bool, aabb):
        (f, box) = self.ptr.bbx()
        if f:
            box = aabb(box.min() + self.offset, box.max() + self.offset)
            return (f, box)
        else:
            return (f, box)

class rotate_y(hitable):
    def __init__(self, p:hitable, angle):
        self.ptr = p
        rad = (math.pi * 180) * angle
        self.sin_theta = math.sin(rad)
        self.cos_theta = math.cos(rad)
       # print(type(self.ptr))
       # print(self.ptr.bbx(0, 1))
        (_, box) = self.ptr.bbx(0,1)
        min_ = vec3(1e9, 1e9, 1e9)
        max_ = vec3(-1e9, -1e9, -1e9)
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    x = i * box._max.x() + (1 - i) * box._min.x()
                    y = j * box._max.y() + (1 - j) * box._min.y()
                    z = k * box._max.z() + (1 - k) * box._min.z()
                    newx = self.cos_theta * x + self.sin_theta * z
                    newz = - self.sin_theta * x + self.cos_theta * z
                    tester = vec3(newx, y, newz)
                    # update max_ and min_
                    if max_.a < tester.a:
                        max_.a = tester.a
                    if max_.b < tester.b:
                        max_.b = tester.b
                    if max_.c < tester.c:
                        max_.c = tester.c
                    if min_.a > tester.a:
                        min_.a = tester.a
                    if min_.b > tester.b:
                        min_.b = tester.b
                    if min_.c > tester.c:
                        min_.c = tester.c
        self.bbx_box = aabb(min_, max_)
    def bbx(self):
        return (True, self.bbx_box)    
    def hit(self, r:ray, tmin:float, tmax:float)->(hit_record, bool):
        origin = r.origin()
        direction = r.direction()
        origin.a = self.cos_theta * r.origin().a - self.sin_theta * r.origin().c
        origin.c = self.sin_theta * r.origin().a + self.cos_theta * r.origin().c
        direction.a = self.cos_theta * r.direction().a - self.sin_theta * r.direction().c
        direction.c = self.sin_theta * r.direction().a + self.cos_theta * r.direction().c
        #rotated_r = ray(origin, direction, r.time())
        (rec, f) = self.ptr.hit(r, tmin, tmax)
        if f:
            p = rec.p
            n = rec.normal
            p.a = self.cos_theta * rec.p.a + self.sin_theta * rec.p.c
            p.c = - self.sin_theta * rec.p.a + self.cos_theta * rec.p.c
            n.a = self.cos_theta * rec.normal.a + self.sin_theta * rec.normal.c
            n.c = - self.sin_theta * rec.normal.a + self.cos_theta * rec.normal.c
            rec.p = p
            rec.n = n
            return (rec, True)
        else:
            return(rec, False)             


if __name__ == "__main__":
    hit_rec = hit_record(0,0,vec3(0,0,0))
    
