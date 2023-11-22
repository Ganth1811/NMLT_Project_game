import pygame
import settings as st
import sfx
from image import ButtonImg

pygame.init()

screen = pygame.display.set_mode((st.SCREEN_WIDTH, st.SCREEN_HEIGHT))
hover_sound = pygame.mixer_music.load("music\\cirno.mp3")

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
        return self.hovered


    #TODO: update the surface of the button
    def update(self):
        self.drawButton()



#* Creating buttons
new_game_button = Button(ButtonImg.new_game_default, ButtonImg.new_game_hover, 640, 400)
#high_score_button = Button(ButtonImg.high_score_default, ButtonImg.high_score_hover, 640, 520)
option_button = Button(ButtonImg.option_default, ButtonImg.option_hover, 640, 520)
quit_game_button = Button(ButtonImg.quit_game_default, ButtonImg.quit_game_hover, 640, 640)

resume_button = Button(ButtonImg.resume_default, ButtonImg.resume_hover, 640, 400)
restart_button = Button(ButtonImg.restart_default, ButtonImg.restart_hover, 640, 520)
main_menu_button = Button(ButtonImg.main_menu_default, ButtonImg.main_menu_hover, 640, 640)