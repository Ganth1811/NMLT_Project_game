import pygame
from sys import exit
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import button as bt
import sfx
from player import player, bullets, Player
from platforms import Obstacle, Platform, generatePlatform, Enemy, Diamond, InvicibleCherry
import random
from math import ceil


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



class State(object):
    #TODO: initialize general properties of the state class and its subclass
    def __init__(self):
        self.screen = screen

    #TODO: processing the events
    def processEvent(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    #TODO: render necessary things in the state
    def render(self):
        pass

    #TODO: update the state, basically mean doing everything in the state
    def update(self):
        pass



#* The splash screen displays the logo of the group for a few seconds then fades out
class SplashScreen(State):
    def __init__(self):
        super(State, self).__init__()
        self.splash_screen = pygame.image.load("img\\Other\\splash_screen.png").convert_alpha()
        self.fade = False
        self.alpha = 0
        self.bg_music = pygame.mixer_music.load("music\\bgm\\stage_theme.mp3")
        self.clock = pygame.time.Clock()
        pygame.mixer_music.play(-1)

    def processEvent(self, events):
        super().processEvent(events)
        if pygame.time.get_ticks() > 6000:
            return TitleMenu()

    def render(self):
        #* Check if the Splash Screen is in the fading procress then fade it in
        if not self.fade:
            fade_transition(self.splash_screen)
            self.fade = True


    def update(self):
        self.render()



#* The title menu displays the game name and different options player can choose
class TitleMenu(State):
    def __init__(self):
        super(State, self).__init__()


        self.background = pygame.image.load("img\\Bg\\main_menu_bg.png").convert_alpha()

        # self.bg_music = pygame.mixer_music.load("music\\bgm\\stage_theme.mp3")
        # pygame.mixer_music.play(-1)

        #* initialize the button objects
        self.buttons = self.createButtons()

    #TODO: create the buttons and add them to a dictionary
    def createButtons(self):
        new_game_button = bt.new_game_button
        option_button = bt.option_button
        quit_game_button = bt.quit_game_button

        #* creating the buttons dictionary to detect which button is being pressed
        button_names = {
            "new_game": new_game_button,
            "option": option_button,
            "quit_game": quit_game_button
        }

        #* creating the button group to draw the buttons
        button_group = pygame.sprite.Group()
        button_group.add(button_names.values())

        #* return both of the button types
        return {
            "button_names": button_names,
            "button_group": button_group
        }


    def processEvent(self, events):
        super().processEvent(events)

        for event in events:
            #* quitting the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            #* Switching the game state acording to the button pressed by the player
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, button in self.buttons["button_names"].items():
                    if button.isClicked():
                        sfx.button_pressed.play()
                        if button_name == "new_game":
                            pygame.mixer_music.unload()
                            return MainGame()
                        elif button_name == "option":
                            pass
                        elif button_name == "quit_game":
                            pygame.quit()
                            exit()

    def render(self):
        screen.blit(self.background, (0, 0))
        self.buttons["button_group"].update()
        self.buttons["button_group"].draw(screen)

    def update(self):
        self.render()


class PauseMenu(State):
    def __init__(self, previous_state):
        super(State, self).__init__()

        #* Pause the music temporarily
        pygame.mixer_music.pause()
        self.previous_state = previous_state
        self.blurScreen()
        self.buttons = self.createButtons()

    #* Not really blur but make the game screen behind darker
    #TODO: make the game screen blur
    def blurScreen(self):
        self.blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.blur.set_alpha(69)
        screen.blit(self.blur, (0, 0))

    def createButtons(self):
        resume_button = bt.resume_button
        restart_button = bt.restart_button
        main_menu_button = bt.main_menu_button

        #* creating the buttons dictionary to detect which button is being pressed
        button_names = {
            "resume": resume_button,
            "restart": restart_button,
            "main_menu": main_menu_button
        }

        #* creating the button group to draw the buttons
        button_group = pygame.sprite.Group()
        button_group.add(button_names.values())

        #* return both of the button types
        return {
            "button_names": button_names,
            "button_group": button_group
        }

    def processEvent(self, events):
        super().processEvent(events)

        #* If the player presses escape then unpause the game
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.previous_state.is_pause = False
                    self.previous_state.start_time = pygame.time.get_ticks()
                    pygame.mixer_music.unpause()

                    #* returning the old game MainGame object instead of initializing a new instance
                    return self.previous_state

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, button in self.buttons["button_names"].items():
                    if button.isClicked():
                        sfx.button_pressed.play()
                        if button_name == "resume":
                            self.previous_state.is_pause = False
                            self.previous_state.start_time = pygame.time.get_ticks()
                            pygame.mixer_music.unpause()
                            return self.previous_state

                        elif button_name == "restart":
                            return MainGame()

                        elif button_name == "main_menu":
                            return TitleMenu()

    def render(self):
        self.buttons["button_group"].update()
        self.buttons["button_group"].draw(screen)

    def update(self):
        self.render()


class MainGame(State):
    def __init__(self):
        super(State, self).__init__()

        #* background and other visual objects
        self.background = pygame.transform.scale(pygame.image.load("Sunny-land-files\\Graphical Assets\\environment\\Background\\Background.jpg").convert_alpha(), (1280, 720))
        self.ground_surface = pygame.Surface((1280,300))
        self.ground_surface.fill('white')
        self.tiles = ceil(SCREEN_WIDTH / self.background.get_width()) + 1
        self.scrolls = [2, 1, 1.4, 1.3, 1.2]
        self.bg = pygame.transform.scale(pygame.image.load("img\\Bg\\sky.png").convert_alpha(), (1280, 720))
        self.background_layers = [pygame.image.load(f"img\\Bg\\layer_{i}.png").convert_alpha() for i in range(1, 6)]
        self.background_layers = [pygame.transform.scale(image, (1280, 720)) for image in self.background_layers]
        
        
        
        #* background music
        self.bg_music = pygame.mixer_music.load("music\\bgm\\game_bg_music.mp3")
        pygame.mixer_music.play(-1)

        #* player and bullets
        self.player_group = pygame.sprite.Group(Player())
        self.player_sprite: Player = self.player_group.sprites()[0]
        self.bullets_group = bullets

        #* platforms
        self.platform_group = pygame.sprite.Group()
        self.init_platform = Platform(100, 500, 1200, 100)
        self.platform_group.add(Platform(0, 500, 3000, 100)) #* initial platform
        self.prev_platform_pos = self.init_platform.rect
        self.platform_speed = 10

        #* enemy
        self.enemy_group = pygame.sprite.Group()

        #* collectible
        self.collectibles_group = pygame.sprite.Group()

        #* obstacles
        self.obstacle_group = pygame.sprite.Group()

        #* time
        self.start_time = pygame.time.get_ticks()
        self.previous_run_time = 0
        self.run_time = 0
        self.spawn_delay = 400

        #* pausing mechanism
        self.is_pause = False

        #* score
        self.score_frame = pygame.image.load("img\\Buttons\\score_frame.png")
        self.font = pygame.font.Font("font2.otf", 50)
        self.score_surf = pygame.Surface((0, 0))

        self.score_by_playtime = 0
        self.score_by_player = 0
        self.total_score = 0
        self.difficulty = 1

        #* collision
        self.colliables = []

    #TODO: Calculate the score and add it to a surface
    def calculateScore(self, time):
        self.score_by_playtime = time
        self.difficulty = int((self.platform_speed - 9) / 21 * 4) + 1
        self.total_score = self.player_sprite.score + self.score_by_playtime
        self.score_surf = self.font.render(f"Score: {self.total_score:05d} ", 0, "Black")
        
    
    def processEvent(self, events):
        super().processEvent(events)
        if self.player_sprite.is_dead:
            pygame.mixer_music.unload()
            sfx.player_die.play()
            return GameOver(self.total_score, self.difficulty)

        for event in events:
            #* Pausing the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_pause = True
                    self.previous_run_time = self.run_time
                    #* Get the state of the current instance of MainGame, so that when the player
                    #* unpauses the game, they will go back to the current game as it was before pause
                    #* instead of returning to the start of the game due to calling a new instance of MainGame
                    previous_state = self
                    return PauseMenu(previous_state)


    def generatePlatform(self):
        #* Increasing the speed by a constant each frame
        self.platform_speed = self.platform_speed + 0.05 / 40
        print(self.platform_speed)

        #* ensuring the speed does not exceed the maximum value
        if self.platform_speed >= 30:
            self.platform_speed = 30

        #* spawn a platform
        #* Spawn a new platform when the last platform reach SCREEN_WIDTH + 50
        if self.platform_group.sprites()[-1].rect.right <= SCREEN_WIDTH + 50:
            platform_info = generatePlatform(self.prev_platform_pos, 100, self.platform_speed)
            platform = platform_info["platform"]
            platform_type = platform_info["platform_type"]
            platform_width = platform_info["platform_width"]

            
            self.platform_group.add(platform)

            #* Temporary spawn logic: Spawn diamond when long platform is spawn and the random number is > 0.9
            if platform_type == "long":
                # if random.uniform(0, 1) > 0.2:
                    # self.collectibles_group.add(Diamond(platform.rect.left + 120, platform.rect.top - 20))

                
                
                if random.uniform(0, 1) > 0.6:
                    enemy = Enemy(platform.rect.right, platform.rect.top)
                    self.enemy_group.add(enemy)
                    self.enemy_group.add(Enemy(platform.rect.right - 200, platform.rect.top))
                    self.collectibles_group.add(platform.createDiamondPath(platform_type))
                    if random.uniform(0, 1) > 0.5:
                        self.collectibles_group.add(InvicibleCherry(platform.rect.right - platform_width / 2, platform.rect.top - 200))
                    
                    if random.uniform(0, 1) > 0.3:
                        for i in range(platform.rect.left + 20 * int(self.platform_speed), platform.rect.right - 20 * int(self.platform_speed) + 1, 75):
                            self.obstacle_group.add(Obstacle(i, platform.rect.top - 200, "img\\obstacles\\spike_ball.png"))    
                    
                else:
                    if platform.rect.top > self.prev_platform_pos.bottom:
                        obstacle = Obstacle(platform.rect.left + 200, platform.rect.top - 200, "img\\obstacles\\spike_ball.png")
                        self.obstacle_group.add(obstacle)
                        self.obstacle_group.add(Obstacle(platform.rect.right - 200, platform.rect.top - 200, "img\\obstacles\\spike_ball.png"))
                        self.obstacle_group.add(Obstacle(platform.rect.right - platform_width / 2, platform.rect.top - 5, "img\\obstacles\\spike_ball.png"))
                        
                    elif platform.rect.y < self.prev_platform_pos.y:
                        self.obstacle_group.add(Obstacle(platform.rect.right - platform_width / 2 - 100, platform.rect.top - 150, "img\\obstacles\\spike_ball.png"))
                        self.obstacle_group.add(Obstacle(platform.rect.right - platform_width / 2 + 100, platform.rect.top - 150, "img\\obstacles\\spike_ball.png"))
                        self.collectibles_group.add(platform.createDiamondPath(platform_type))
                        
                        
                    else:    
                        #obstacle = Obstacle((platform.rect.right - 5), platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                        #self.obstacle_group.add(obstacle)
                        #self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))
                        obstacle = Obstacle((platform.rect.right - platform_width / 2), platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                        self.obstacle_group.add(obstacle)
                        self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))

            else:
                self.collectibles_group.add(platform.createDiamondPath(platform_type))
                
            self.prev_platform_pos = platform.rect

    def showBackground(self):
        screen.blit(self.bg, (0 ,0))
        
        self.scrollBackground(self.background_layers[0], 0, 2)
        self.scrollBackground(self.background_layers[1], 1, 1)
        self.scrollBackground(self.background_layers[2], 2, 1.4)
        self.scrollBackground(self.background_layers[3], 3, 2.3)
        self.scrollBackground(self.background_layers[4], 4, 3)


    def render(self):
        screen.fill('Black')
        self.showBackground()
        #screen.blit(self.background, (0, 0))
        #self.scrollBackground()
        self.obstacle_group.draw(screen)
        self.enemy_group.draw(screen)
        self.platform_group.draw(screen)
        self.collectibles_group.draw(screen)
        self.bullets_group.draw(screen)
        if self.player_sprite.invicible_time > 0:
            pygame.draw.rect(screen, "blue", self.player_sprite.hitbox)
        self.player_group.draw(screen)
        
        screen.blit(self.score_frame, (640 - 200- 20, 10))
        screen.blit(self.score_surf, (640 - 155 - 20, 60))
    
    
    def scrollBackground(self, layer, index, speed):
        if (self.scrolls[index] > SCREEN_WIDTH):
            self.scrolls[index] = 0
        self.scrolls[index] += (self.platform_speed - 9) * speed

        for i in range(0, ceil(SCREEN_WIDTH / layer.get_width()) + 1 ):
            screen.blit(layer, (i * SCREEN_WIDTH - (self.scrolls[index]), 0))




    def update(self):
        if not self.player_sprite.is_dead and not self.is_pause:
            #* getting the second elapsed since MainGame ran as score
            self.run_time = self.previous_run_time + int((pygame.time.get_ticks() - self.start_time) / 1000)

            self.generatePlatform()
            self.platform_group.update(self.platform_speed)
            self.obstacle_group.update(self.platform_speed)
            self.enemy_group.update(self.platform_speed)
            self.player_group.update()
            self.bullets_group.update(self.colliables)
            self.collectibles_group.update(self.platform_speed)

            self.colliables = self.obstacle_group.sprites() + self.collectibles_group.sprites()
            self.player_sprite.handleAllCollisions(self.colliables, self.platform_group.sprites())

            for bullet in self.bullets_group.sprites():
                bullet.handlePlatformCollision(self.platform_group.sprites())
                if bullet is not None:
                    self.player_sprite.score += bullet.handleEnemyCollision(self.enemy_group.sprites())

            for enemy in self.enemy_group.sprites():
                self.player_sprite.score += self.player_sprite.handleEnemyCollision(enemy)

            self.calculateScore(self.run_time)
            self.render()


