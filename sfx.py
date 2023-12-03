import pygame
import settings as st
pygame.init()

button_hover = pygame.mixer.Sound("music\\sfx\\button_hover.mp3")
button_pressed = pygame.mixer.Sound("music\\sfx\\button_pressed.mp3")
player_jump = pygame.mixer.Sound("music\\sfx\\jump.mp3")
player_die = pygame.mixer.Sound("music\\sfx\\player_death.mp3")
player_shoot = pygame.mixer.Sound("music\\sfx\\shoot.mp3")
player_collect_coin = pygame.mixer.Sound("music\\sfx\\collect_coin.mp3")
player_collect_cherry = pygame.mixer.Sound("music\\sfx\\invicible.mp3")

player_shoot.set_volume(0.2)
player_collect_coin.set_volume(2.5)
sound_list = [button_hover, button_pressed, player_jump, player_die, player_shoot, player_collect_coin, player_collect_cherry]
init_volume = [sound.get_volume() for sound in sound_list]

class SoundConfig():
    def muteSound():
        pygame.mixer.music.set_volume(not st.is_muted)
        for i in range(len(sound_list)):
            sound_list[i].set_volume(init_volume[i] * (not st.is_muted))

    def loadMenuTheme():
        pygame.mixer_music.load("music\\bgm\\menu_theme.mp3")
        pygame.mixer_music.play(-1)

    def loadBgMusic():
        pygame.mixer_music.load("music\\bgm\\stage_theme_1.wav")
        pygame.mixer_music.play(-1)

    def loadGameOverMusic():
        pygame.mixer_music.load("music\\bgm\\game_over.wav")
        pygame.mixer_music.play(-1)