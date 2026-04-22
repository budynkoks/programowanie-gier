# asteroid.py
import pyray as rl
import math
import random
from utils import ghost_positions
from config import SCREENW, SCREENH

class Asteroid:
    def __init__(self, x, y, level=3):
        self.pos = [x, y]
        self.level = level
        self.alive = True

        # Rozmiar na podstawie poziomu
        if level == 1: self.radius = 15
        elif level == 2: self.radius = 35
        else: self.radius = 50

        # Prędkość - im mniejszy poziom, tym wyższa prędkość
        speed = random.uniform(20.0, 80.0) * (4.0 / self.level)
        direction = random.uniform(0, math.tau)
        self.vel = [math.cos(direction) * speed, math.sin(direction) * speed]
        
        self.angle = 0.0
        self.rot_speed = random.uniform(-1.5, 1.5)
        
        self.verts = []
        num_points = 9
        for i in range(num_points):
            a = (i / num_points) * math.tau
            r = self.radius * random.uniform(0.75, 1.25)
            self.verts.append((math.cos(a) * r, math.sin(a) * r))

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.angle += self.rot_speed * dt

    def wrap(self):
        self.pos[0] %= SCREENW
        self.pos[1] %= SCREENH

    def draw(self):
        positions = ghost_positions(self.pos[0], self.pos[1], self.radius * 1.25)
        for px, py in positions:
            world_verts = []
            for vx, vy in self.verts:
                rx = vx * math.cos(self.angle) - vy * math.sin(self.angle)
                ry = vx * math.sin(self.angle) + vy * math.cos(self.angle)
                world_verts.append(rl.Vector2(rx + px, ry + py))
            
            for i in range(len(world_verts)):
                v1 = world_verts[i]
                v2 = world_verts[(i + 1) % len(world_verts)]
                rl.draw_line_v(v1, v2, rl.WHITE)

    # NOWE: Funkcja dzieląca asteroidę na dwie mniejsze
    def split(self):
        if self.level <= 1:
            return []
        return [
            Asteroid(self.pos[0], self.pos[1], self.level - 1),
            Asteroid(self.pos[0], self.pos[1], self.level - 1)
        ]