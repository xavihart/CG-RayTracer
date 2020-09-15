from tools.utils import *
from tools.vec3 import *
from tools.ray import *
from tools.hit_list import *
from tools.camera import *
from tools.material import *
from tools.aabb import *
from tools.texture import *
from tools.box import *
from tools.Myprocess import myProcess
import threadpool
import numpy as np
import sys
import os
import time
import argparse
from tqdm import tqdm
import multiprocessing as ml

parser = argparse.ArgumentParser()
parser.add_argument("--r", default=100, type=int, help="the resolution of the image generated")
parser.add_argument("--ns", default=1, type=int, help="iteration times for background diffusion")
parser.add_argument("--name", default="light2", type=str, help="set the name for saving the image")
parser.add_argument("--scene", type=str, default="2ball", help="scene to generate, e.g. cornellbox, 2-balls, final...")
parser.add_argument("--multithread", default = "on", type=str, help="if open the threadpool and support ms")
parser.add_argument("--threadnum", default = 100, type=int, help="set the name for saving the image")
parser.add_argument("--show-freq", default = 10, type = int, help = "the frequency to show the process on the screen")
parser.add_argument("--block-num", default = 100, type = int, help = "the block numbers used for multi-thread")

args = parser.parse_args()
h = args.r
MAXNUM = 1e9
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
a = np.zeros([h, 2*h*3])
b = np.ones([h, 2*h])
time_st = time.time()
ny, nx = a.shape[0], a.shape[1] // 3
done_num = 0
print("NOTE: The resolution of your image is:[{} * {}]".format(h, h * 2))


def two_spheres():
    checker = checker_texture(constant_texture(vec3(0.2, 0.3, 0.1)), constant_texture(vec3(0.9, 0.9, 0.9)))
    l = []
    l.append(sphere(vec3(0, -10, 0), 10, lambertian(checker)))
    l.append(sphere(vec3(0, 10, 0), 10, lambertian(checker)))
    return l
def two_spheres_perlin():
    tex = noise_texture(3)
    l = []
    l.append(sphere(vec3(0, -1000, 0), 1000, lambertian(tex)))
    l.append(sphere(vec3(0, 2, 0), 2, lambertian(tex)))
    return l
def two_spheres_texture_mapping():
    pixels, shape = image_flatten("./earth.JPG")
    h, w = shape[0], shape[1]
    tex = image_texture(pixels, h, w)
    tex2 = noise_texture(3)
    l = []
    l.append(sphere(vec3(0, -1000, 0), 1000, lambertian(tex2)))
    l.append(sphere(vec3(0, 2, 0), 2, lambertian(tex)))
    return l

def two_spheres_with_lightenning_rect():
    tex = noise_texture(4)
    l = []
    pixels, shape = image_flatten("./earth.JPG")
    h, w = shape[0], shape[1]
    tex_image = image_texture(pixels, h, w)
    l.append(sphere(vec3(0, -1000, 0), 1000, lambertian(tex)))
    l.append(sphere(vec3(0, 2, 0), 2, lambertian(tex)))
    #l.append(sphere(vec3(0, 7, 0), 2, diffuse_light(constant_texture(vec3(4,4,4)))))
    #l.append(xy_rect(3, 5, 1, 3, -2, diffuse_light(constant_texture(vec3(4,4,4)))))
    return l

def cornell_box():
    l = []
    red = lambertian(constant_texture(vec3(0.65, 0.05, 0.05)))
    white = lambertian(constant_texture(vec3(0.73, 0.73, 0.73)))
    green = lambertian(constant_texture(vec3(0.12, 0.45, 0.15)))
    light =  diffuse_light(constant_texture(vec3(4, 4, 4)))

    l.append(flip_normals(yz_rect(0, 555, 0, 555, 555, green)))
    l.append(yz_rect(0, 555, 0, 555, 0, red)) # 
    l.append(xz_rect(100, 400, 100, 400, 554, light))
    l.append(flip_normals(xz_rect(0, 555, 0, 555, 555, white)))
    l.append(xz_rect(0, 555, 0, 555, 0, white))
    l.append(flip_normals(xy_rect(0, 555, 0, 555, 555, white)))
    l.append(rotate_y(box(vec3(130, 0, 65), vec3(295, 165, 230), white), -60))
    l.append(rotate_y(box(vec3(265, 0, 295), vec3(430, 330, 460), white), 40))
    return l


