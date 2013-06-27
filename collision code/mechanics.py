from mathsupp import Vector2d

GRAVITY = 9.81 * 3

class Physics:
    def __init__(self, pos, mass, velocity, const_forces = (Vector2d(0, GRAVITY),), max_speed_squared = 400):
        self.pos = Vector2d(pos[0], pos[1])
        self.mass = mass
        self.velocity = Vector2d(velocity[0], velocity[1])
        self.const_forces = const_forces
        self.forces = []
        self.impulses = []

        self.max_speed_squared = max_speed_squared

        self.dt = 0.2

    def add_impulse(self, x, y):
        self.impulses.append(Vector2d(x, y))

    def add_force(self, x, y):
        self.forces.append(Vector2d(x, y))

    def sum_of_forces(self, *force_lists):
        sumof = Vector2d(0, 0)
        for i in force_lists:
            for n in i:
                sumof += n
        return sumof

    def change_in_pos(self):
        return self.change_in_velocity() + self.velocity
        
    def change_in_velocity(self):
        a = self.get_acceleration()
        t = self.dt
        dv = Vector2d(t * a.x, t * a.y)
        if (dv + self.velocity).squared_length() <= self.max_speed_squared:
            return dv
        return Vector2d(0, 0)

    def get_acceleration(self):
        return self.sum_of_forces(self.const_forces, self.forces, self.impulses) * (1/self.mass)

    def update(self):
        d = self.change_in_pos()
        self.pos = d + self.pos
        self.velocity = d
        self.impulses = []

