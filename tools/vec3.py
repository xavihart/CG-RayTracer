import math
class vec3:
    def __init__(self, a_, b_, c_):
        self.a = a_
        self.b = b_
        self.c = c_
    def x(self):
        return self.a
    def y(self):
        return self.b
    def z(self):
        return self.c
    def r(self):
        return self.a
    def g(self):
        return self.b
    def b_(self):
        return self.c
    def length(self):
        return math.sqrt(self.a ** 2 +self.b ** 2 + self.c ** 2)
    def squared_length(self):
        return self.a**2 + self.b**2  + self.c**2
    def __add__(self, other):
        return vec3(self.a + other.a, self.b + other.b, self.c + other.c)
    def __sub__(self, other):
        return vec3(self.a - other.a, self.b - other.b, self.c - other.c)
    def __truediv__(self, other):
        return vec3(self.a / other.a, self.b / other.b, self.c / other.c)
    def __mul__(self, other):
        return vec3(self.a * other.a, self.b * other.b, self.c * other.c)
    def mul(self, p):
        return vec3(self.a * p, self.b * p, self.c * p)
    def div(self, p):
        return vec3(self.a / p, self.b / p, self.c / p)
    def make_unit_vector(self):
        p = 1 / self.length()
        self.a *= p
        self.b *= p
        self.c *= p
    def show(self):
        print("[{}, {}, {}]".format(self.a, self.b, self.c))
    def cross(self, other):
        return vec3(self.b * other.c - self.c * other.b, - (self.a * other.c - self.c * other.a), self.a * other.b - self.b * other.a)
    def dot(self, other):
        return self.a * other.a + self.b * other.b + self.c * other.c

if __name__ == "__main__":
    p = vec3(3,4,5)
    print("p:")
    p.show()
    print("len of p:", p.length())
    q = vec3(1,2,3)
    print("q:")
    print("len of q", q.length())
    q.show()
    k=p.mul(2000)
    k.show()
    p.show()
    c = p + q
    c.show()
    c = p - q
    c.show()
    c = p * q
    c.show()
    c = p / q
    c.show()
    c = p.mul(100)
    c.show()
    c = p.div(100)
    c.show()
    t = p.dot(q)
    print("p * q = ", t)
    p.make_unit_vector()
    q.make_unit_vector()
    p.show()
    q.show()
    c = p.cross(q)
    c.show()

    
    

        