def next_week_finals():
    # to do
    return 


def generate_random_spheres():
    """
    using methods from the book 11 * 11 grids
    return sphere list
    """

    obj_list = []
    n = 5
    # cen_list.append(vec3(0, -1000, 0))
    # rad_list.append(1000)
    # mat_list.append(lambertian(vec3(0.5, 0.5, 0.5)))
    checker = checker_texture(constant_texture(vec3(0.2, 0.3, 0.1)), constant_texture(vec3(0.9, 0.9, 0.9)))
    obj_list.append(sphere(vec3(0, -1000, 0), 1000, lambertian(checker)))
    for a in range(-n, n):
        for b in range(-n, n):
            p = np.random.uniform(0, 1)
            cent = vec3(a + 0.9 * np.random.uniform(0, 1), 0.2, b + np.random.uniform(0, 1))
            if (cent - vec3(4, 0.2, 0)).length() > 0.9:
                if p < 0.8:
                    # cen_list.append(cent)
                    # rad_list.append(0.2)
                    vp = vec3(np.random.uniform(0, 1) ** 2, np.random.uniform(0, 1) ** 2, np.random.uniform(0, 1) ** 2)
                    m = lambertian(constant_texture(vp))
                    # moving.append[1]
                    cent_end = cent + vec3(0, 0.5 * np.random.uniform(0, 1), 0)
                    obj_list.append(moving_sphere(cent, cent_end, 0, 1, 0.2, m))
                elif p < 0.95:
                    #moving.append(0)
                    #cen_list.append(cent)
                    #rad_list.append(0.2)
                    mat = metal(vec3((np.random.uniform(0, 1) + 1 ) / 2 , (np.random.uniform(0, 1) + 1 ) / 2, (np.random.uniform(0, 1) + 1 ) / 2), \
                        np.random.uniform(0, 1) * 0.5)
                    obj_list.append(sphere(cent, 0.2, mat))
                else:
                    # moving.append(0)
                    # cen_list.append(cent)
                    # rad_list.append(0.2)
                    # mat_list.append(dielectric(1.5))
                    obj_list.append(sphere(cent, 0.2, dielectric(1.5)))
    cen_list, rad_list, mat_list = [], [], []
    cen_list += [vec3(0, 1, 0), vec3(-4, 1, 0), vec3(4, 1, 0)]
    rad_list += [1, 1, 1]
    mat_list += [dielectric(1.5), lambertian(constant_texture(vec3(0.4, 0.2, 0.1))), metal(vec3(0.7, 0.6, 0.5), 0.0)]
    for i in range(len(cen_list)):
        obj_list.append(sphere(cen_list[i], rad_list[i], mat_list[i]))
    
    return obj_list
    

def hit_sphere(c, rad, r):
    """
    c : vec3, center 
    r : float, radius
    r : ray
    """
    oc = r.origin() - c
    a = r.direction()
    a = a.dot(a)
    b = 2 * oc.dot(r.direction()) 
    c = oc.dot(oc) - rad * rad
    disc =  b*b - 4*a*c
    if disc <  0:
        return -1
    else:
        return (-b - math.sqrt(disc)) / (2 * a)



