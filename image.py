import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def loadImg(path: str):
	return pygame.image.load(path).convert_alpha()

def scaleImg(img: pygame.Surface, scale: int):
	return pygame.transform.scale_by(img, scale)

#* platforms.py
class PlatformImg():
	platform = loadImg("img\\Bg\\platform.png")

class EnemyImg():
	run_anim = [scaleImg(loadImg(f"Sunny-land-files\\Graphical Assets\\sprites\\Enemy\\enemyRun{i}.png"), 2) for i in range(1,7)]
	death_anim = [scaleImg(loadImg(f"Sunny-land-files\\Graphical Assets\\sprites\\enemy-death\\enemy-death-{i}.png"), 2) for i in range(1,7)]

class CollectibleImg():
	coin_sprites = loadImg("img\\collectibles\\coin_sprites.png")
	coin_anim = []
	for i in range(8):
		coin_anim.append(coin_sprites.subsurface((32*i+5, 5), (22, 22)))

	print(1)

	multiplier_sprites = loadImg("img\\collectibles\\multiplier_sprites.png")
	multiplier_anim = []
	for i in range(8):
		multiplier_anim.append(scaleImg(multiplier_sprites.subsurface((32*i+5, 5), (22, 22)), 2))
	
	invicibility_sprites = loadImg("img\\collectibles\\invicibility_sprites.png")
	invicibility_anim = []
	for i in range(8):
		invicibility_anim.append(scaleImg(invicibility_sprites.subsurface((32*i+5, 2), (22, 25)), 2))

	rainbow_orb_sprites = loadImg("img\\collectibles\\rainbow_orb_sprites.png")
	rainbow_orb_anim = []
	for i in range(5):
		rainbow_orb_anim.append(scaleImg(rainbow_orb_sprites.subsurface((32*i+7, 7), (18, 18)), 2))

class ObstacleImg():
	obstacle_1 = scaleImg(loadImg("img\\obstacles\\spike_ball.png"), 2)

#* player.py
class PlayerImg():
	run_anim = [scaleImg(loadImg(f"img\\Sprites\\player_run{i}.png"), 4) for i in range(1,5)]
	jump_anim = ([scaleImg(loadImg("img\\Sprites\\player_jump.png"), 4)] 
			  + [scaleImg(loadImg(f"img\\Sprites\\player_spin{i}.png"), 4) for i in range(1,5)])
	descend = scaleImg(loadImg("img\\Sprites\\player_fall.png"), 4)
	slash_anim = [scaleImg(loadImg(f"img\\Sprites\\player_attack{i}.png"),4) for i in range(1,5)]

class BulletImg():
	bullet = scaleImg(loadImg("img\\Sprites\\slash.png"), 4)

#* gameState.py
class SplashScreenImg():
	splash_screen = loadImg("img\\Other\\splash_screen.png")

class TitleMenuImg():
	text_quest_of = [scaleImg(loadImg(f"img\\mainmenutext\\frame_{i:02d}_delay-0.1s.png"), 1.5) for i in range(0, 20)]
	text_athelard = [scaleImg(loadImg(f"img\\mainmenutext2\\frame_{i:02d}_delay-0.1s.png"), 1.5) for i in range(0, 20)]

class MainGameImg():
	bg = loadImg("img\\Bg\\sky.png")
	bg_layers = [loadImg(f"img\\Bg\\layer_{i}.png") for i in range(1, 6)]
	score_frame = loadImg("img\\Buttons\\score_frame.png")
	
	for i in range(5):
		bg_layers[i].set_alpha(150)

#* main.py
class MainImg():
	game_icon = loadImg('img\\Other\\game_icon.png')

#* button.py
class ButtonImg():
	new_game_default = loadImg("img\\Buttons\\NewGame_default.png")
	new_game_hover = loadImg("img\\Buttons\\NewGame_hover.png")

	resume_default = loadImg("img\\Buttons\\Resume_default.png")
	resume_hover = loadImg("img\\Buttons\\Resume_hover.png")

	high_score_default = loadImg("img\\Buttons\\HighScore_default.png")
	high_score_hover = loadImg("img\\Buttons\\HighScore_hover.png")

	quit_game_default = loadImg("img\\Buttons\\QuitGame_default.png")
	quit_game_hover = loadImg("img\\Buttons\\QuitGame_hover.png")

	option_default = loadImg("img\\Buttons\\Option_default.png")
	option_hover = loadImg("img\\Buttons\\Option_hover.png")

	restart_default = loadImg("img\\Buttons\\Restart_default.png")
	restart_hover = loadImg("img\\Buttons\\Restart_hover.png")

	main_menu_default = loadImg("img\\Buttons\\MainMenu_default.png")
	main_menu_hover = loadImg("img\\Buttons\\MainMenu_hover.png")