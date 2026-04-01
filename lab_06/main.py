import pyray as rl
from ship import Ship
from asteroid import Asteroid

from utils import SCREENW, SCREENH
def main():
   
    # Inicjalizacja okna
    rl.init_window(SCREENW, SCREENH, "Gierka")
    
    rl.set_target_fps(120) 
    
    # Tworzenie instancji statku na środku ekranu 
    player = Ship(SCREENW / 2, SCREENH / 2)
    asteroid = Asteroid(100, 100, 'medium')
    asteroid2 = Asteroid(700, 500, 'large')
    asteroid3 = Asteroid(400, 300, 'small')
    asteroid4 = Asteroid(100, 800, 'small')
    asteroid5= Asteroid(200, 600, 'small')

    # Główna pętla gry
    while not rl.window_should_close():
        dt = rl.get_frame_time()
        player.update(dt)
        player.wrap()  # Owijanie pozycji statku wokół krawędzi ekranu
        asteroid.update(dt)
        asteroid.wrap()  # Owijanie pozycji asteroidy wokół krawędzi ekranu
        asteroid2.update(dt)
        asteroid2.wrap()  
        asteroid3.update(dt)
        asteroid3.wrap()  
        asteroid4.update(dt)
        asteroid4.wrap()  
        asteroid5.update(dt)
        asteroid5.wrap()     
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        asteroid.draw()
        asteroid2.draw()
        asteroid3.draw()
        asteroid4.draw()
        asteroid5.draw()

        player.draw()
        
        rl.end_drawing()
        
    rl.close_window()

if __name__ == "__main__":
    main()