'''
def color1(r, obj):
    """
    param:
    r : ray 
    obj : hitable object list ,a list of sphere for example
    """
    hit_rec = hit_record(0, 0, vec3(0, 0, 0))
    (hit_rec, f) = obj.hit(r, 0.0001, 1e9 + 7)
    if f:
        #hit_rec.normal.show()
        #return vec3(hit_rec.normal.x()+1, hit_rec.normal.y()+1, hit_rec.normal.z()+1).mul(0.5)
        tar = hit_rec.p + hit_rec.normal + random_unit_sphere()
        return color(ray(hit_rec.p, tar - hit_rec.p), obj).mul(0.5)
    else:
        unit_dir = r.direction()
        unit_dir.make_unit_vector()
        t = 0.5 * (unit_dir.y() + 1)
        return vec3(1 ,1, 1).mul(1 - t) + vec3(0.5, 0.7, 1.0).mul(t)
'''

def color(r, objs, dep):
    rec = hit_record()
    (rec, f) = objs.hit(r, 0.0001, MAXNUM)
    # r.direction().show()
    if f:
        attenuation = vec3()
        scattered = ray()
        # print("#####################2")
        args = {'rec':rec, 'attenuation':attenuation, 'scattered':scattered}
        argsrec =args['rec']
        emit = args['rec'].mat.emitted(argsrec.u, argsrec.v, argsrec.p)
        if dep < 20 and rec.mat.scatter(r, args):
            return emit + color(args['scattered'], objs, dep + 1) * args['attenuation']
        else:
            return emit
    else:
        unit_dir = r.direction()
        # print("#####################")
        # r.direction().show()
        unit_dir.make_unit_vector()
        t = 0.5 * (unit_dir.y() + 1)
        # print(t)
        return vec3(1 ,1, 1).mul(1 - t) + vec3(0.5, 0.7, 1.0).mul(t)
        """
        # black bkg
        return vec3(0, 0, 0)
        """
    
def color_function_thread_pixel(i, j, cam, sp_l):
    """s
    param:
    i, j :  the indexes for the pixel
    cam : camera instance
    sp_l : sphere_list instance
    return : none, change values of matrix "a"
    """
    global nx
    global ny
    global args
    u = i / nx
    v = j / ny
    col = vec3(0, 0, 0)
    ns = args.ns
    for _ in range(ns):
        u_, v_ = -1, -1
        while u_ > 1 or u_ < 0:
            u_ = u + np.random.uniform(0, 1e-4)
        while v_ > 1 or v_ < 0:
            v_ = v + np.random.uniform(0, 1e-4)
        # get sight
        r_ = cam.get_ray(u_, v_)
        # print(r_.time())
        col = col + color(r_, sp_l, 0)
    col = col.div(ns)
    col = vec3(math.sqrt(col.x()), math.sqrt(col.y()), math.sqrt(col.z()))
    ir, ig, ib = int(255.99 * col.x()), int(255.99 * col.y()), int(255.99 * col.z())
    a[ny - 1 - j][i * 3], a[ny - 1 - j][i * 3 + 1], a[ny - 1 - j][i * 3 + 2] = ir, ig, ib
    global done_num
    done_num += 1
    if done_num % args.show_freq == 0:
        print("[{}/{}] --- ({}%%)".format(done_num, nx * ny, done_num/nx/ny))
    return 

def color_function_thread_pixel_list(pixel_list, cam, sp_l):
    """
    pixel_list: list like [[x1,y1], [x2, y2]]
    """
    times = time.time()
    x_list = [i[0] for i in pixel_list]
    y_list = [i[1] for i in pixel_list]
    assert len(x_list) == len(y_list)
    for p in range(len(pixel_list)):
        x, y = x_list[p], y_list[p]
        u = x / nx
        v = y / ny
        i, j = x, y
        col = vec3(0, 0, 0)
        ns = args.ns
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
        global a, b
        a[ny - 1 - j][i * 3], a[ny - 1 - j][i * 3 + 1], a[ny - 1 - j][i * 3 + 2] = ir, ig, ib
        b[y][x] = 0
        global done_num
    done_num += 1
    print("time:", time.time() - times)
    return 
  
    
