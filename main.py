import pygame
import platforms
from sys import exit
import gameStates as gs
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


#setup before running
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Alpha 1.0")


#* setting the default state
current_state = gs.SplashScreen()

#* main game loop
while True:
    events = pygame.event.get()
    current_state.processEvent(events)
    
    next_state = current_state.processEvent(events)
    
    if next_state is not None:
        current_state = next_state
    
    current_state.update()
    
    pygame.display.update()
    clock.tick(60)    