# utils.py
import math
from config import SCREENW, SCREENH

def ghost_positions(x, y, size):
    positions = [(x, y)]
    current_positions = positions.copy()
    for px, py in current_positions:
        if px < size: positions.append((px + SCREENW, py))
        elif px > SCREENW - size: positions.append((px - SCREENW, py))
            
    current_positions = positions.copy()
    for px, py in current_positions:
        if py < size: positions.append((px, py + SCREENH))
        elif py > SCREENH - size: positions.append((px, py - SCREENH))
            
    return list(set(positions))

def check_collision_circles(pos1, radius1, pos2, radius2):
    dist = math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return dist < (radius1 + radius2)

# NOWE: DRY (Don't Repeat Yourself) dla czyszczenia list
def cleanup_dead(objects):
    return [obj for obj in objects if obj.alive]