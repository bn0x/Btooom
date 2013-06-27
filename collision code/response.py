from mathsupp import *
from detection import *
from response import *
from mechanics import Physics, GRAVITY


def distance(polygon_points, point):
    """ finds minimum distance to every side.
        takes the shortest resulting vector. """

    P = Vector2d(point)
    PZ = Vector2d(1000000, 1000000)
    for i in range(len(polygon_points)):
        Q = Vector2d(polygon_points[i])
        V = Vector2d(polygon_points[i-1])

        QV = V - Q
        QP = P - Q

        u = unit_vector(QV)
        d = dot_product(QP, u)
        Z = Q + u * d

        PZ_temp = P - Z

        if PZ_temp.squared_length() < PZ.squared_length():
            PZ = PZ_temp
            side = QV

    return PZ, side


def penetration_vector(polygon_points, point):
    return distance(polygon_points, point)[0]


def collision_info(polygon_points, velocity):
    """ gets side that polygon penetrated.
        returns a unit vector parallel to
        the side """

    pos = -velocity[0], -velocity[1]
    adjusted_pp = list(map(lambda p: (p[0]+pos[0], p[1]+pos[1]), polygon_points))
    origin = (0, 0)
    d, v = distance(adjusted_pp, origin)

    return d, v
    

class Bounce_Contact:
    def __init__(self):
        self.history = []
        self.bounces = []

    def update(self, contact):
        self.history.append(contact)
        
        if len(self.history) == 3:
            self.history.pop(0)

    def in_contact(self):
        if len(self.history) < 2:
            return False
        return all(self.history)

    def add_bounce(self, bounce):
        self.bounces.append(bounce)

    def get_bounce(self):
        if not self.in_contact():
            if len(self.bounces) != 0:
                return self.bounces.pop()
        return 1


class Distance_Contact:
    def __init__(self):
        self.incontact = False
        self.edge = 0, 0
        self.normal = 0, 0
        self.collidable = None

    def break_contact(self):
        self.incontact = False

    def new_contact(self, edge, normal, collidable):
        self.edge = edge
        self.normal = normal
        self.collidable = collidable
        self.incontact = True
        

class Actor:
    def __init__(self, pos, collidable, world):
        self.pos = pos
        self.collidable = collidable
        self.mech = Physics(pos, 10, (0, 0))
        self.contact = Distance_Contact()
        self.world = world

    def move_to(self, x, y):
        self.pos = x, y
        self.collidable.set_pos(x, y)

    def move_mech_to(self, x, y):
        self.mech.pos.x = x
        self.mech.pos.y = y

    def move(self, dx, dy):
        self.pos = self.pos[0]+dx, self.pos[1]+dy
        self.collidable.move(dx, dy)

    def move_mech(self, dx, dy):
        self.mech.pos.x += dx
        self.mech.pos.y += dy


    def nearby_collidables(self):
        return self.world


    def update(self):
        self.mech.update()

        if self.contact.incontact:
            u = unit_vector(self.contact.edge)
            d = dot_product(self.mech.velocity, u)

            self.mech.pos -= self.mech.velocity
            self.mech.velocity = u * d
            self.mech.pos += self.mech.velocity

            n = self.contact.normal
            self.collidable.move(-n.x, -n.y)
            status, poly_pts = collision(self.collidable, self.contact.collidable)
            if not status:
                self.contact.break_contact()
            else:
                pass#self.mech.add_impulse(0, -9.81)
            self.collidable.move(n.x, n.y)
            

        v = self.mech.velocity.__tuple__()
        p = self.mech.pos.__tuple__()
        
        self.move_to(*p)

        for c in self.nearby_collidables():
            status, polygon_points = collision(self.collidable, c)
            
            if status == True:
                self.resolve_collision(polygon_points, p, v, c, "slide")
        

    def resolve_collision(self, polygon_points, p, v, c, mechanic):
        pen_vector = penetration_vector(polygon_points, (0, 0))
        d, v = collision_info(polygon_points, v)

        self.move(*pen_vector)
        self.move_mech(*pen_vector)

        
        if mechanic == "slide":
            self.contact.new_contact(v, pen_vector, c)
        elif mechanic == "bounce":
            self.mech.velocity = mirror_vector(self.mech.velocity, v)
            


    def jump(self):
        self.contact.break_contact()
        
        u = unit_vector(self.contact.edge)

        normal = u.get_normal()
        avg = u * 0.5 + normal * 0.5

        
        jvect = avg * -u.y + normal * -u.x

        print(jvect)

   #    if 


        self.mech.velocity = jvect * GRAVITY * 0.5 + self.mech.velocity * 0.5

    

#todo:
        
#smooth mechanics;
#proper jumping 
#fix sliding
#introduce stable bumping mechanics
#friction with surfaces

#etc;
#fix collisions with multiple (2-3) objects

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

    status, poly_points = collision(A, B)

    a1 = clock()
    for i in range(runs):
        penetration_vector(poly_points, (0,0))
        collision_info(poly_points, (-200, -200))
    a2 = clock()

    num_coll = runs/(a2-a1)

    print("calculated", num_coll, "calls to each essential response function per sec")


