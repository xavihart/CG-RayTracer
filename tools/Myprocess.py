from multiprocessing import Process 
from .color import *
import time
import copy
class myProcess(Process):
    def __init__(self, args):
        super(myProcess, self).__init__()
        self.works = 0
        self.done = 0
        self.time_st = 0
        self.args = args.copy()
    def run(self):
        pixel_list, cam, sp_l, a, nx, ny, ns = self.args['pixel_list'].copy(), self.args['cam'], self.args['sp_l'], self.args['a'], \
            self.args['nx'], self.args['ny'], self.args['ns']
        
        self.time_st = time.time()
        x_list = [i[0] for i in pixel_list]
        y_list = [i[1] for i in pixel_list]
        assert len(x_list) == len(y_list)
        self.works = len(x_list)
        for p in range(len(pixel_list)):
            
            x, y = x_list[p], y_list[p]
            u = x / nx
            v = y / ny
            i, j = x, y
            col = vec3(0, 0, 0)
            for _ in range(ns):
                u_, v_ = -1, -1
                while u_ > 1 or u_ < 0:
                    u_ = u + np.random.uniform(0, 1e-5)
                while v_ > 1 or v_ < 0:
                    v_ = v + np.random.uniform(0, 1e-5)
                # get sight
                r_ = cam.get_ray(u_, v_)
                # print(r_.time())
                col = col + color(r_, sp_l, 0)
            col = col.div(ns)
            col = vec3(math.sqrt(col.x()), math.sqrt(col.y()), math.sqrt(col.z()))
            ir, ig, ib = int(255.99 * col.x()), int(255.99 * col.y()), int(255.99 * col.z())
            self.args['a'][ny - 1 - j][i * 3], self.args['a'][ny - 1 - j][i * 3 + 1], self.args['a'][ny - 1 - j][i * 3 + 2] = ir, ig, ib
            self.done += 1
            self.args['block'].append((ir, ig, ib))

        #print("id in child:", id(self.args['a']), a.sum())
    def get_time(self):
        return time.time() - self.time_st
    def get_stat(self):
        return (self.done / self.works)
        
        
    