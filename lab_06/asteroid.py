import pyray as rl
import math
import random
from utils import SCREENW, SCREENH, ghost_positions

class Asteroid:
    SIZES = {
        'small': 15,
        'medium': 35,
        'large': 50
    }

    def __init__(self, x, y, size):
        radius = self.SIZES.get(size, 20)
        self.pos = [x, y]
        self.radius = radius
        
        # Prędkość zależy odwrotnie proporcjonalnie od promienia (większe są wolniejsze)
        speed = random.uniform(20.0, 80.0) * (30.0 / radius)
        direction = random.uniform(0, math.tau)
        self.vel = [math.cos(direction) * speed, math.sin(direction) * speed]
        
        self.angle = 0.0
        self.rot_speed = random.uniform(-1.5, 1.5)
        
        # Generowanie proceduralnego kształtu (Zadanie 5)
        self.verts = []
        num_points = 9
        for i in range(num_points):
            a = (i / num_points) * math.tau
            # Zniekształcenie promienia, żeby nie był idealnym kołem
            r = radius * random.uniform(0.75, 1.25)
            self.verts.append((math.cos(a) * r, math.sin(a) * r))

    def update(self, dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.angle += self.rot_speed * dt

    def wrap(self):
        self.pos[0] %= SCREENW
        self.pos[1] %= SCREENH

    def draw(self):
        # Mnożymy promień przez 1.25, żeby objąć proceduralne wypukłości przy krawędzi
        positions = ghost_positions(self.pos[0], self.pos[1], self.radius * 1.25)
        
        for px, py in positions:
            world_verts = []
            for vx, vy in self.verts:
                # Rotacja proceduralnego wierzchołka
                rx = vx * math.cos(self.angle) - vy * math.sin(self.angle)
                ry = vx * math.sin(self.angle) + vy * math.cos(self.angle)
                world_verts.append(rl.Vector2(rx + px, ry + py))
            
            # Rysowanie linii łączących wierzchołki (zamknięty wielokąt)
            for i in range(len(world_verts)):
                v1 = world_verts[i]
                v2 = world_verts[(i + 1) % len(world_verts)] # modulo łączy ostatni z pierwszym
                rl.draw_line_v(v1, v2, rl.WHITE)