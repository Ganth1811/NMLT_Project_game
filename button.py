import pygame
import settings as st
import sfx

pygame.init()

screen = pygame.display.set_mode((st.SCREEN_WIDTH, st.SCREEN_HEIGHT))
hover_sound = pygame.mixer_music.load("music\cirno.mp3")

class Button(pygame.sprite.Sprite):
    def __init__(self, default_image, hovering_image, x_pos, y_pos):
        super().__init__()
        
        self.image = default_image
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.default_image, self.hovering_image = default_image, hovering_image
        self.position = (x_pos, y_pos)
        self.hovered = False
    
    
    #TODO: Draw the button on the screen depending on the state (hover or static)
    def drawButton(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.hovering_image
            if not self.hovered:
                self.hovered = True
                sfx.button_hover.play()
            
        else:
            self.image = self.default_image
            self.hovered = False
        
        
    #TODO: Check if the button is clicked
    def isClicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return 1
        return 0
    
    
    #TODO: update the surface of the button
    def update(self):
        self.drawButton()
        
        

#* Creating buttons      
new_game_default = pygame.image.load("img\\Buttons\\NewGame_default.png").convert_alpha()
new_game_hover = pygame.image.load("img\\Buttons\\NewGame_hover.png").convert_alpha()

resume_default = pygame.image.load("img\Buttons\\Resume_default.png").convert_alpha()
resume_hover = pygame.image.load("img\Buttons\\Resume_hover.png").convert_alpha()

high_score_default = pygame.image.load("img\Buttons\\HighScore_default.png").convert_alpha()
high_score_hover = pygame.image.load("img\Buttons\\HighScore_hover.png").convert_alpha()

quit_game_default = pygame.image.load("img\Buttons\\QuitGame_default.png").convert_alpha()
quit_game_hover = pygame.image.load("img\Buttons\\QuitGame_hover.png").convert_alpha()

option_default = pygame.image.load("img\Buttons\\Option_default.png").convert_alpha()
option_hover = pygame.image.load("img\Buttons\\Option_hover.png").convert_alpha()

new_game_button = Button(new_game_default, new_game_hover, 640, 400)
#high_score_button = Button(high_score_default, high_score_hover, 640, 520)
option_button = Button(option_default, option_hover, 640, 520)
quit_game_button = Button(quit_game_default, quit_game_hover, 640, 640)

resume_button = Button(resume_default, resume_hover, 100, 100)
