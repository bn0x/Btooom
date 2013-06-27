import math

#faster handling of vectors (find a library? (numpy?))

## vector stuff

class Vector2d:
    def __init__(self, *points):
        if len(points) == 2:
            self.x, self.y = points
        elif len(points) == 1:
            self.x, self.y = points[0]

    def squared_length(self):
        return self.x**2+self.y**2

    def get_length(self):
        return self.squared_length()**0.5

    def get_normal(self):
        return Vector2d(-self.y, self.x)

    def __tuple__(self):
        return (self.x, self.y)

    def __repr__(self):
        return str(self.__tuple__())

    def __iter__(self):
        return iter((self.x, self.y))

    def __len__(self):
        return 2

    def arithmetic(self, data, operation):
        for valid_type in (Vector2d, int, float):
            if isinstance(data, valid_type):
                if valid_type in (int, float):
                    return Vector2d(operation(self.x, data), operation(self.y, data))
                elif valid_type is Vector2d:
                    return Vector2d(operation(self.x, data.x), operation(self.y, data.y))
        raise TypeError("Invalid type.")

    def __add__(self, data):
        return self.arithmetic(data, lambda a, b: a + b)

    def __sub__(self, data):
        return self.arithmetic(data, lambda a, b: a - b)

    def __mul__(self, data):
        return self.arithmetic(data, lambda a, b: a * b)

    def __div__(self, data):
        return self.arithmetic(data, lambda a, b: a / b)


def unit_vector(v):
    length = v.get_length()
    if length != 0:
        return Vector2d(v.x / length, v.y / length)
    else:
        return Vector2d(0, 0)

    
def dot_product(v1, v2):
    return v1.x * v2.x + v1.y * v2.y


def scalar_projection(v1, v2):
    uv2 = unit_vector(v2)
    return dot_product(v1, uv2)


def mirror_vector(x, b):
    """ mirrors v1 around v2 """
    v = b.get_normal()
    r = 2 * dot_product(x, v) / dot_product(v, v)

    mirrored = x - v * r
    return mirrored


def get_quadrant(v):
    x, y = v.x, v.y

    if x >= 0:
        if y >= 0:
            return 1
        else:
            return 4
    else:
        if y >= 0:
            return 2
        else:
            return 3


## vector stuff done

def get_angle(v):
    if v[0] == 0:
        if v[1] > 0:
            v_a = math.pi/2
        else:
            v_a = 2*math.pi-math.pi/2
    else:
        v_a = math.atan(v[1]/v[0])
        if v[0] < 0:
            v_a += math.pi

    return v_a
