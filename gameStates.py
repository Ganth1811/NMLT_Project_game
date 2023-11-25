import pygame
from sys import exit
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FRAMERATE, MAX_SPEED, score
import button as bt
import sfx
from player import Player
from platforms import Obstacle, Platform, generatePlatform, Enemy, InvicibleCherry, RemoveHostile, Multiplier
import random
from math import ceil
from image import SplashScreenImg, TitleMenuImg, MainGameImg

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
    def update(self, dt):
        pass



#* The splash screen displays the logo of the group for a few seconds then fades out
class SplashScreen(State):
    def __init__(self):
        super(State, self).__init__()
        self.splash_screen = SplashScreenImg.splash_screen
        self.fade = False
        self.alpha = 0
        self.bg_music = pygame.mixer_music.load("music\\bgm\\menu_theme.mp3")
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


    def update(self, dt):
        self.render()

#* The title menu displays the game name and different options player can choose
class TitleMenu(State):
    def __init__(self):
        super(State, self).__init__()


        self.background = pygame.image.load("img\\Bg\\bg.jpg").convert_alpha()
        self.text_quest_of = TitleMenuImg.text_quest_of
        self.text_athelard = TitleMenuImg.text_athelard
        self.text_timer = 0
        self.particle_group = []

        self.bg_music = pygame.mixer_music.load("music\\bgm\\menu_theme.mp3")
        pygame.mixer_music.play(-1)

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
        
        self.text_timer += 0.5
        if self.text_timer >= 18:
            self.text_timer = 0
            
        screen.blit(self.text_quest_of[int(self.text_timer)], (130, 50))
        screen.blit(self.text_athelard[int(self.text_timer)], (115, 170))
        
        if self.text_timer % 5 == 0:
            self.particle_group.append(Particle())
            
        for particle in self.particle_group:
            if particle is not None:
                particle.update()

    def update(self, dt):
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

    def update(self, dt):
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
        self.bg = pygame.transform.scale(MainGameImg.bg, (1280, 720))
        self.background_layers = [pygame.transform.scale(image, (1280, 720)) for image in MainGameImg.bg_layers]
        
        #* background music
        self.bg_music = pygame.mixer_music.load("music\\bgm\\game_bg_music.mp3")
        pygame.mixer_music.play(-1)

        #* player and bullets
        self.player_group = pygame.sprite.GroupSingle(Player())
        self.player_sprite = self.player_group.sprites()[0]
        self.bullet_group = self.player_sprite.bullet_group

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
        self.time_before = 0
        self.is_day = True
        self.day_counter = 0
        self.background_counter = 0

        #* pausing mechanism
        self.is_pause = False

        #* score
        self.score_frame = MainGameImg.score_frame
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
        time_elapsed = time - self.time_before
        if time_elapsed >= 1:
            self.time_before = time
            self.score_by_playtime += time_elapsed * self.player_sprite.current_multipler

        self.difficulty = int((self.platform_speed - 9) / (MAX_SPEED - 9) * 4) + 1
        self.total_score = self.player_sprite.score + self.score_by_playtime
        self.score_surf = self.font.render(f"Score: {int(self.total_score):05d} ", 0, "Black")
        
        
        
    
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


    def generateGameObjects(self):
        #* Increasing the speed by a constant each frame
        if self.difficulty <= 2:
            self.platform_speed += 0.1 / 40
        else:
            self.platform_speed += 0.05 / 40
        # print(self.platform_speed)

        #* ensuring the speed does not exceed the maximum value
        if self.platform_speed >= MAX_SPEED:
            self.platform_speed = MAX_SPEED

        #* spawn a platform
        #* Spawn a new platform when the last platform reach SCREEN_WIDTH + 50
        if self.platform_group.sprites()[-1].rect.right <= SCREEN_WIDTH + 50:
            platform_info = generatePlatform(self.prev_platform_pos, 100, self.platform_speed)
            platform = platform_info["platform"]
            platform_type = platform_info["platform_type"]
            platform_width = platform_info["platform_width"]
            self.platform_group.add(platform)

            #* spawn logic
            if platform_type == "long":
                #* easy difficulty
                if self.difficulty < 2:
                    if random.uniform(0, 1) <= 0.3:
                        self.enemy_group.add(Enemy(platform.rect.right - 100, platform.rect.top))
                        self.collectibles_group.add(platform.createDiamondPath(platform_type))                     
                        
                    elif random.uniform(0, 1) <= 0.7:
                        obstacle = Obstacle(platform.rect.centerx, platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                        self.obstacle_group.add(obstacle)
                        self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))
                        
                    else:
                        self.collectibles_group.add(platform.createDiamondPath(platform_type))
                
                #* medium difficulty
                elif self.difficulty < 4:
                    #* enemy
                    if random.uniform(0, 1) <= 0.3:
                        #* spawn two enemies in the middle and the end of the platform respectively
                        self.enemy_group.add(Enemy(platform.rect.centerx, platform.rect.top))
                        self.enemy_group.add(Enemy(platform.rect.right - 100, platform.rect.top))
                        self.collectibles_group.add(platform.createDiamondPath(platform_type))
                        
                        #* a row of obstacles on top prevent the player from jumping
                        if random.uniform(0, 1) > 0.3:
                            for i in range(platform.rect.left + 20 * int(self.platform_speed), platform.rect.right - 20 * int(self.platform_speed) + 1, 75):
                                self.obstacle_group.add(Obstacle(i, platform.rect.top - 200, "img\\obstacles\\spike_ball.png"))    
                                
                    # *obstacles
                    elif random.uniform(0, 1) <= 0.9:
                        if platform.rect.top < self.prev_platform_pos.top:
                            #* an obstacle high up at the end of the platform, prevent the player from jumping early
                            if random.uniform(0, 1) > 0.5:
                                self.obstacle_group.add(Obstacle(platform.rect.right - 100, platform.rect.top - 200, "img\\obstacles\\spike_ball.png"))
                            
                            #* spawn the Multiplier
                            if random.uniform(0, 1) <= 0.31 and self.player_sprite.multiplier_cd == 0:
                                self.collectibles_group.add(Multiplier(platform.rect.centerx - 10, platform.rect.top - 200))
                            
                            #* an obstacle in the middle
                            obstacle = Obstacle(platform.rect.centerx, platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                            self.obstacle_group.add(obstacle)
                            self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))
                        
                        #* a group of three zic-zac obstacles
                        elif platform.rect.top >= self.prev_platform_pos.bottom:
                            self.obstacle_group.add(Obstacle(platform.rect.left + 200, platform.rect.top - 200, "img\\obstacles\\spike_ball.png"))
                            
                            obstacle = Obstacle(platform.rect.left + 500, platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                            self.obstacle_group.add(obstacle)
                            self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))
                            
                            self.obstacle_group.add(Obstacle(platform.rect.left + 500 + 300, platform.rect.top - 200, "img\\obstacles\\spike_ball.png"))
                        
                        
                        else:
                            #* an obstacle in the left of the platform prevents early jumping
                            self.obstacle_group.add(Obstacle(platform.rect.left, platform.rect.top - 5, "img\\obstacles\\spike_ball.png"))
                            
                            obstacle = Obstacle(platform.rect.left + 500, platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                            self.obstacle_group.add(obstacle)
                            self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))
                            
                            self.collectibles_group.add(platform.createDiamondPath(platform_type))
                            
                            #* spawn the inviciblle potion
                            if random.uniform(0, 1) <= 0.25 and self.player_sprite.invincible_cd == 0:
                                self.collectibles_group.add(InvicibleCherry(platform.rect.centerx - 100 , platform.rect.top - 200))
                            
                    else:
                        self.collectibles_group.add(platform.createDiamondPath(platform_type))

                    
                
                
                #* Hard difficulty
                else:
                    if random.uniform(0, 1) <= 0.4:
                        #* spawn two enemies in the middle and the end of the platform respectively
                        self.enemy_group.add(Enemy(platform.rect.centerx + 10, platform.rect.top))
                        self.enemy_group.add(Enemy(platform.rect.right - 100, platform.rect.top))
                        self.collectibles_group.add(platform.createDiamondPath(platform_type))
                        
                        #* a row of obstacles on top prevent the player from jumping
                        for i in range(platform.rect.left + 20 * int(self.platform_speed), platform.rect.right - 20 * int(self.platform_speed) + 1, 75):
                            self.obstacle_group.add(Obstacle(i, platform.rect.top - 200, "img\\obstacles\\spike_ball.png"))    
                        
                    else:
                        if platform.rect.top <= self.prev_platform_pos.top:
                            #* an obstacle high up at the end of the platform, prevent the player from jumping early
                            if random.uniform(0, 1) > 0.1:
                                self.obstacle_group.add( Obstacle(platform.rect.right - 100, platform.rect.top - 200, "img\\obstacles\\spike_ball.png"))
                            
                            #* an obstacle in the middle
                            obstacle = Obstacle(platform.rect.centerx, platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                            self.obstacle_group.add(obstacle)
                            self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))
                            
                            #* spawn the Multiplier
                            if random.uniform(0, 1) <= 0.31 and self.player_sprite.multiplier_cd == 0:
                                self.collectibles_group.add(Multiplier(platform.rect.centerx + 100, platform.rect.top - 200))
                        
                        #* a group of five zic-zac obstacles
                        if platform.rect.top >= self.prev_platform_pos.bottom:
                            #* high
                            self.obstacle_group.add(Obstacle(platform.rect.left + 200, platform.rect.top - 210, "img\\obstacles\\spike_ball.png"))
                            
                            #* low
                            obstacle = Obstacle(platform.rect.left + 500, platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                            self.obstacle_group.add(obstacle)
                            self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))
                            
                            #* high
                            self.obstacle_group.add(Obstacle(platform.rect.left + 500 + 300, platform.rect.top - 210, "img\\obstacles\\spike_ball.png"))
                            
                            if self.difficulty == 5:
                                #* low
                                obstacle = Obstacle(platform.rect.left + 1150, platform.rect.top - 5, "img\\obstacles\\spike_ball.png")
                                self.obstacle_group.add(obstacle)
                                self.collectibles_group.add(obstacle.createDiamondPath(self.player_sprite, self.platform_speed))
                                
                                #* high
                                self.obstacle_group.add(Obstacle(platform.rect.left + 1200 + 300, platform.rect.top - 210, "img\\obstacles\\spike_ball.png"))
                        
                        #* an obstacle at the start of the platform prevents early jumping
                        else: 
                            self.obstacle_group.add(Obstacle(platform.rect.left, platform.rect.top - 10, "img\\obstacles\\spike_ball.png")) 
                            
                            #* spawn the inviciblle potion
                            if random.uniform(0, 1) <= 0.25 and self.player_sprite.invincible_cd == 0:
                                self.collectibles_group.add(InvicibleCherry(platform.rect.centerx , platform.rect.top - 200))

                        #* spawn the obstacle deleter
                        if random.uniform(0, 1) <= 0.15 and self.player_sprite.shock_wave_cd == 0:
                            self.collectibles_group.add(RemoveHostile(platform.rect.right + 100, platform.rect.top - 200))
                        
            else:
                self.collectibles_group.add(platform.createDiamondPath(platform_type)) 
            
            self.prev_platform_pos = platform.rect

    def showBackground(self, dt):
        
        
        self.scrollBackground(self.background_layers[0], 0, 0.8, dt)
        self.scrollBackground(self.background_layers[1], 1, 0.1, dt)
        self.scrollBackground(self.background_layers[2], 2, 0.6, dt)
        self.scrollBackground(self.background_layers[3], 3, 0.9, dt)
        self.scrollBackground(self.background_layers[4], 4, 0.4, dt)


    
    def cycleDayAndNight(self, dt):
        
        if self.is_day:
            self.day_counter += (1 * dt * TARGET_FRAMERATE) / 30
            if self.day_counter >= 100:
                self.is_day = False
        else:
            self.day_counter -= (1 * dt * TARGET_FRAMERATE) / 30
            if self.day_counter <= 0:
                self.is_day = True
        
        
        blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        blur.set_alpha(self.day_counter)
        screen.blit(blur, (0, 0))
        print(self.day_counter)
        
    
    def darkenBackground(self, dt):
        
        if self.is_day:
            self.background_counter += (1 * dt * TARGET_FRAMERATE) / 25
                
        else:
            self.background_counter -= (1 * dt * TARGET_FRAMERATE) / 25

        
        
        blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        blur.set_alpha(self.day_counter)
        screen.blit(blur, (0, 0))
        print(self.day_counter)
        



    def render(self, dt):
        screen.fill('Black')
        screen.blit(self.bg, (0 ,0))
        self.darkenBackground(dt)
        
        
        
        self.showBackground(dt)
        
        self.platform_group.draw(screen)
        
        if self.player_sprite.invicible_time > 0:
            pygame.draw.rect(screen, "blue", self.player_sprite.hitbox)
        self.player_group.draw(screen)
        
        
        self.cycleDayAndNight(dt)
        
        
        self.collectibles_group.draw(screen)
        self.bullet_group.draw(screen)
        self.obstacle_group.draw(screen)
        self.enemy_group.draw(screen)
        
        
        
        screen.blit(self.score_frame, (640 - 200- 20, 10))
        screen.blit(self.score_surf, (640 - 155 - 20, 60))

        if self.player_sprite.shockwave is not None and not self.player_sprite.shockwave.over:
            self.player_sprite.shockwave.drawShockwave(screen, dt)
        
        
    
    
    def scrollBackground(self, layer, index, speed, dt):
        if (self.scrolls[index] > SCREEN_WIDTH):
            self.scrolls[index] = 0
        self.scrolls[index] += (self.platform_speed - 9) * speed * dt * TARGET_FRAMERATE

        for i in range(0, ceil(SCREEN_WIDTH / layer.get_width()) + 1 ):
            screen.blit(layer, (i * SCREEN_WIDTH - (self.scrolls[index]), 0))


    def update(self, dt):
        if not self.player_sprite.is_dead and not self.is_pause:
            #* getting the second elapsed since MainGame ran as score
            self.run_time = self.previous_run_time + int((pygame.time.get_ticks() - self.start_time) / 1000)
            if self.total_score > score.high_score:
                score.high_score = self.total_score
                with open('score.high_score.txt', 'w') as file:
                    file.write(str(self.total_score))

            self.generateGameObjects()
            self.platform_group.update(self.platform_speed, dt)
            self.obstacle_group.update(self.platform_speed, dt)
            self.enemy_group.update(self.platform_speed, dt)
            self.player_group.update(dt)
            self.bullet_group.update(dt)
            self.collectibles_group.update(self.platform_speed, dt)

            self.colliables = self.obstacle_group.sprites() + self.collectibles_group.sprites()
            self.player_sprite.handleAllCollisions(self.colliables, self.platform_group.sprites())
            self.bullet_group = self.player_sprite.bullet_group

            for bullet in self.bullet_group.sprites():
                bullet.handlePlatformCollision(self.platform_group.sprites())
                if bullet is not None:
                    self.player_sprite.score += bullet.handleEnemyCollision(self.enemy_group.sprites()) * self.player_sprite.current_multipler

            for enemy in self.enemy_group.sprites():
                self.player_sprite.score += self.player_sprite.handleEnemyCollision(enemy) * self.player_sprite.current_multipler
            
            if self.player_sprite.shockwave is not None: 
                self.player_sprite.shockwave.clearHostile(self.obstacle_group.sprites() + self.enemy_group.sprites())
                if self.player_sprite.shockwave.over:
                    self.player_sprite.shockwave = None

            self.calculateScore(self.run_time)
            self.render(dt)

            
            
                    
            

