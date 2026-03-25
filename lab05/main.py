import pyray as rl
from ship import Ship

def main():
    screen_width = 800
    screen_height = 600
    
    # Inicjalizacja okna
    rl.init_window(screen_width, screen_height, "Gierka")
    
    rl.set_target_fps(120) 
    
    # Tworzenie instancji statku na środku ekranu 
    player = Ship(screen_width / 2, screen_height / 2)
    
    # Główna pętla gry
    while not rl.window_should_close():
        dt = rl.get_frame_time()
        player.update(dt)
        
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        
        player.draw()
        
        rl.end_drawing()
        
    rl.close_window()

if __name__ == "__main__":
    main()