import pygame
import settings as st
pygame.init()

button_hover = pygame.mixer.Sound("GameAssets\\music\\sfx\\button_hover.mp3")
button_pressed = pygame.mixer.Sound("GameAssets\\music\\sfx\\button_pressed.mp3")
player_jump = pygame.mixer.Sound("GameAssets\\music\\sfx\\jump.mp3")
player_die = pygame.mixer.Sound("GameAssets\\music\\sfx\\player_death.mp3")
player_shoot = pygame.mixer.Sound("GameAssets\\music\\sfx\\shoot.mp3")
player_collect_coin = pygame.mixer.Sound("GameAssets\\music\\sfx\\collect_coin.mp3")
player_collect_item = pygame.mixer.Sound("GameAssets\\music\\sfx\\invicible.mp3")

player_shoot.set_volume(0.2)
player_collect_coin.set_volume(0.8)
sound_list = [button_hover, button_pressed, player_jump, player_die, player_shoot, player_collect_coin, player_collect_item]
init_volume = [sound.get_volume() for sound in sound_list]
bgm_init_volume = 0.3

def adjustSoundVolume():
    pygame.mixer_music.set_volume(not st.is_muted)
    for i in range(len(sound_list)):
        sound_list[i].set_volume(init_volume[i] * (not st.is_muted))
    pygame.mixer_music.set_volume(bgm_init_volume * (not st.is_muted))

def loadMenuTheme():
    pygame.mixer_music.load("GameAssets\\music\\bgm\\menu_theme.mp3")
    pygame.mixer_music.play(-1)

def loadBgMusic():
    pygame.mixer_music.load("GameAssets\\music\\bgm\\stage_theme.wav")
    pygame.mixer_music.play(-1)

def loadGameOverMusic():
    pygame.mixer_music.load("GameAssets\\music\\bgm\\game_over.wav")
    pygame.mixer_music.play(-1)