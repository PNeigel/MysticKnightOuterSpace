import numpy as np

def ScreenFromIngame(x,y):
    screen_x = x - y
    screen_y = (x + y) / 2.
    screen_x = int(np.round(screen_x))
    screen_y = int(np.round(screen_y))
    return screen_x, screen_y

def IngameFromScreen(x,y):
    ingame_x = y + x / 2.0
    ingame_y = y - x / 2.0
    
    return ingame_x, ingame_y