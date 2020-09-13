from .utils import *
from .vec3 import *
from .ray import *
from .hit_list import *
from tools.material import *
from tools.aabb import *
from tools.texture import *
from tools.box import *

def color(r, objs, dep):
    rec = hit_record()
    MAXNUM = 1e9+7
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