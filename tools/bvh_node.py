from .bbaa import *
from .vec3 import *
from .ray import *
from .hit_list import *
import numpy as np
class bvh_node:
    def __init__(self, sp_l:sphere_list, time0, time1):
        # note : sp_l is a class-type container (has functions), not a typical list
        # in the init function we create a bvh tree, the node type is class sphere_list
        # when dividing, we randomly choose from x,y,z of min-aabb to compare 
        # private members : left, right, box
        p = int(np.random.uniform(0, 1))
        if  p == 0:
            sp_l.sp_list.sort(key=lambda o:o.bbx(0, 0)[1].min().x())
        elif p == 1:
            sp_l.sp_list.sort(key=lambda o:o.bbx(0, 0)[1].min().y())
        else:
            sp_l.sp_list.sort(key=lambda o:o.bbx(0, 0)[1].min().z())
        n = len(sp_l)
        if n == 1:
            self.left = sphere_list(sp_l.sp_list[0:1])
            self.right = sphere_list(sp_l.sp_list[0:1])
        elif n == 2:
            self.left = sphere_list(sp_l.sp_list[0:1])
            self.right = sphere_list(sp_l.sp_list[1:2])
        else:
            self.left = bvh_node(sphere_list(sp_l.sp_list[0:n//2]), time0, time1)
            self.right = bvh_node(sphere_list(sp_l.sp_list[n//2 - 1 : n]), time0, time1)
        f1, b1 = self.left.bbx(time0, time1)
        f2, b2 = self.right.bbx(time0, time1)
        # liggy
        assert (f1 and f2) == True
        self.box = surrounding_bbx(b1, b2)
    # to do
    def hit(self, r:ray, tmin, tmax)->(bool, hit_record):
        """
        return : (flag, hit_record)
        binary searching
        """
        rec = hit_record()
        f = self.box.hit(r, tmin, tmax)
        if f:
            l_rcd, l_flag = self.left.hit(r, tmin, tmax)
            r_rcd, r_flag = self.right.hit(r, tmin, tmax)
            ## ??? it seems that we still use the original hit function to make decision, 
            ## which may of no use actually regarding the time complexity
            if l_flag and r_flag:
                if l_rcd.t < r_rcd.t:
                    return (True, l_rcd)
                else:
                    return (True, r_rcd)
            elif l_flag:
                return (True, l_rcd)
            elif r_flag:
                return (True, r_rcd)
            else:
                return (False, rec)
        else:
            return (False, rec)



            



