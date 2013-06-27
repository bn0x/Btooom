from detection import rect_rect, Rect2

##REDO

class QuadtreeR2:
    def __init__(self):
        self.l = []

    def add_moving_collidable(self, c):
        self.l.append(c)

    def clear_moving_collidables(self):
        self.l = []
