import pygame
from pygame.locals import *
from detection import Polygon
from response import Actor
from math import degrees, sin, cos
from mathsupp import get_angle, Vector2d, unit_vector
from time import sleep
from time import clock as tclock
from convex_hull import jarvis_march
from quadtree import QuadtreeR2


def recur_draw_qtree(node, surf):
    if node.children == None:
        r = node.rect
        rect = pygame.Rect(r.left, r.top, r.w, r.h)
        pygame.draw.rect(surf, (200, 200, 200), rect, 2)
    else:
        for child in node.children:
            recur_draw_qtree(child, surf)

def draw_qtree(qtree, surf):
    recur_draw_qtree(qtree.firstnode, surf)
    r = qtree.firstnode.rect
    rect = pygame.Rect(r.left, r.top, r.w, r.h)
    pygame.draw.rect(surf, (200, 200, 200), rect, 2)


def gen_poly(p1, p2, height):
    v1, v2 = Vector2d(p1), Vector2d(p2)
    
    v = v1-v2
    n = v.get_normal()
    u = unit_vector(n)

    t = u * height

    q1 = v1+t
    q2 = v1-t
    q3 = v2+t
    q4 = v2-t

    points = list(i.__tuple__() for i in (q1, q2, q3, q4))

    return Polygon(points=jarvis_march(points))

            
class testing_facilities:
    """ used for debugging """
    def __init__(self, test):
        pygame.init()
        self.w, self.h = 1200, 700
        self.surf = pygame.display.set_mode((self.w, self.h))

        self.clock, self.fps = pygame.time.Clock(), 60

        self.fill_color = (0, 0, 0)

        if test == "test 1":
            self.test1()
            self.update = self.update1
            self.draw = self.draw1

    def test1(self):
        polypoints1 = ((10, 10), (20, 20), (10, 40), (0, 20))
        #polypoints2 = ((0, 0), (0, 0.1), (1, 0.1), (1, 0.1))
        polypoints2 = ((0, 0), (0, 0.1), (1, 0.1), (1, 0))
        polypoints3 = ((0, 0), (0, 800), (100, 800), (100, 0))
        square_points = ((0,0),(50,0),(50,50),(0,50))
        
        s = 20
        polypoints1 = list(map(lambda p: (p[0]*s,p[1]*s), polypoints1))
        s = 600
        polypoints2 = list(map(lambda p: (p[0]*s,p[1]*s), polypoints2))
        
        self.polygon1 = Polygon(points=square_points)        
        self.polygon2 = Polygon(pos=(0, 500), points=polypoints2)
        self.polygon3 = Polygon(pos=(700, 0), points=polypoints3)
        self.polygon4 = Polygon(pos=(0, -200), points=polypoints1)

        f = 50
     #   worldx, worldy = 100*f, 100*f
        #self.qtree = QuadtreeR2(worldx, worldy)
        
        self.world = [self.polygon2, self.polygon3, self.polygon4]
        self.draw_polys = [self.polygon2, self.polygon3, self.polygon4]

      #  n = 0
      #  for x in range(10, 15):
        #    for y in range(10, 15):
           #     poly = Polygon(pos=(x*f,y*f),points=polypoints3)
            #    self.world.append(poly)
             #   self.qtree.add_collidable(poly)
            #    print(n)
            #    n += 1

        

      #  print(len(self.world))
       # self.world = [self.polygon2]

        self.player = Actor((0, 0), self.polygon1, self.world)


        self.targets = [(0,0), (0,0)]
        self.selected = 0

    def main(self):
        while True:
            self.update()
            
            self.draw()
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.clock.tick(self.fps)

    def update1(self):
        self.player.update()

        x = 0
        if pygame.key.get_pressed()[K_a]:
            x -= 1
        if pygame.key.get_pressed()[K_d]:
            x += 1
            
        if pygame.key.get_pressed()[K_w] and self.player.contact.incontact:
            self.player.jump()

        s = 15
        self.player.mech.add_impulse(x * s, 0)
 

        if pygame.mouse.get_pressed()[0]:
            self.player.mech.velocity.x, self.player.mech.velocity.y = 0, 0
            mpos = pygame.mouse.get_pos()
            self.player.move_to(*mpos)
            self.player.move_mech_to(*mpos)

            self.targets[self.selected] = (mpos[0], mpos[1])
            

        if self.player.pos[1] > self.h + 100:
            pos = self.player.pos[0], -100
            self.player.move_to(*pos)
            self.player.move_mech_to(*pos)

        if not (-100 < self.player.pos[0] < self.w + 100):
            pos = (100+self.w)-abs(self.player.pos[0]), self.player.pos[1]
            self.player.move_to(*pos)
            self.player.move_mech_to(*pos)


        if pygame.key.get_pressed()[K_t]:
            self.selected = 1 - self.selected
            print(self.selected)
            sleep(0.5)

        if pygame.key.get_pressed()[K_p]:
            poly = gen_poly(self.targets[0], self.targets[1], 10)
            self.world.append(poly)
            sleep(0.5)
        

    def draw1(self): 
        self.surf.fill(self.fill_color)

        red, blue = (255, 0, 0), (0, 0, 255)
        green = (0, 255, 0)
        white = (255, 255, 255)
        gray = (100, 100, 100)

        pygame.draw.circle(self.surf, green, self.targets[0], 5, 2)
        pygame.draw.circle(self.surf, red, self.targets[1], 5, 2)
        
        pygame.draw.polygon(self.surf, white, self.polygon1.get_points())

        
        for poly in self.draw_polys:
            pygame.draw.polygon(self.surf, blue, poly.get_points())

       # draw_qtree(self.qtree, self.surf)

if __name__ == "__main__":
    tests = testing_facilities("test 1")
    tests.main()