class GameOver(State):
    
    def __init__(self, score, difficulty):
        super(State, self).__init__()
        self.is_transitioned = False
        self.transition_counter = 0

        self.score = score
        self.difficulty = difficulty

    #TODO: Transition to the game over screen
    def transition(self, dt):
        if not self.is_transitioned:
            if self.transition_counter <= SCREEN_WIDTH:
                for transition_index in range(0, 6, 2):
                    self.transition_counter += 15 * dt * TARGET_FRAMERATE
                    pygame.draw.rect(screen, 'black', (0, transition_index * 120, self.transition_counter + 100, SCREEN_HEIGHT / 6))
                    pygame.draw.rect(screen, 'black', (SCREEN_WIDTH - self.transition_counter, (transition_index + 1) * 120, SCREEN_WIDTH + 100, SCREEN_HEIGHT / 6))

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
        text_high_score = font.render(f"Highest score: {score.high_score}", 0, 'White')

        screen.blit(text, text.get_rect(center = (SCREEN_WIDTH / 2, 300)))
        screen.blit(text_score, text_score.get_rect(center = ((SCREEN_WIDTH / 2, 400))))
        screen.blit(text_high_score, text_high_score.get_rect(center = ((SCREEN_WIDTH / 2, 500))))
        screen.blit(text2, text2.get_rect(center = ((SCREEN_WIDTH / 2, 600))))

    def update(self, dt):
        self.transition(dt)


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
        
        
class Particle():
    def __init__(self):
        self.rect = pygame.Rect(-1, random.randint(50, 700), 5, 5)
        self.speed = random.randint(1, 3)
        self.remove = False
        self.radius = random.randint(2, 5)

    
    
    def update(self):
        self.rect.x += self.speed
        pygame.draw.circle(screen,pygame.Color('Red'), (self.rect.x, self.rect.y), self.radius)
        if self.rect.x > SCREEN_WIDTH:
            self.remove= True
            