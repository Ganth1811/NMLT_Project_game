import pygame
import gameStates as gs
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from time import time


 
#! changes in the player: added invincible frame (player doesn not take dmg when in this state)
#! changes in platforms: added an item that gives player invincibility, also some other obstacles spawn type


#setup before running          
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Beta 1.0")
pygame.display.set_icon(pygame.image.load('img\\Other\\game_icon.png').convert_alpha())

#setting the default state
#current_state = gs.SplashScreen()
current_state = gs.TitleMenu()
last_time = time()

#* main game loop
while 1:
    #Getting the events and passing it to the current state so it can procress the events accordingly
    events = pygame.event.get()
    current_state.processEvent(events)

    #Getting the next state of the game
    
    next_state = current_state.processEvent(events)

    #if there is a next state switch to it
    if next_state is not None:
        current_state = next_state

    #Update the current state (meaning handling everything in that state)
    current_time = time()
    dt = current_time - last_time
    last_time = current_time
    current_state.update(dt)

    #print(clock.get_fps())
    pygame.display.update()

    clock.tick(60)






#! COMMENTING RULES

#TODO: use before function and method to indicate their uses
#* Highlighting or explaining some code lines or logic
#? Not sure or fully understand the code and still in implementation
#! Warnings or highlight very important stuff
## marking old/debug/temporary codes, or just to note some less important stuff

