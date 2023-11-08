import pygame
import platforms
import time
from sys import exit
import platforms
import gameStates as gs
from settings import SCREEN_HEIGHT, SCREEN_WIDTH


#setup before running
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Alpha 1.0")
pygame.display.set_icon(pygame.image.load('img\\Other\\game_icon.png').convert_alpha())

#setting the default state
# current_state = gs.SplashScreen()
current_state = gs.TitleMenu()

time.sleep(1)

#* main game loop
while True: 
    #Getting the events and passing it to the current state so it can procress the events accordingly
    events = pygame.event.get()
    current_state.processEvent(events)
    
    #Getting the next state of the game
    next_state = current_state.processEvent(events)
    
    #if there is a next state switch to it
    if next_state is not None:
        current_state = next_state
    
    #Update the current state (meaning handling everything in that state)
    current_state.update()
    
    pygame.display.update()

    clock.tick(60)
    
    
    
    
    
    
    
    
    
    
    
    
#! COMMENTING RULES

#TODO: use before function and method to indicate their uses
#* Highlighting or explaining some code lines or logic
#? Not sure or fully understand the code and still in implementation
#! Warnings or highlight very important stuff
## marking old/debug/temporary codes, or just to note some less important stuff 

