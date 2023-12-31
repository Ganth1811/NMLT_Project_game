import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def loadImg(path: str):
    return pygame.image.load(path).convert_alpha()

def scaleImg(img: pygame.Surface, scale: float):
    return pygame.transform.scale_by(img, scale).convert_alpha()


#* platforms.py
class PlatformImg():
    platform = loadImg("GameAssets\\img\\Bg\\platform.png")

class EnemyImg():
    death_anim = [scaleImg(loadImg(f"GameAssets\\img\\obstacles\\enemy-death-{i}.png"), 2) for i in range(1,7)]

    enemy1_sprites = loadImg("GameAssets\\img\\obstacles\\enemy1.png")
    enemy1_run = []
    for i in range(8):
        enemy1_run.append(scaleImg(pygame.transform.flip(enemy1_sprites.subsurface((48*i, 0), (25, 20)), 1, 0), 4))

    enemy2_sprites = loadImg("GameAssets\\img\\obstacles\\enemy2.png")
    enemy2_run = []
    for i in range(8):
        enemy2_run.append(scaleImg(pygame.transform.flip(enemy2_sprites.subsurface((64*i, 0), (27, 24)), 1, 0), 4))

class CollectibleImg():
    coin_sprites = loadImg("GameAssets\\img\\collectibles\\coin_sprites.png")
    coin_anim = []
    for i in range(8):
        coin_anim.append(coin_sprites.subsurface((32*i+5, 5), (22, 22)))

    emerald_sprites = loadImg("GameAssets\\img\\collectibles\\multiplier_sprites.png")
    emerald_anim = []
    for i in range(8):
        emerald_anim.append(scaleImg(emerald_sprites.subsurface((32*i+5, 5), (22, 22)), 2))

    potion_sprites = loadImg("GameAssets\\img\\collectibles\\invicibility_sprites.png")
    potion_anim = []
    for i in range(8):
        potion_anim.append(scaleImg(potion_sprites.subsurface((32*i+5, 2), (22, 25)), 2))

    rainbow_orb_sprites = loadImg("GameAssets\\img\\collectibles\\rainbow_orb_sprites.png")
    rainbow_orb_anim = []
    for i in range(5):
        rainbow_orb_anim.append(scaleImg(rainbow_orb_sprites.subsurface((32*i+7, 7), (18, 18)), 2))

class ObstacleImg():
    suriken_sprites = loadImg("GameAssets\\img\\obstacles\\suriken_sprites.png")
    suriken_anim = []
    for i in range(8):
        suriken_anim.append(scaleImg(suriken_sprites.subsurface((32 * i, 0), (32, 32)), 2))

    spike = scaleImg(loadImg("GameAssets\\img\\obstacles\\spike.png"), 3)


#* player.py
class PlayerImg():
    run_anim = [scaleImg(loadImg(f"GameAssets\\img\\Sprites\\player_run{i}.png"), 4) for i in range(1,5)]
    jump_anim = ([scaleImg(loadImg("GameAssets\\img\\Sprites\\player_jump.png"), 4)] + [scaleImg(loadImg(f"GameAssets\\img\\Sprites\\player_spin{i}.png"), 4) for i in range(1,5)])
    descend = scaleImg(loadImg("GameAssets\\img\\Sprites\\player_fall.png"), 4)
    slash_anim = [scaleImg(loadImg(f"GameAssets\\img\\Sprites\\player_attack{i}.png"), 4) for i in range(1,5)]

    run_anim_invi = [scaleImg(loadImg(f"GameAssets\\img\\Sprites\\pleier\\player_run{i}.png"), 4) for i in range(1,5)]
    jump_anim_invi = [scaleImg(loadImg("GameAssets\\img\\Sprites\\pleier\\player_jump.png"), 4)] + [scaleImg(loadImg(f"GameAssets\\img\\Sprites\\pleier\\player_spin{i}.png"), 4) for i in range(1,5)]
    descend_invi = scaleImg(loadImg("GameAssets\\img\\Sprites\\pleier\\player_fall.png"), 4)
    slash_anim_invi = [scaleImg(loadImg(f"GameAssets\\img\\Sprites\\pleier\\player_attack{i}.png"),4) for i in range(1,5)]

    die_anim = [scaleImg(loadImg(f"GameAssets\\img\\Sprites\\player_die{i}.png"), 4) for i in range(1, 5)]
    explode_anim = [scaleImg(loadImg(f"GameAssets\\img\\Sprites\\player_explode{i}.png"), 4) for i in range(1, 10)]