def main_multithread():
    # set scene and cam
    aperture = 0
    time_st = time.time()
    if args.scene == "2ball":
        look_from = vec3(13, 4, 2)
        look_at = vec3(0, 1, 0)
        dist_to_focus = 10
    elif args.scene == "cornellbox":
        look_from = vec3(278, 278, -800)
        look_at = vec3(278, 278, 0)
        dist_to_focus = 10
        
 
    cam = camera(look_from, look_at, vec3(0, 1, 0), 40, nx / ny, aperture, dist_to_focus, 0, 1)    
    
    if args.scene == "2ball":
        l = two_spheres_with_lightenning_rect()
    elif args.scene == "cornellbox":
        l = cornell_box()
    elif args.scene == "final1":
        l = generate_random_spheres()
    print("You generated {} objects at all".format(len(l)))
    sp_l = sphere_list(l)
    ## multithread part
    taskpool = threadpool.ThreadPool(args.threadnum)
    ## generate the param dir : [(None, {'i':, 'j':, 'cam':, 'sp_l':}), {}, {}]  
    args_list = []
    plist = []
    for i in tqdm(range(nx)):
        for j in range(ny-1, -1, -1):
            plist.append([i, j])
    plist = np.array(plist)
    plist = np.random.permutation(plist)
    plist = np.split(plist, args.block_num, axis=0)
    for i in range(len(plist)):
        d = {}
        d['pixel_list'] = plist[i]
        d['cam'] = cam
        d['sp_l'] = sp_l
        args_list.append((None, d))
    
    # create the threadpool
    t1  = time.time()
    req = threadpool.makeRequests(color_function_thread_pixel_list, args_list)
    t2 = time.time()
    [taskpool.putRequest(r) for r in req]
     
    taskpool.wait()    
    ## to do
    ## [pool.putRequest(r) for r in requests]
    ## pool.wait()
    print("pooling timecsm", (time.time() - t2)/60)
    save_ppm(file_pth, a)
    time_ed = time.time()
    print("Time consm:", (time_ed - time_st) / 60, "min")
    print(b.sum())
    return 

def main_multiprocess(args):
    # set scene and cam
    aperture = 0
    time_st = time.time()
    if args.scene == "2ball":
        look_from = vec3(13, 4, 2)
        look_at = vec3(0, 1, 0)
        dist_to_focus = 10
    elif args.scene == "cornellbox":
        look_from = vec3(278, 278, -800)
        look_at = vec3(278, 278, 0)
        dist_to_focus = 10
    elif args.scene == "final1":
        aperture = 0
        dist_to_focus = 10
        look_from = vec3(3, 2, 3)
        look_at = vec3(0, 0, -1)

    cam = camera(look_from, look_at, vec3(0, 1, 0), 40, nx / ny, aperture, dist_to_focus, 0, 1)    
    if args.scene == "2ball":
        l = two_spheres_with_lightenning_rect()
    elif args.scene == "cornellbox":
        l = cornell_box()
    elif args.scene == "final1":
        l = generate_random_spheres()
    print("You generated {} objects at all".format(len(l)))
    sp_l = sphere_list(l)
    ## multiprocess part
    blocks=[]
    with ml.Manager() as MG:
        # color block
        for i in range(args.block_num):
           blocks.append(ml.Manager().list([]))
    plist = []
    for i in tqdm(range(nx)):
        for j in range(ny-1, -1, -1):
            plist.append([i, j])
    plist = np.array(plist)
    plist = np.random.permutation(plist)
    plist = np.split(plist, args.block_num, axis=0)
    process_list = []
    for i in range(len(plist)):
        d = {}
        d['pixel_list'] = plist[i]
        d['cam'] = cam
        d['sp_l'] = sp_l
        d['a'] = a
        d['block'] = blocks[i]
        d['nx'] = nx
        d['ny'] = ny
        d['ns'] = args.ns
        process_list.append(myProcess(d))
    alive_number = len(process_list)
    
    for i in range(len(process_list)):
        process_list[i].start()
    print("id in main", id(a))
    timer = 0
    """
    while alive_number != 0:
        t = 0
        done = 0
        for p in process_list:
            done += p.get_stat()
            if p.is_alive():
                t += 1
        done /= len(process_list)
        if t < alive_number:
            print("done ++ -> {}", len(process_list) - t)
        alive_number = t
    """
    for i in range(len(process_list)):
        process_list[i].join()
    time_ed = time.time()
    
    #for p in process_list:
     #   p.join()
    for i_ in range(args.block_num):
        for j_, item in enumerate(blocks[i_]):
             i, j = plist[i_][j_][0], plist[i_][j_][1]
             ir, ig, ib = item[0], item[1], item[2] 
             a[ny - 1 - j][i * 3], a[ny - 1 - j][i * 3 + 1], a[ny - 1 - j][i * 3 + 2] = ir, ig, ib     

    #print(a.sum())
    save_ppm(file_pth, a)
    print("Time consm:", (time_ed - time_st) / 60, "min")
    
    return 


