import pyray as rl
import math

# Przyspieszenie liniowe statku w pikselach na sekundę do kwadratu (ile pędu zyskuje statek).
THRUST = 300.0 
# Współczynnik tarcia addytywnego, stopniowo i liniowo wyhamowujący statek (piksele na sekundę do kwadratu).
FRICTION = 50.0 
# Prędkość obrotu statku w radianach na sekundę.
ROTSPEED = 3.5 
# Maksymalna prędkość statku w pikselach na sekundę, zapobiegająca nieskończonemu przyspieszaniu.
MAXSPEED = 400.0 

DEBUG = True # Flaga do wyświetlania diagnostyki 

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
            self.angle += ROTSPEED * dt
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            self.angle -= ROTSPEED * dt

        dir_x = math.sin(self.angle)
        dir_y = -math.cos(self.angle)

        self.is_thrusting = rl.is_key_down(rl.KeyboardKey.KEY_UP)
        if self.is_thrusting:
            self.vel[0] += dir_x * THRUST * dt
            self.vel[1] += dir_y * THRUST * dt

        #  Hamulec awaryjny
        is_braking = rl.is_key_down(rl.KeyboardKey.KEY_Z)
        current_friction = FRICTION * 10 if is_braking else FRICTION

        # Tarcie addytywne i limit prędkości 
        speed = math.hypot(self.vel[0], self.vel[1])
        
        if speed > 0:
            new_speed = max(0.0, speed - current_friction * dt)
            
            # Clamp prędkości maksymalnej
            if new_speed > MAXSPEED:
                new_speed = MAXSPEED
                
            # Skalujemy wektor prędkości do nowej długości
            scale = new_speed / speed
            self.vel[0] *= scale
            self.vel[1] *= scale

        # Aktualizacja pozycji na podstawie prędkości
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

        # Odbijanie od krawędzi ekranu
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.vel[0] *= -1 
        elif self.pos[0] > 800:
            self.pos[0] = 800
            self.vel[0] *= -1
            
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.vel[1] *= -1 
        elif self.pos[1] > 600:
            self.pos[1] = 600
            self.vel[1] *= -1

    def get_world_verts(self, local_verts):
        world_verts = []
        for vx, vy in local_verts:
            # Rotacja
            rx, ry = self.rotate_point(vx, vy, self.angle)
            # Translacja (przesunięcie na pozycję statku)
            world_verts.append(rl.Vector2(rx + self.pos[0], ry + self.pos[1]))
        return world_verts

    def draw(self):
        # Pobranie przeliczonych wierzchołków
        ship_wverts = self.get_world_verts(self.verts)
        
        # Rysowanie statku
        rl.draw_triangle_lines(ship_wverts[0], ship_wverts[1], ship_wverts[2], rl.DARKBLUE)
        rl.draw_triangle(ship_wverts[0], ship_wverts[1], ship_wverts[2], rl.DARKBLUE)

        if self.is_thrusting:
            flame_wverts = self.get_world_verts(self.flame_verts)
            rl.draw_triangle(flame_wverts[0], flame_wverts[2], flame_wverts[1], rl.ORANGE)
            rl.draw_triangle_lines(flame_wverts[0], flame_wverts[2], flame_wverts[1], rl.ORANGE)
        # Diagnostyka 
        if DEBUG:
            # Rysowanie wektora prędkości
            end_x = self.pos[0] + self.vel[0] * 0.5 
            end_y = self.pos[1] + self.vel[1] * 0.5
            rl.draw_line_v(rl.Vector2(self.pos[0], self.pos[1]), rl.Vector2(end_x, end_y), rl.RED)
            
            # Tekst z wartością prędkości
            speed = math.hypot(self.vel[0], self.vel[1])
            rl.draw_text(f"Speed: {speed:.1f}", int(self.pos[0]) + 20, int(self.pos[1]) - 20, 10, rl.GREEN)