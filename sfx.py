import pygame
pygame.init()

button_hover = pygame.mixer.Sound("music\\sfx\\button_hover.mp3")
button_pressed = pygame.mixer.Sound("music\\sfx\\button_pressed.mp3")
player_jump = pygame.mixer.Sound("music\\sfx\\jump.mp3")
player_die = pygame.mixer.Sound("music\\sfx\\die.mp3")
player_shoot = pygame.mixer.Sound("music\\sfx\\shoot.mp3")

player_shoot.set_volume(0.2)
