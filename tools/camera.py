from .ray import *
from .vec3 import *
class camera:
    def __init__(self, lower_left_corner_=vec3(-2, -1, -1), horizontal_=vec3(4, 0, 0) \
    , vertical_=vec3(0, 2, 0), origin_=vec3(0, 0, 0)):
        self.lower_left_corner = lower_left_corner_
        self.horizontal = horizontal_
        self.vertical = vertical_
        self.origin = origin_
    def get_ray(self, u, v):
        return ray(self.origin, self.lower_left_corner + \
        self.horizontal.mul(u) + self.vertical.mul(v) - self.origin)
    