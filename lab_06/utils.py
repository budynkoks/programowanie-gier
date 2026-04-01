SCREENW = 800
SCREENH = 600

# Przyspieszenie liniowe statku w pikselach na sekundę do kwadratu (ile pędu zyskuje statek).
SHIP_THRUST = 300.0 
# Współczynnik tarcia addytywnego, stopniowo i liniowo wyhamowujący statek (piksele na sekundę do kwadratu).
SHIP_FRICTION = 50.0 
# Prędkość obrotu statku w radianach na sekundę.
SHIP_ROTSPEED = 3.5 
# Maksymalna prędkość statku w pikselach na sekundę, zapobiegająca nieskończonemu przyspieszaniu.
SHIP_MAXSPEED = 400.0 

DEBUG = False # Flaga do wyświetlania diagnostyki 

def ghost_positions(x, y, size):
    """Zwraca listę pozycji (x, y) do narysowania obiektu, uwzględniając krawędzie ekranu."""
    positions = [(x, y)]
    
    # Sprawdzamy oś X
    current_positions = positions.copy()
    for px, py in current_positions:
        if px < size:
            positions.append((px + SCREENW, py))
        elif px > SCREENW - size:
            positions.append((px - SCREENW, py))
            
    # Sprawdzamy oś Y (dla wszystkich dotychczasowych wariantów X)
    current_positions = positions.copy()
    for px, py in current_positions:
        if py < size:
            positions.append((px, py + SCREENH))
        elif py > SCREENH - size:
            positions.append((px, py - SCREENH))
            
    return list(set(positions))