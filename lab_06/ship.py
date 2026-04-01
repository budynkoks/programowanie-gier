import pyray as rl
import math
from utils import SCREENW, SCREENH, SHIP_MAXSPEED, SHIP_THRUST, SHIP_FRICTION, SHIP_ROTSPEED, SHIP_MAXSPEED, DEBUG, ghost_positions 


class Ship:
    def __init__(self, x, y):
        self.pos = [x, y]       
        self.vel = [0.0, 0.0]   
        self.angle = 0.0        
        
        # Wierzchołki statku w układzie lokalnym (nos na (0, -15))
        self.verts = [(0, -15), (-10, 10), (10, 10)]
        # Wierzchołki płomienia silnika
        self.flame_verts = [(0, 20), (-5, 10), (5, 10)]
        
        self.is_thrusting = False

    def rotate_point(self, px, py, angle):
        # Wzór z macierzy rotacji 2D:
        rx = px * math.cos(angle) - py * math.sin(angle)
        ry = px * math.sin(angle) + py * math.cos(angle)
        return rx, ry

    def update(self, dt):
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            self.angle += SHIP_ROTSPEED * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.angle -= SHIP_ROTSPEED * dt

        dir_x = math.sin(self.angle)
        dir_y = -math.cos(self.angle)

        self.is_thrusting = rl.is_key_down(rl.KeyboardKey.KEY_UP)
        if self.is_thrusting:
            self.vel[0] += dir_x * SHIP_THRUST * dt
            self.vel[1] += dir_y * SHIP_THRUST * dt

        #  Hamulec awaryjny
        is_braking = rl.is_key_down(rl.KeyboardKey.KEY_Z)
        current_friction = SHIP_FRICTION * 10 if is_braking else SHIP_FRICTION

        # Tarcie addytywne i limit prędkości 
        speed = math.hypot(self.vel[0], self.vel[1])
        
        if speed > 0:
            new_speed = max(0.0, speed - current_friction * dt)
            
            # Clamp prędkości maksymalnej
            if new_speed > SHIP_MAXSPEED:
                new_speed = SHIP_MAXSPEED
                
            # Skalujemy wektor prędkości do nowej długości
            scale = new_speed / speed
            self.vel[0] *= scale
            self.vel[1] *= scale

        # Aktualizacja pozycji na podstawie prędkości
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

        # Odbijanie od krawędzi ekranu zkomentowane, bo mamy owijanie w metodzie wrap()
        ''' if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] *= -1 
        elif self.pos[0] > 800:
            self.pos[0] = 800
            self.vel[0] *= -1
            
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] *= -1 
        elif self.pos[1] > SCREENH:
            self.pos[1] = SCREENH
            self.vel[1] *= -1      '''
       
        
    def get_world_verts(self, local_verts, px, py):
        world_verts = []
        for vx, vy in local_verts:
            # Rotacja
            rx, ry = self.rotate_point(vx, vy, self.angle)
            # Translacja (przesunięcie na pozycję statku)
            world_verts.append(rl.Vector2(rx + px, ry + py))
        return world_verts
    def wrap(self):
        # Owijanie pozycji statku wokół krawędzi ekranu
        if self.pos[0] < 0:
            self.pos[0] += SCREENW
        elif self.pos[0] > SCREENW:
            self.pos[0] -= SCREENW

        if self.pos[1] < 0:
            self.pos[1] += SCREENH
        elif self.pos[1] > SCREENH:
            self.pos[1] -= SCREENH
            
    def draw(self):
        positions = ghost_positions(self.pos[0], self.pos[1], 20) # 20 to promień do sprawdzania sąsiedztwa
        
        for px, py in positions:
            world_verts = self.get_world_verts(self.verts, px, py)
            for i in range(len(world_verts)):
                v1 = world_verts[i]
                v2 = world_verts[(i + 1) % len(world_verts)]
                rl.draw_line_v(v1, v2, rl.DARKBLUE)
            
            # Rysowanie płomienia silnika, jeśli statek jest w trybie SHIP_THRUST
            if self.is_thrusting:
                flame_world_verts = self.get_world_verts(self.flame_verts, px, py)
                for i in range(len(flame_world_verts)):
                    v1 = flame_world_verts[i]
                    v2 = flame_world_verts[(i + 1) % len(flame_world_verts)]
                    rl.draw_line_v(v1, v2, rl.ORANGE)
            
        # Diagnostyka
        if DEBUG:
            # Rysowanie wektora prędkości
            end_x = self.pos[0] + self.vel[0] * 0.5 
            end_y = self.pos[1] + self.vel[1] * 0.5
            rl.draw_line_v(rl.Vector2(self.pos[0], self.pos[1]), rl.Vector2(end_x, end_y), rl.RED)
            
            # Tekst z wartością prędkości
            speed = math.hypot(self.vel[0], self.vel[1])
            rl.draw_text(f"Speed: {speed:.2f}", 10, 10, 20, rl.YELLOW)