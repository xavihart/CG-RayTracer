from .hit_list import *
class box:
    def __init__(self, p0:vec3, p1:vec3, mat_):
        self.pmin, self.pmax = p0, p1
        self.mat = mat_
        l = []
        l.append(xy_rect(p0.x(), p1.x(), p0.y(), p1.y(), p1.z(), self.mat))
        l.append(flip_normals(xy_rect(p0.x(), p1.x(), p0.y(), p1.y(), p0.z(), self.mat)))
        l.append(xz_rect(p0.x(), p1.x(), p0.z(), p1.z(), p1.y(), self.mat))
        l.append(flip_normals(xz_rect(p0.x(), p1.x(), p0.z(), p1.z(), p0.y(), self.mat)))
        l.append(yz_rect(p0.y(), p1.y(), p0.z(), p1.z(), p1.x(), self.mat))
        l.append(flip_normals(yz_rect(p0.y(), p1.y(), p0.z(), p1.z(), p0.x(), self.mat)))
        self.hit_list = sphere_list(l)
    def hit(self, r, tmin, tmax):
        return self.hit_list.hit(r, tmin, tmax)
    def bbx(self, t0, t1):
        return (True, aabb(self.pmin, self.pmax))
