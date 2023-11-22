import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#* platforms.py
class PlatformImg():
	platform = pygame.image.load("img\\Bg\\platform.png").convert_alpha()

class EnemyImg():
	run_anim = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\Enemy\\enemyRun{i}.png").convert_alpha() for i in range(1,7)]
	death_anim = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\enemy-death\\enemy-death-{i}.png").convert_alpha() for i in range(1,7)]

class CollectibleImg():
	diamond_anim = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\gem\\gem-{i}.png").convert_alpha() for i in range(1,6)]
	cherry_anim = [pygame.image.load(f"img\\collectibles\\cherry-{i}.png").convert_alpha() for i in range(1,8)]

class ObstacleImg():
	pass

#* player.py
class PlayerImg():
	run_anim = [pygame.image.load(f"img\\Sprites\\player_run{i}.png").convert_alpha() for i in range(1,5)]
	jump_anim = [pygame.image.load("img\\Sprites\\player_jump.png").convert_alpha()] + [pygame.image.load(f"img\\Sprites\\player_spin{i}.png").convert_alpha() for i in range(1,5)]
	descend = pygame.image.load("img\\Sprites\\player_fall.png").convert_alpha()
	slash_anim = [pygame.image.load(f"img\\Sprites\\player_attack{i}.png").convert_alpha() for i in range(1,5)]

class BulletImg():
	bullet = pygame.image.load("img\\Sprites\\slash.png").convert_alpha()

#* gameState.py
class SplashScreenImg():
	splash_screen = pygame.image.load("img\\Other\\splash_screen.png").convert_alpha()

class TitleMenuImg():
	pass
	#TODO: Wait for new menu background

class MainGameImg():
	bg = pygame.image.load("img\\Bg\\sky.png").convert_alpha()
	bg_layers = [pygame.image.load(f"img\\Bg\\layer_{i}.png").convert_alpha() for i in range(1, 6)]
	score_frame = pygame.image.load("img\\Buttons\\score_frame.png")

#* main.py
class MainImg():
	game_icon = pygame.image.load('img\\Other\\game_icon.png').convert_alpha()

#* button.py
class ButtonImg():
	new_game_default = pygame.image.load("img\\Buttons\\NewGame_default.png").convert_alpha()
	new_game_hover = pygame.image.load("img\\Buttons\\NewGame_hover.png").convert_alpha()

	resume_default = pygame.image.load("img\\Buttons\\Resume_default.png").convert_alpha()
	resume_hover = pygame.image.load("img\\Buttons\\Resume_hover.png").convert_alpha()

	high_score_default = pygame.image.load("img\\Buttons\\HighScore_default.png").convert_alpha()
	high_score_hover = pygame.image.load("img\\Buttons\\HighScore_hover.png").convert_alpha()

	quit_game_default = pygame.image.load("img\\Buttons\\QuitGame_default.png").convert_alpha()
	quit_game_hover = pygame.image.load("img\\Buttons\\QuitGame_hover.png").convert_alpha()

	option_default = pygame.image.load("img\\Buttons\\Option_default.png").convert_alpha()
	option_hover = pygame.image.load("img\\Buttons\\Option_hover.png").convert_alpha()

	restart_default = pygame.image.load("img\\Buttons\\Restart_default.png").convert_alpha()
	restart_hover = pygame.image.load("img\\Buttons\\Restart_hover.png").convert_alpha()

	main_menu_default = pygame.image.load("img\\Buttons\\MainMenu_default.png").convert_alpha()
	main_menu_hover = pygame.image.load("img\\Buttons\\MainMenu_hover.png").convert_alpha()