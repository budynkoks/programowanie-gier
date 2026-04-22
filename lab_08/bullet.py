import pyray as rl
import math
from utils import SCREENW, SCREENH

class Bullet:
    def __init__(self, x, y, angle):
        self.pos = [x, y]
        self.radius = 2.0
        
        # Prędkość pocisku musi być znacznie wyższa niż statku
        speed = 600.0
        
        # Obliczamy wektor kierunku na podstawie kąta statku
        dir_x = math.sin(angle)
        dir_y = -math.cos(angle)
        
        self.vel = [dir_x * speed, dir_y * speed]
        self.ttl = 1.5 
        self.alive = True

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        
        # Zmniejszanie czasu życia
        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False

    def wrap(self):
        self.pos[0] %= SCREENW
        self.pos[1] %= SCREENH

    def draw(self):
        rl.draw_circle(int(self.pos[0]), int(self.pos[1]), self.radius, rl.WHITE)