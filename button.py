import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import settings as st
import sfx
from image import ButtonImg

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
hover_sound = pygame.mixer_music.load("music\\cirno.mp3")

class Button(pygame.sprite.Sprite):
    def __init__(self, images: tuple, x_pos: int, y_pos: int):
        super().__init__()

        self.default_image, self.hovering_image = images
        self.image = self.default_image
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
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

class MuteButton(Button):
    def __init__(self, x_pos: int, y_pos: int):

        self.unmute = ButtonImg.unmute
        self.mute = ButtonImg.mute

        if st.is_muted:
            images = self.mute
        else:
            images = self.unmute

        super().__init__(images, x_pos, y_pos)
    
    def update(self):
        if st.is_muted:
            self.default_image, self.hovering_image = self.mute
        else:
            self.default_image, self.hovering_image = self.unmute
        self.drawButton()


#* Creating buttons
new_game_button = Button(ButtonImg.new_game, 640 - 270, 400)
high_score_button = Button(ButtonImg.high_score, 640 - 270, 520)

#option_button = Button(ButtonImg.option, 640 - 270, 520)
quit_game_button = Button(ButtonImg.quit_game, 640 - 270, 640)

resume_button = Button(ButtonImg.resume, 640, 400)
restart_button = Button(ButtonImg.restart, 640, 520)
main_menu_button = Button(ButtonImg.main_menu, 640, 640)

mute_button = MuteButton(SCREEN_WIDTH - 70, 70)
how_to_play_button = Button(ButtonImg.how_to_play, SCREEN_WIDTH - 70, 190)