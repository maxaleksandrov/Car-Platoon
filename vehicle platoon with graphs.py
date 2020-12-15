import numpy as np
from matplotlib import pyplot as plt

period = 1 / 60
mu = 0.2
g = 9.8


class LEADCAR:
    def __init__(self, v, x, f, m, acceleration, deceleration, moving):
        self.v = v
        self.f = f
        self.m = m
        self.a = (self.f - self.m * mu * g) / self.m
        self.acceleration = acceleration
        self.deceleration = deceleration
        self.pos = x
        self.moving = moving

    def update(self):
        if self.moving:
            if self.acceleration:
                self.v += self.a
                self.pos += self.v
            elif self.deceleration:
                self.v -= self.a
                self.pos += self.v
            else:
                self.pos += self.v
        else:
            self.pos = self.pos

    def distance(self):
        return self.pos

    def speed(self):
        return self.v


class FOLLOWERCAR:
    def __init__(self, v, x, D, d):
        self.v = v
        self.vel = v
        self.D = D
        self.pos = x
        self.d = d

    def update(self):
        dis = abs(self.pos - self.d)
        if dis == self.D:
            self.pos += self.v
        else:
            self.v += (dis - self.D)
            self.pos += self.v

    def distance(self):
        return self.pos

    def speed(self):
        return self.v


def update_model(max_count, v_0, gap, n):
    pos_lead = []
    pos_fol = []
    vel_lead = []
    vel_fol = []
    pos_diff = []
    vel_diff = []
    count = 1
    v_l = v_0
    v_f = v_0
    pos_l = gap
    pos_f = 0
    running = True
    moving_l = True
    while count <= max_count and running:
        leadcar = LEADCAR(v_l, pos_l, 2010, 1000, False, False, moving_l)
        follower = FOLLOWERCAR(v_f, pos_f, gap, pos_l)
        leadcar.update()
        pos_l = leadcar.distance()
        v_l = leadcar.speed()
        follower.update()
        pos_f = follower.distance()
        v_f = follower.speed()
        if v_l <= 0:
            v_l = 0
            moving_l = False
        if v_f <= 0:
            v_f = 0
            running = False
        pos_diff.append(pos_l - pos_f)
        pos_lead.append(pos_l)
        pos_fol.append(pos_f)
        vel_lead.append(v_l)
        vel_fol.append(v_f)
        vel_diff.append(v_l - v_f)
        count += 1
    if n == 1:
        return pos_diff
    elif n == 2:
        return vel_diff
    elif n == 3:
        return pos_lead
    elif n == 4:
        return pos_fol
    elif n == 5:
        return vel_lead
    elif n == 6:
        return vel_fol


def graphs(i, iterations):
    results = update_model(iterations, 1, 10, i)
    x = np.arange(1, iterations + 1)
    y = results
    plt.title("whatever")
    plt.xlabel("iterations")
    plt.ylabel("whatever")
    plt.plot(x, y)
    plt.show()


graphs(1, 100)
