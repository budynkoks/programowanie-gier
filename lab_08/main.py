# main.py
import pyray as rl
import random
import os
import math
from enum import Enum

from config import SCREENW, SCREENH, FPS, POINTS_LARGE, POINTS_MEDIUM, POINTS_SMALL
from utils import check_collision_circles, cleanup_dead
from ship import Ship
from asteroid import Asteroid
from bullet import Bullet
from explosion import Explosion

# Maszyna Stanów
class State(Enum):
    MENU = 1
    GAME = 2
    GAME_OVER = 3

# Zmienne globalne stanu
state = State.MENU
score = 0
best_score = 0
wave = 1
win = False

# Obiekty gry
player = None
asteroids = []
bullets = []
explosions = []
stars = []
snd_shoot = None
snd_explode = None

def load_best_score():
    global best_score
    try:
        if os.path.exists("scores.txt"):
            with open("scores.txt", "r") as f:
                best_score = int(f.read().strip())
    except Exception:
        best_score = 0

def save_best_score():
    try:
        with open("scores.txt", "w") as f:
            f.write(str(best_score))
    except Exception:
        pass

def spawn_wave():
    global asteroids
    # Unikamy spawnu bezpośrednio na graczu
    asteroids = []
    for _ in range(3 + wave):
        while True:
            ax = random.randint(0, SCREENW)
            ay = random.randint(0, SCREENH)
            if math.hypot(ax - SCREENW/2, ay - SCREENH/2) > 150:
                asteroids.append(Asteroid(ax, ay, level=3))
                break

def init_game():
    global player, asteroids, bullets, explosions, score, wave, win
    player = Ship(SCREENW / 2, SCREENH / 2)
    score = 0
    wave = 1
    win = False
    bullets.clear()
    explosions.clear()
    spawn_wave()

def get_points(level):
    if level == 1: return POINTS_SMALL
    elif level == 2: return POINTS_MEDIUM
    return POINTS_LARGE

# --- STAN: MENU ---
def update_menu(dt):
    global state
    if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
        init_game()
        state = State.GAME

def draw_menu():
    rl.draw_text("ASTEROIDS", SCREENW//2 - 120, SCREENH//3, 40, rl.WHITE)
    rl.draw_text("Nacisnij ENTER aby zagrac", SCREENW//2 - 140, SCREENH//2, 20, rl.GRAY)
    rl.draw_text(f"Najlepszy Wynik: {best_score}", SCREENW//2 - 120, SCREENH//2 + 50, 20, rl.GOLD)

# --- STAN: GRA ---
def update_game(dt):
    global state, score, best_score, win, asteroids, bullets, wave

    # Strzelanie
    if rl.is_key_pressed(rl.KeyboardKey.KEY_SPACE) and player.alive:
        nx, ny = player.get_nose_pos()
        bullets.append(Bullet(nx, ny, player.angle))
        rl.play_sound(snd_shoot)

    # Aktualizacje logiki
    if player.alive:
        player.update(dt)
        player.wrap()

    for b in bullets: b.update(dt); b.wrap()
    for e in explosions: e.update(dt)
    for a in asteroids: a.update(dt); a.wrap()

    # Kolizje: Pocisk - Asteroida
    new_asteroids = []
    for b in bullets:
        if not b.alive: continue
        for a in asteroids:
            if not a.alive: continue
            if check_collision_circles(b.pos, b.radius, a.pos, a.radius):
                b.alive = False
                a.alive = False
                rl.play_sound(snd_explode)
                explosions.append(Explosion(a.pos[0], a.pos[1], a.radius))
                
                score += get_points(a.level)
                new_asteroids.extend(a.split())
                break
    
    asteroids.extend(new_asteroids)

    # Kolizje: Statek - Asteroida
    if player.alive:
        for a in asteroids:
            if a.alive and check_collision_circles(player.pos, player.size, a.pos, a.radius * 0.8): # 0.8 daje mały bufor błędu
                player.alive = False
                explosions.append(Explosion(player.pos[0], player.pos[1], player.size * 2))
                rl.play_sound(snd_explode)
                
                if score > best_score:
                    best_score = score
                    save_best_score()
                
                state = State.GAME_OVER
                return

    # Czyszczenie zniszczonych obiektów
    bullets[:] = cleanup_dead(bullets)
    asteroids[:] = cleanup_dead(asteroids)
    explosions[:] = cleanup_dead(explosions)

    # Mechanika Fal (Zwycięstwo tymczasowe)
    if not asteroids and player.alive:
        wave += 1
        spawn_wave()

def draw_hud():
    rl.draw_text(f"Wynik: {score}", 10, 10, 20, rl.WHITE)
    rl.draw_text(f"Najlepszy: {best_score}", 10, 35, 20, rl.GRAY)
    rl.draw_text(f"Fala: {wave}", SCREENW - 100, 10, 20, rl.GOLD)

def draw_game():
    for sx, sy in stars: rl.draw_pixel(sx, sy, rl.DARKGRAY)
    for a in asteroids: a.draw()
    for b in bullets: b.draw()
    for e in explosions: e.draw()
    if player.alive: player.draw()
    draw_hud()

# --- STAN: GAME OVER ---
def update_game_over(dt):
    global state
    for e in explosions: e.update(dt) # Pozwólmy dograć się wybuchom
    if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
        state = State.MENU

def draw_game_over():
    draw_game() # Rysujemy zatrzymaną klatkę gry w tle
    rl.draw_text("GAME OVER", SCREENW//2 - 110, SCREENH//3, 40, rl.RED)
    rl.draw_text("Nacisnij ENTER by wrocic do menu", SCREENW//2 - 170, SCREENH//2, 20, rl.WHITE)

# --- PĘTLA GŁÓWNA ---
def main():
    global stars, snd_shoot, snd_explode
    
    rl.init_window(SCREENW, SCREENH, "Asteroids")
    rl.set_target_fps(FPS)
    rl.init_audio_device()

    # Load assets
    snd_shoot = rl.load_sound("assets/freesound_community-snare-space-shot-80932.mp3")
    snd_explode = rl.load_sound("assets/mixkit-shatter-shot-explosion-1693.wav")
    stars = [(random.randint(0, SCREENW), random.randint(0, SCREENH)) for _ in range(100)]
    
    load_best_score()

    while not rl.window_should_close():
        dt = rl.get_frame_time()

        # Update
        if state == State.MENU: update_menu(dt)
        elif state == State.GAME: update_game(dt)
        elif state == State.GAME_OVER: update_game_over(dt)

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        
        if state == State.MENU: draw_menu()
        elif state == State.GAME: draw_game()
        elif state == State.GAME_OVER: draw_game_over()
            
        rl.end_drawing()

    # Zamykanie
    rl.unload_sound(snd_shoot)
    rl.unload_sound(snd_explode)
    rl.close_audio_device()
    rl.close_window()

if __name__ == "__main__":
    main()