def main():
    #lower_left_corner = vec3(-2, -1, -1)
    
    aperture = 0
    """ two green grid spheres
    look_from = vec3(13, 2, 3)
    look_at = vec3(0, 0, 0)
    dist_to_focus = 10
    """
    
     #for cornell box 
    #look_from = vec3(278, 278, -800)
    #look_at = vec3(278, 278, 0)
    #dist_to_focus = 10
    
    if args.scene == "2ball":
        look_from = vec3(13, 4, 2)
        look_at = vec3(0, 1, 0)
        dist_to_focus = 10
    elif args.scene == "cornellbox":
        look_from = vec3(278, 278, -800)
        look_at = vec3(278, 278, 0)
        dist_to_focus = 10
    if args.scene == "final1": 
        aperture = 2
        look_from = vec3(3, 2, 3)
        look_at = vec3(0, 0, -1)
        dist_to_focus = 10
    cam = camera(look_from, look_at, vec3(0, 1, 0), 40, nx / ny, aperture, dist_to_focus, 0, 1)    
    
    
    ns = args.ns
    l = []
    ## sphere properties list
    #l = two_spheres_texture_mapping()
    # assert len(sphere_cen) == len(sphere_mat) and len(sphere_cen) == len(sphere_rad)
    
    if args.scene == "2ball":
        l = two_spheres_with_lightenning_rect()
    elif args.scene == "cornellbox":
        l = cornell_box()
    elif args.scene == "final1":
        l = generate_random_spheres()

    print("You generated {} objects at all".format(len(l)))

    # for i in range(len(sphere_mat)):
    #   l.append(sphere(sphere_cen[i], sphere_rad[i], sphere_mat[i]))
    
    sp_l = sphere_list(l)
    cnt = 0
    for i in tqdm(range(nx)):
        for j in range(ny-1, -1, -1):
            u = i / nx
            v = j / ny
            col = vec3(0, 0, 0)
            # background diffusion
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
            # gamma repair
            col = col.div(ns)
            col = vec3(math.sqrt(col.x()), math.sqrt(col.y()), math.sqrt(col.z()))
            if col.length() != 0:
                #col.show()
                cnt += 1
            ir, ig, ib = int(255.99 * col.x()), int(255.99 * col.y()), int(255.99 * col.z())
           # if ir != 0 or ig != 0 or ib != 0:
           #     print("gg")
            a[ny - 1 - j][i * 3], a[ny - 1 - j][i * 3 + 1], a[ny - 1 - j][i * 3 + 2] = ir, ig, ib
    # save image as *.ppm 
    save_ppm(file_pth, a)
    time_ed = time.time()
    print("Time consm:", (time_ed - time_st) / 60, "min")
    print(cnt)


if __name__ == "__main__":
    save_path = "./results/9-13"
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    file_pth = os.path.join("./results/9-13", "{}.ppm".format(args.name))

    if args.multithread == "off":
        print("you are now using single thread to run, may be slower")
        main()
    elif args.multithread == "on":
        print("you are now using multithread")
        main_multiprocess(args)
    else:
        print("param error" + "-" * 15)