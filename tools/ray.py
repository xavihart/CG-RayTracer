from .vec3 import *
class ray:
    def __init__(self, a_=vec3(0, 0, 0), b_=vec3(0, 0, 0), t_=0):
        # note : a_ and b_ must be vec3
        self.a = a_
        self.b = b_
        self.t = t_
    def origin(self):
        return self.a
    def direction(self):
        return self.b
    def point_at_parameter(self, t):
        return self.a + self.b.mul(t)
    def time(self):
        return self.t
if __name__ == "__main__":
    a = vec3(1,2,3)
    b = vec3(1,1,1)
    r = ray(a, b)
    c = r.point_at_parameter(2)
    c.show()
    c = r.point_at_parameter(3)
    c.show()
    
