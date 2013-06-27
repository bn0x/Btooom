from mathsupp import *
from convex_hull import make_polygon

#important;
#fix polygon and rect classes, lay them out more logically


#deal with;
#collisions between two moving objects
#crowd collisions / multiple collisions (more than 3)
#(these are more long term)

#optimizations;
#optimized collision tree; quadtree <-- possibly redundant
#computing "blueprint polygons" for every set of polygons that might collide


def farthest_point_along_vector(points, v):
    """ finds the point that is farthest
        projected along a vector """

    unit_v = unit_vector(Vector2d(v))
    farthest = points[0]
    farthest_length = dot_product(Vector2d(points[0]), unit_v)
    
    for i in range(1, len(points)):
        p = dot_product(Vector2d(points[i]), unit_v)    
        if p > farthest_length:
            farthest = points[i]
            farthest_length = p

    return farthest


class Rect2:
    def __init__(self, left, top, w, h):
        self.left, self.top = left, top
        self.w, self.h = w, h
        self.right = self.left + w
        self.bottom = self.top + self.h
    
    def move_to(self, x, y):
        self.left = self.left + x
        self.top = self.top + y

        self.right = self.left + self.w
        self.bottom = self.top + self.h
        
        
class Polygon:
    """ a class for handling polygons """
    def __init__(self, pos = None, points = None):
        if pos == None:
            pos = (0, 0)
        if points == None:
            points = []
            
        self.pos = pos
        self.points = points

        self.is_convex = True

        self.left = farthest_point_along_vector(points, (-1, 0))[0]
        self.right = farthest_point_along_vector(points, (1, 0))[0]
        self.top = farthest_point_along_vector(points, (0, -1))[1]
        self.bottom = farthest_point_along_vector(points, (0, 1))[1]

        self.rect = Rect2(self.left, self.top, self.right-self.left, self.bottom-self.top)
        #used for bounding boxes


    def move(self, dx, dy):
        self.pos = self.pos[0]+dx, self.pos[1]+dy

    def set_pos(self, x, y):
        self.pos = x, y

    def get_points(self):
        return list(map(lambda p: (p[0]+self.pos[0], p[1]+self.pos[1]), self.points))

    def get_centerpoint(self):
        a = len(self.points)
        s = 0, 0
        for i in self.get_points():
            s = i[0]+s[0], i[1]+s[1]

        return s[0]/a, s[1]/a

    def get_rect(self):
        x, y = self.pos
        new_rect = Rect2(self.rect.left, self.rect.top, self.rect.w, self.rect.h)
        new_rect.move_to(x, y)
        return new_rect
            
    
def minkowski_difference(A, B):
    for p1 in B:
        for p2 in A:
            yield p2[0]-p1[0], p2[1]-p1[1]

    
def point_polygon_coll(point, points):
    """ test if a point is inside
        of a polygon formed by the vertices of
        points"""
    nvert = len(points)
    testx, testy = point
    j = nvert-1
    c = False
    for i in range(nvert):
        if ( ((points[i][1]>testy) != (points[j][1]>testy)) and \
             (testx < (points[j][0]-points[i][0]) * (testy-points[i][1]) \
              / (points[j][1]-points[i][1]) + points[i][0]) ):
            c = True - c
        
        j = i

    return c


def simple_GJK(A, B):
    """ an unoptimized pseudo-version of the GJK collision algorithm """
    diff = list(minkowski_difference(A, B))
    polygon_points = make_polygon(diff)

    origin = 0, 0
    if point_polygon_coll(origin, polygon_points):
        return True, polygon_points
    return False, polygon_points


def rect_rect(Ra, Rb):
    if Ra.top > Rb.bottom or Rb.top > Ra.bottom or Ra.left > Rb.right or Rb.left > Ra.right:
        return False
    return True


def collision(A, B):
    """ checks collisions between various shapes """
    if rect_rect(A.get_rect(), B.get_rect()):
        if A.is_convex and B.is_convex:
            return simple_GJK(A.get_points(), B.get_points())
    return False, tuple()


if __name__ == "__main__":
    from time import clock
    #benchmarking
    points = [(-10, -10), (-10, 790), (90, 790), (90, -10), \
              (-20, -20), (-20, 780), (80, 780), (80, -20), \
              (-10, -40), (-10, 760), (90, 760), (90, -40), \
              (0, -20), (0, 780), (100, 780), (100, -20)]

    A = Polygon(pos=(100,100), points=points)
    B = Polygon(pos=(100,200), points=points)

    runs = 5000

    a1 = clock()
    for i in range(runs):
        rect_rect(A.get_rect(), B.get_rect())
    a2 = clock()

    num_coll = runs/(a2-a1)

    print("rect-rect")
    print("calculated", num_coll, "collisions per sec")
    
    runs = 5000

    a1 = clock()
    for i in range(runs):
        collision(A, B)
    a2 = clock()

    num_coll = runs/(a2-a1)

    print("polygon-polygon")
    print("calculated", num_coll, "collisions per sec")

    p = (50, 300)

    runs = 5000

    a1 = clock()
    for i in range(runs):
        point_polygon_coll(p, points)
    a2 = clock()

    num_coll = runs/(a2-a1)

    print("point-polygon")
    print("calculated", num_coll, "collisions per sec")



