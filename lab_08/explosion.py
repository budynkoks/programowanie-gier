import pyray as rl

class Explosion:
    def __init__(self, x, y, target_radius):
        self.pos = [x, y]
        self.radius = 1.0
        self.target_radius = target_radius * 1.5
        self.expansion_speed = 100.0 # Szybkość powiększania się okręgu
        self.alive = True

    def update(self, dt):
        self.radius += self.expansion_speed * dt
        if self.radius >= self.target_radius:
            self.alive = False

    def draw(self):
        # Rysujemy pusty w środku okrąg (tylko kontur)
        rl.draw_circle_lines(int(self.pos[0]), int(self.pos[1]), self.radius, rl.ORANGE)