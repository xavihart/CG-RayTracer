from .vec3 import *
from .ray import *
class aabb:
    def __init__(self, min_=vec3(), max_=vec3()):
        self._min = min_
        self._max = max_

    def min(self):
        return self._min
    def max(self):
        return self._max
    
    def hit(self, r:ray, tmin, tmax):
        for a in range(3):
            # add 1e-10 to make division not 0
            t0, t1 = min((self._min.idx(a) - r.origin().idx(a)) / (r.direction().idx(a)+1e-10), \
                     (self._max.idx(a) - r.origin().idx(a)) / (r.direction().idx(a)+1e-10)),  \
                     max((self._min.idx(a) - r.origin().idx(a)) / (r.direction().idx(a)+1e-10), \
                     (self._max.idx(a) - r.origin().idx(a)) / (r.direction().idx(a)+1e-10)) 
            tmin = max(tmin, t0)
            tmax = min(tmax, t1)
            if tmax < tmin:
                return False
        return True

            
            