class BulletImg():
    bullet = scaleImg(loadImg("GameAssets\\img\\Sprites\\slash.png"), 4)


#* gameState.py
class SplashScreenImg():
    splash_screen = loadImg("GameAssets\\img\\Other\\splash_screen.png")

class TitleMenuImg():
    background = loadImg("GameAssets\\img\\Bg\\bg.jpg")
    text_quest_of = [scaleImg(loadImg(f"GameAssets\\img\\mainmenutext\\frame_{i:02d}_delay-0.1s.png"), 1.5) for i in range(0, 20)]
    text_athelard = [scaleImg(loadImg(f"GameAssets\\img\\mainmenutext2\\frame_{i:02d}_delay-0.1s.png"), 1.5) for i in range(0, 20)]
    high_score_popup = loadImg("GameAssets\\img\\Bg\\highscore_popup.png")
    how_to_play_popup = loadImg("GameAssets\\img\\Bg\\how_to_play_popup.png")

class MainGameImg():
    bg = loadImg("GameAssets\\img\\Bg\\sky.png")
    bg_1 = scaleImg(loadImg("GameAssets\\img\\Bg\\layer_1.png"), 4)
    bg_2 = scaleImg(loadImg("GameAssets\\img\\Bg\\layer_2.png"), 4)
    bg_3 = scaleImg(loadImg("GameAssets\\img\\Bg\\layer_3.png"), 4)
    bg_4 = scaleImg(loadImg("GameAssets\\img\\Bg\\layer_4.png"), 4)
    bg_5 = scaleImg(loadImg("GameAssets\\img\\Bg\\layer_5.png"), 4)
    score_frame = loadImg("GameAssets\\img\\Buttons\\score_frame.png")

    # for i in range(5):
    #     bg_layers[i].set_alpha(150)

    popup_x2 = scaleImg(loadImg(f"GameAssets\\img\\Sprites\\popup_x2.png"), 0.4)
    popup_invincible = scaleImg(loadImg(f"GameAssets\\img\\Sprites\\popup_invincible.png"), 0.125)


#* main.py
class MainImg():
    game_icon = loadImg("GameAssets\\img\\Other\\game_icon.png")


#* button.py
class ButtonImg():
    new_game = (loadImg("GameAssets\\img\\Buttons\\NewGame_default.png"), loadImg("GameAssets\\img\\Buttons\\NewGame_hover.png"))
    resume = (loadImg("GameAssets\\img\\Buttons\\Resume_default.png"), loadImg("GameAssets\\img\\Buttons\\Resume_hover.png"))
    high_score = (loadImg("GameAssets\\img\\Buttons\\HighScore_default.png"), loadImg("GameAssets\\img\\Buttons\\HighScore_hover.png"))
    quit_game = (loadImg("GameAssets\\img\\Buttons\\QuitGame_default.png"), loadImg("GameAssets\\img\\Buttons\\QuitGame_hover.png"))
    restart = (loadImg("GameAssets\\img\\Buttons\\Restart_default.png"), loadImg("GameAssets\\img\\Buttons\\Restart_hover.png"))
    main_menu = (loadImg("GameAssets\\img\\Buttons\\MainMenu_default.png"), loadImg("GameAssets\\img\\Buttons\\MainMenu_hover.png"))
    unmute = (scaleImg(loadImg("GameAssets\\img\\Buttons\\SoundOn_default.png"), 0.3), scaleImg(loadImg("GameAssets\\img\\Buttons\\SoundOn_hover.png"), 0.3))
    mute = (scaleImg(loadImg("GameAssets\\img\\Buttons\\SoundOff_default.png"), 0.3), scaleImg(loadImg("GameAssets\\img\\Buttons\\SoundOff_hover.png"), 0.3))
    how_to_play = (scaleImg(loadImg("GameAssets\\img\\Buttons\\HowToPlay_default.png"), 0.3), scaleImg(loadImg("GameAssets\\img\\Buttons\\HowToPlay_hover.png"), 0.3))
    close = (scaleImg(loadImg("GameAssets\\img\\Buttons\\Close_default.png"), 0.3), scaleImg(loadImg("GameAssets\\img\\Buttons\\Close_hover.png"), 0.3))