class GameOver(State):
    def __init__(self, score, difficulty):
        super(State, self).__init__()
        self.is_transitioned = False
        self.transition_counter = 0

        self.score = score
        self.difficulty = difficulty

    #TODO: Transition to the game over screen
    def transition(self):
        if not self.is_transitioned:

            #? Some logic stuff that I don't realy know how to explain
            #? basically spawn 6 rectangles coming from 2 edges of the screen interchangably and then move them
            if self.transition_counter <= SCREEN_WIDTH:
                for transition_index in range(0, 6, 2):
                    self.transition_counter += 15
                    pygame.draw.rect(screen, 'black', (0, transition_index * 120, self.transition_counter, SCREEN_HEIGHT / 6))
                    pygame.draw.rect(screen, 'black', (SCREEN_WIDTH - self.transition_counter, (transition_index + 1) * 120, SCREEN_WIDTH, SCREEN_HEIGHT / 6))

            else:
                self.is_transitioned = True
                self.render()

    def processEvent(self, events):
        super().processEvent(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return MainGame()

    #TODO: displaying text
    def render(self):
        #! This is just temporary
        font = pygame.font.Font("font.ttf", 35)

        text = font.render(f"GAME OVER", 0, 'White')
        text_score = font.render(f"Your score: {self.score} - Difficulty: {self.difficulty}", 0, 'White')
        text2 = font.render(f"Press R to play again", 0, 'White')

        screen.blit(text, text.get_rect(center = (SCREEN_WIDTH / 2, 300)))
        screen.blit(text_score, text_score.get_rect(center = ((SCREEN_WIDTH / 2, 400))))
        screen.blit(text2, text2.get_rect(center = ((SCREEN_WIDTH / 2, 500))))

    def update(self):
        self.transition()


#* I was so tired so I used chatGPT to generate this function ;) so still don't really understand wtf it does
def fade_transition(fade_surface, FADE_SPEED = 5, FADE_DELAY = 6000):
    start_time = pygame.time.get_ticks()
    while True:
        fade_rect = fade_surface.get_rect()

        # Calculate the time elapsed
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        # Display the splash screen for FADE_DELAY milliseconds
        if elapsed_time <= FADE_DELAY:
            alpha = min(255, int(elapsed_time / FADE_SPEED))
        else:
            alpha = max(0, 255 - int((elapsed_time - FADE_DELAY) / FADE_SPEED))

        # Create a copy of the splash screen image with the adjusted transparency
        faded_splash = fade_surface.copy()
        faded_splash.set_alpha(alpha)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Blit the faded splash screen onto the screen
        screen.blit(faded_splash, fade_rect)

        pygame.display.update()

        # Exit the loop after the fade-in and fade-out are complete
        if elapsed_time > FADE_DELAY + 255 * FADE_SPEED:
            break