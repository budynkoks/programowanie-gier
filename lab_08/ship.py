import pyray as rl
import math
from utils import ghost_positions
from config import SCREENW, SCREENH, SHIP_THRUST, SHIP_FRICTION, SHIP_ROTSPEED, SHIP_MAXSPEED

DEBUG = False

class Ship:
    def __init__(self, x, y):
        self.pos = [x, y]       
        self.vel = [0.0, 0.0]   
        self.angle = 0.0        
        self.verts = [(0, -15), (-10, 10), (10, 10)]
        self.flame_verts = [(0, 20), (-5, 10), (5, 10)]
        self.is_thrusting = False
        self.size = 15 
        self.alive = True 

    def rotate_point(self, px, py, angle):
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

        is_braking = rl.is_key_down(rl.KeyboardKey.KEY_Z)
        current_friction = SHIP_FRICTION * 10 if is_braking else SHIP_FRICTION

        speed = math.hypot(self.vel[0], self.vel[1])
        if speed > 0:
            new_speed = max(0.0, speed - current_friction * dt)
            if new_speed > SHIP_MAXSPEED:
                new_speed = SHIP_MAXSPEED
            scale = new_speed / speed
            self.vel[0] *= scale
            self.vel[1] *= scale

        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

    def wrap(self):
        self.pos[0] %= SCREENW
        self.pos[1] %= SCREENH

    def get_world_verts(self, local_verts, bx, by):
        world_verts = []
        for vx, vy in local_verts:
            rx, ry = self.rotate_point(vx, vy, self.angle)
            world_verts.append(rl.Vector2(rx + bx, ry + by))
        return world_verts

    def draw(self):
        positions = ghost_positions(self.pos[0], self.pos[1], self.size)
        
        for px, py in positions:
            ship_wverts = self.get_world_verts(self.verts, px, py)
            rl.draw_triangle_lines(ship_wverts[0], ship_wverts[1], ship_wverts[2], rl.DARKBLUE)
            rl.draw_triangle(ship_wverts[0], ship_wverts[1], ship_wverts[2], rl.DARKBLUE)

            if self.is_thrusting:
                flame_wverts = self.get_world_verts(self.flame_verts, px, py)
                rl.draw_triangle(flame_wverts[0], flame_wverts[2], flame_wverts[1], rl.ORANGE)
                rl.draw_triangle_lines(flame_wverts[0], flame_wverts[2], flame_wverts[1], rl.ORANGE)

        if DEBUG:
            end_x = self.pos[0] + self.vel[0] * 0.5 
            end_y = self.pos[1] + self.vel[1] * 0.5
            rl.draw_line_v(rl.Vector2(self.pos[0], self.pos[1]), rl.Vector2(end_x, end_y), rl.RED)
            speed = math.hypot(self.vel[0], self.vel[1])
            rl.draw_text(f"Speed: {speed:.1f}", int(self.pos[0]) + 20, int(self.pos[1]) - 20, 10, rl.GREEN)

    def get_nose_pos(self):
        nx, ny = self.rotate_point(0, -15, self.angle)
        return [self.pos[0] + nx, self.pos[1] + ny]