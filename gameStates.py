import pygame
from sys import exit
import random
from math import ceil

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FRAMERATE, INIT_SPEED, MAX_SPEED, Score
import settings as st
import button as bt
import sfx
from player import Player
from gameObject import Obstacle, Platform, Enemy, Coin, InvinciblePotion, MagicOrb, Emerald
from image import SplashScreenImg, TitleMenuImg, MainGameImg

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class State(object):
    #TODO: initialize general properties of the state class and its subclass
    def __init__(self):
        self.screen = screen

    #TODO: processing the events
    def processEvent(self, events: list[pygame.event.Event]):
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
        self.start_time = pygame.time.get_ticks()

        sfx.adjustSoundVolume()
        sfx.loadMenuTheme()

    def processEvent(self, events: list[pygame.event.Event]):
        super().processEvent(events)
        if self.fade:
            return TitleMenu()

    def fade_transition(self, fade_surface: pygame.Surface, FADE_SPEED = 2, FADE_DELAY = 4000):
        fade_rect = fade_surface.get_rect()

        # Calculate the time elapsed
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time

        # Display the splash screen for FADE_DELAY milliseconds
        if elapsed_time <= FADE_DELAY:
            alpha = min(255, int(elapsed_time / FADE_SPEED))
        else:
            alpha = max(0, 255 - int((elapsed_time - FADE_DELAY) / FADE_SPEED))

        # Create a copy of the splash screen image with the adjusted transparency
        faded_splash = fade_surface.copy()
        faded_splash.set_alpha(alpha)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Blit the faded splash screen onto the screen
        screen.blit(faded_splash, fade_rect)

        pygame.display.update()

        # Stop calling the function after the fade-in and fade-out are complete
        if elapsed_time > FADE_DELAY + 255 * FADE_SPEED:
            self.fade = True

    def render(self):
        #* Check if the Splash Screen is in the fading procress then fade it in
        if not self.fade:
            self.fade_transition(self.splash_screen)

    def update(self, dt):
        self.render()

#* The title menu displays the game name and different options player can choose
class TitleMenu(State):
    def __init__(self):
        super(State, self).__init__()

        self.background = TitleMenuImg.background
        self.text_quest_of = TitleMenuImg.text_quest_of
        self.text_athelard = TitleMenuImg.text_athelard
        self.text_timer = 0
        self.particle_group = []
        self.is_in_high_score = False
        self.is_in_how_to_play = False
        self.displayed_score = None
        self.event_processed = False

        # sfx.adjustSoundVolume()

        #* initialize the button objects
        self.buttons = self.createButtons()
        self.close_button = pygame.sprite.Group(bt.close_button)

    #TODO: create the buttons and add them to a dictionary
    def createButtons(self):
        new_game_button = bt.new_game_button
        high_score_button = bt.high_score_button
        quit_game_button = bt.quit_game_button
        how_to_play_button = bt.how_to_play_button
        mute_button = bt.mute_button

        #* creating the buttons dictionary to detect which button is being pressed
        button_names = {
            "new_game": new_game_button,
            "high_score": high_score_button,
            "quit_game": quit_game_button,
            "how_to_play": how_to_play_button,
            "mute": mute_button
        }

        #* creating the button group to draw the buttons
        button_group = pygame.sprite.Group()
        button_group.add(button_names.values())

        #* return both of the button types
        return {
            "button_names": button_names,
            "button_group": button_group
        }

    def processEvent(self, events: list[pygame.event.Event]):
        super().processEvent(events)

        for event in events:
            #* quitting the game using ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            #* Switching the game state acording to the button pressed by the player
            if event.type == pygame.MOUSEBUTTONDOWN and not self.event_processed:
                if not self.is_in_how_to_play and not self.is_in_high_score:
                    for button_name, button in self.buttons["button_names"].items():
                        if button.isClicked():
                            sfx.button_pressed.play()

                            if button_name == "quit_game":
                                pygame.quit()
                                exit()

                            elif button_name == "new_game":
                                pygame.mixer_music.unload()
                                return MainGame()

                            elif button_name == "high_score":
                                self.is_in_high_score = True

                            elif button_name == "mute":
                                st.is_muted = not st.is_muted
                                sfx.adjustSoundVolume()

                            elif button_name == "how_to_play":
                                self.is_in_how_to_play = True

                        self.event_processed = True

                else:
                    if self.close_button.sprites()[0].isClicked():
                        sfx.button_pressed.play()
                        self.is_in_how_to_play = False
                        self.is_in_high_score = False

    def displayHighscore(self):
        blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        blur.set_alpha(69)
        screen.blit(blur, (0, 0))

        font = pygame.font.Font("font.ttf", 40)

        high_score_popup = TitleMenuImg.high_score_popup
        popup_rect = high_score_popup.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(TitleMenuImg.high_score_popup, popup_rect)

        score_list = Score.high_score_list
        for i in range(len(score_list)):
            if i == 0:
                rank_line = font.render(f'{i+1}.', 1, 'Yellow')
                score_line = font.render(str(score_list[i][0]), 1, 'Yellow')
                date_line = font.render(score_list[i][1], 1, 'Yellow')
            else:
                rank_line = font.render(f'{i+1}.', 1, 'White')
                score_line = font.render(str(score_list[i][0]), 1, 'White')
                date_line = font.render(score_list[i][1], 1, 'White')

            screen.blit(rank_line, (300, 300 + 75 * i))
            screen.blit(score_line, (375, 300 + 75 * i))
            screen.blit(date_line, (680, 300 + 75 * i))

    def render(self):
        screen.blit(self.background, (0, 0))

        if not self.is_in_how_to_play and not self.is_in_high_score:
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

        if self.is_in_how_to_play:
            blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            blur.set_alpha(69)
            screen.blit(blur, (0, 0))

            how_to_play_popup = TitleMenuImg.how_to_play_popup
            popup_rect = how_to_play_popup.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(TitleMenuImg.how_to_play_popup, popup_rect)

            self.close_button.draw(screen)

        elif self.is_in_high_score:
            self.displayHighscore()
            self.close_button.draw(screen)


        # if self.is_in_high_score:
        #     screen.blit(img.)

    def handleButtons(self):
        if not self.is_in_how_to_play and not self.is_in_high_score:
            self.buttons["button_group"].update()
        else:
            for button in self.buttons["button_group"].sprites():
                button.hovered = False
            self.close_button.update()
        self.event_processed = False

    def update(self, dt):
        self.handleButtons()
        self.render()

#* The pause menu displays the pause screen and pause the game temporarily
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
        blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        blur.set_alpha(69)
        screen.blit(blur, (0, 0))

    def createButtons(self):
        resume_button = bt.resume_button
        restart_button = bt.restart_button
        main_menu_button = bt.main_menu_button
        mute_button = bt.mute_button

        #* creating the buttons dictionary to detect which button is being pressed
        button_names = {
            "resume": resume_button,
            "restart": restart_button,
            "main_menu": main_menu_button,
            "mute": mute_button
        }

        #* creating the button group to draw the buttons
        button_group = pygame.sprite.Group()
        button_group.add(button_names.values())

        #* return both of the button types
        return {
            "button_names": button_names,
            "button_group": button_group
        }

    def processEvent(self, events: list[pygame.event.Event]):
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
                            sfx.loadMenuTheme()
                            return TitleMenu()

                        elif button_name == "mute":
                            st.is_muted = not st.is_muted
                            sfx.adjustSoundVolume()

    def render(self):
        self.buttons["button_group"].draw(screen)

    def update(self, dt):
        self.render()
        self.buttons["button_group"].update()

#* The main state of the game while running
class MainGame(State):
    def __init__(self):
        super(State, self).__init__()

        #* background and other visual objects
        self.scrolls = [2, 1, 1.4, 1.3, 1.2]
        self.bg = pygame.transform.scale(MainGameImg.bg, (1280, 720))
        #self.background_layers = [pygame.transform.scale(image, (1280, 720)) for image in MainGameImg.bg_layers]
        self.bg_layer_1 = Background(MainGameImg.bg_1, 0.4)
        self.bg_layer_2 = Background(MainGameImg.bg_2, 0.8)
        self.bg_layer_3 = Background(MainGameImg.bg_3, 1)
        self.bg_layer_4 = Background(MainGameImg.bg_4, 1.3)
        self.bg_layer_5 = Background(MainGameImg.bg_5, 1.4)

        #* background music
        sfx.loadBgMusic()

        #* player and bullets
        self.player_sprite = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player_sprite)
        self.bullet_group = self.player_sprite.bullet_group

        #* platforms
        self.platform_group = pygame.sprite.Group()
        self.init_platform = Platform(100, 500, 1200, 100)
        self.platform_group.add(Platform(0, 500, 3000, 100)) #* initial platform
        self.prev_platform_pos = self.init_platform.rect
        self.platform_speed = INIT_SPEED

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
        self.day_duration = 60
        self.background_counter = 0
        self.death_countdown = 60 * 2

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
        self.scroll = 0

    #TODO: Calculate the score and add it to a surface
    def calculateScore(self, time):
        time_elapsed = time - self.time_before
        if time_elapsed >= 1:
            self.time_before = time
            self.score_by_playtime += time_elapsed * self.player_sprite.current_multiplier

        self.difficulty = ceil((self.platform_speed - 10) / (MAX_SPEED - 10) * 5)
        self.total_score = self.player_sprite.score + self.score_by_playtime
        self.score_surf = self.font.render(f"Score: {int(self.total_score):05d} ", 0, "Black")

    def processEvent(self, events: list[pygame.event.Event]):
        super().processEvent(events)
        if self.player_sprite.is_dead:
            pygame.mixer_music.unload()
            if self.death_countdown <= 0:
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
            platform_info = Platform.generatePlatform(self.prev_platform_pos, 100, self.platform_speed)
            platform = platform_info["platform"]
            platform_type = platform_info["platform_type"]
            self.platform_group.add(platform)

            #* spawn logic
            if platform_type == "long":
                #* easy difficulty
                if self.difficulty < 2:
                    if random.uniform(0, 1) <= 0.3:
                        self.enemy_group.add(Enemy(platform.rect.right - 100, platform.rect.top))
                        self.collectibles_group.add(Coin.spawnCoin(platform.rect, platform_type))

                    elif random.uniform(0, 1) <= 0.7:
                        obstacle = Obstacle(platform.rect.centerx, platform.rect.top, "low")
                        self.obstacle_group.add(obstacle)
                        self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center))

                    else:
                        self.collectibles_group.add(Coin.spawnCoin(platform.rect, platform_type))

                #* medium difficulty
                elif self.difficulty < 4:
                    #* enemy
                    if random.uniform(0, 1) <= 0.4:
                        if random.uniform(0, 1) <= 0.3 and self.difficulty == 3:
                            #* spawn like a tons of enemies
                            self.enemy_group.add(Enemy(platform.rect.centerx, platform.rect.top))
                            self.enemy_group.add(Enemy(platform.rect.right - 100, platform.rect.top))
                            self.enemy_group.add(Enemy(platform.rect.right - 200, platform.rect.top))
                            self.collectibles_group.add(Coin.spawnCoin(platform.rect, platform_type))

                        else:
                            #* spawn two enemies in the middle and the end of the platform respectively
                            self.enemy_group.add(Enemy(platform.rect.centerx, platform.rect.top))
                            self.enemy_group.add(Enemy(platform.rect.right - 100, platform.rect.top))
                            self.collectibles_group.add(Coin.spawnCoin(platform.rect, platform_type))



                        #* a row of obstacles on top prevent the player from jumping
                        if random.uniform(0, 1) > 0.3:
                            for i in range(platform.rect.left + 20 * int(self.platform_speed), platform.rect.right - 20 * int(self.platform_speed) + 1, 75):
                                self.obstacle_group.add(Obstacle(i, platform.rect.top - 190, "high"))

                    # *obstacles
                    elif random.uniform(0, 1) <= 0.9:
                        if platform.rect.top < self.prev_platform_pos.top:
                            #* an obstacle high up at the end of the platform, prevent the player from jumping early
                            if random.uniform(0, 1) > 0.5:
                                self.obstacle_group.add(Obstacle(platform.rect.right - 100, platform.rect.top - 190, "high"))
                            obstacle = Obstacle(platform.rect.centerx, platform.rect.top, "low")

                            #* spawn the Multiplier
                            if random.uniform(0, 1) <= 0.31 and self.player_sprite.multiplier_cd == 0:
                                self.collectibles_group.add(Emerald(platform.rect.centerx, platform.rect.top - 200))
                                self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center, True))

                            else:
                                self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center))

                            #* an obstacle in the middle
                            self.obstacle_group.add(obstacle)

                        #* a group of three zic-zac obstacles
                        elif platform.rect.top >= self.prev_platform_pos.bottom:
                            self.obstacle_group.add(Obstacle(platform.rect.left + 200, platform.rect.top - 190, "high"))

                            obstacle = Obstacle(platform.rect.left + 500, platform.rect.top, "low")
                            self.obstacle_group.add(obstacle)
                            self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center))

                            self.obstacle_group.add(Obstacle(platform.rect.left + 500 + 300, platform.rect.top - 190, "high"))


                        else:
                            #* an obstacle in the left of the platform prevents early jumping
                            self.obstacle_group.add(Obstacle(platform.rect.left, platform.rect.top, "low"))

                            obstacle = Obstacle(platform.rect.left + 500, platform.rect.top, "low")
                            self.obstacle_group.add(obstacle)

                            #* spawn the inviciblle potion
                            if random.uniform(0, 1) <= 0.25 and self.player_sprite.invincible_cd == 0:
                                self.collectibles_group.add(InvinciblePotion(platform.rect.left + 500, platform.rect.top - 200))
                                self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center, True))

                            else:
                                self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center))

                    else:
                        self.collectibles_group.add(Coin.spawnCoin(platform.rect, platform_type))

                #* Hard difficulty
                else:
                    if random.uniform(0, 1) <= 0.4:
                        if random.uniform(0, 1) <= 0.4:
                            self.enemy_group.add(Enemy(platform.rect.centerx + 300, platform.rect.top))
                            self.enemy_group.add(Enemy(platform.rect.centerx + 600, platform.rect.top))
                        #* spawn two enemies in the middle and the end of the platform respectively

                        self.enemy_group.add(Enemy(platform.rect.centerx + 10, platform.rect.top))
                        self.enemy_group.add(Enemy(platform.rect.right - 5, platform.rect.top))
                        self.collectibles_group.add(Coin.spawnCoin(platform.rect, platform_type))

                        #* a row of obstacles on top prevent the player from jumping
                        for i in range(platform.rect.left + 20 * int(self.platform_speed), platform.rect.right - 20 * int(self.platform_speed) + 1, 75):
                            self.obstacle_group.add(Obstacle(i, platform.rect.top - 190, "high"))

                    else:
                        if platform.rect.top <= self.prev_platform_pos.top:
                            #* an obstacle high up at the end of the platform, prevent the player from jumping early
                            if random.uniform(0, 1) > 0.1:
                                self.obstacle_group.add(Obstacle(platform.rect.right - 100, platform.rect.top - 190, "high"))

                            #* an obstacle in the middle
                            obstacle = Obstacle(platform.rect.centerx, platform.rect.top, "low")
                            self.obstacle_group.add(obstacle)


                            #* spawn the Multiplier
                            if random.uniform(0, 1) <= 0.31 and self.player_sprite.multiplier_cd == 0:
                                self.collectibles_group.add(Emerald(platform.rect.centerx, platform.rect.top - 200))
                                self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center, True))
                            else:
                                self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center))

                        #* a group of five zic-zac obstacles
                        if platform.rect.top >= self.prev_platform_pos.bottom:
                            #* high
                            self.obstacle_group.add(Obstacle(platform.rect.left + 200, platform.rect.top - 210, "high"))

                            #* low
                            obstacle = Obstacle(platform.rect.left + 500, platform.rect.top, "low")
                            self.obstacle_group.add(obstacle)
                            self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center))

                            #* high
                            self.obstacle_group.add(Obstacle(platform.rect.left + 500 + 300, platform.rect.top - 210, "high"))

                            if self.difficulty >= 5:
                                #* low
                                obstacle = Obstacle(platform.rect.left + 1150, platform.rect.top, "low")
                                self.obstacle_group.add(obstacle)
                                self.collectibles_group.add(Coin.spawnCoinCurve(self.player_sprite, self.platform_speed, obstacle.rect.center))

                                #* high
                                self.obstacle_group.add(Obstacle(platform.rect.left + 1200 + 300, platform.rect.top - 210, "high"))

                        #* an obstacle at the start of the platform prevents early jumping
                        else:
                            self.obstacle_group.add(Obstacle(platform.rect.left, platform.rect.top, "low"))

                            #* spawn the inviciblle potion
                            if random.uniform(0, 1) <= 0.25 and self.player_sprite.invincible_cd == 0:
                                self.collectibles_group.add(InvinciblePotion(platform.rect.centerx , platform.rect.top - 200))


                        #* spawn the obstacle deleter
                        if random.uniform(0, 1) <= 0.25 and self.player_sprite.shock_wave_cd == 0:
                            self.collectibles_group.add(MagicOrb(platform.rect.right + 100, platform.rect.top - 200))

            else:
                self.collectibles_group.add(Coin.spawnCoin(platform.rect, platform_type))

            self.prev_platform_pos = platform.rect

    def render(self, dt):
        screen.fill('Black')
        screen.blit(self.bg, (0 ,0))
        self.bg_layer_1.draw()
        self.bg_layer_2.draw()
        self.bg_layer_3.draw()
        self.bg_layer_4.draw()
        self.bg_layer_5.draw()

        self.platform_group.draw(screen)
        self.collectibles_group.draw(screen)
        self.bullet_group.draw(screen)
        self.obstacle_group.draw(screen)
        self.enemy_group.draw(screen)
        self.player_group.draw(screen)

        screen.blit(self.score_frame, (640 - 200- 20, 10))
        screen.blit(self.score_surf, (640 - 155 - 20, 60))

        if self.player_sprite.shockwave is not None and not self.player_sprite.shockwave.over:
            self.player_sprite.shockwave.drawShockwave(screen, dt)

        if not self.player_sprite.is_dead:
            if self.player_sprite.invicible_time > 0:
                icon = MainGameImg.popup_invincible
                screen.blit(icon, icon.get_rect(topright = self.player_sprite.rect.topleft))
            if self.player_sprite.multiplier_time > 0:
                icon = MainGameImg.popup_x2
                screen.blit(icon, icon.get_rect(midright = (self.player_sprite.rect.left, self.player_sprite.rect.centery)))

    def handleGameEvent(self):
        colliables = self.obstacle_group.sprites() + self.collectibles_group.sprites() + self.enemy_group.sprites()
        self.player_sprite.handleAllCollisions(colliables, self.platform_group.sprites())

        for bullet in self.bullet_group.sprites():
            bullet.handlePlatformCollision(self.platform_group.sprites())
            if bullet is not None:
                self.player_sprite.score += bullet.handleEnemyCollision(self.enemy_group.sprites()) * self.player_sprite.current_multiplier

        if self.player_sprite.shockwave is not None:
            self.player_sprite.shockwave.clearHostile(self.obstacle_group.sprites() + self.enemy_group.sprites())
            if self.player_sprite.shockwave.over:
                self.player_sprite.shockwave = None

    def update(self, dt):
        if not self.player_sprite.is_dead and not self.is_pause:

            self.scroll += 1
            if self.scroll >= SCREEN_WIDTH:
                self.scroll = 0

            self.bg_layer_1.update(dt)
            self.bg_layer_2.update(dt)
            self.bg_layer_3.update(dt)
            self.bg_layer_4.update(dt)
            self.bg_layer_5.update(dt)

            #* getting the second elapsed since MainGame ran as score
            self.run_time = self.previous_run_time + int((pygame.time.get_ticks() - self.start_time) / 1000)

            self.generateGameObjects()
            self.platform_group.update(self.platform_speed, dt)
            self.obstacle_group.update(self.platform_speed, dt)
            self.enemy_group.update(self.platform_speed, dt)
            self.player_group.update(dt)
            self.bullet_group.update(dt)
            self.collectibles_group.update(self.platform_speed, dt)

            self.handleGameEvent()
            self.calculateScore(self.run_time)
            self.render(dt)

        else:
            self.death_countdown -= 1 * dt * TARGET_FRAMERATE
            # self.player_group.update(dt)
            # self.handleGameEvent()
            self.player_sprite.animatePlayer(dt)
            self.render(dt)

#* The state where the player dies and the game is stopped, displaying the score and other info
class GameOver(State):
    def __init__(self, score, difficulty):
        super(State, self).__init__()
        self.is_transitioned = False
        self.transition_counter = 0

        self.score = score
        self.difficulty = difficulty

        self.buttons = self.createButtons()
        self.is_new_high_score = Score.updateHighScore(score)

        self.font1 = pygame.font.Font("font.ttf", 60)
        self.font2 = pygame.font.Font("font.ttf", 40)

        sfx.loadGameOverMusic()


    #TODO: Transition to the game over screen
    def transition(self, dt):
        if not self.is_transitioned:
            if self.transition_counter <= SCREEN_WIDTH + 20 * dt * TARGET_FRAMERATE:
                for transition_index in range(0, 6, 2):
                    self.transition_counter += 15 * dt * TARGET_FRAMERATE
                    pygame.draw.rect(screen, 'black', (0, transition_index * 120, self.transition_counter + 100, SCREEN_HEIGHT / 6))
                    pygame.draw.rect(screen, 'black', (SCREEN_WIDTH - self.transition_counter, (transition_index + 1) * 120, SCREEN_WIDTH + 100, SCREEN_HEIGHT / 6))

            else:
                self.is_transitioned = True

    def createButtons(self):
        restart_button = bt.restart_button
        main_menu_button = bt.main_menu_button

        #* creating the buttons dictionary to detect which button is being pressed
        button_names = {
            "restart": restart_button,
            "main_menu": main_menu_button,
        }

        #* creating the button group to draw the buttons
        button_group = pygame.sprite.Group()
        button_group.add(button_names.values())

        #* return both of the button types
        return {
            "button_names": button_names,
            "button_group": button_group
        }

    def processEvent(self, events: list[pygame.event.Event]):
        super().processEvent(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return MainGame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, button in self.buttons["button_names"].items():
                    if button.isClicked():
                        sfx.button_pressed.play()

                        if button_name == "restart":
                            return MainGame()

                        elif button_name == "main_menu":
                            sfx.loadMenuTheme()
                            return TitleMenu()

    #TODO: displaying text
    def render(self):
        pygame.draw.rect(screen, 'black', (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        text_game_over = self.font1.render(f"GAME OVER", 0, 'White')

        if self.is_new_high_score:
            text_score = self.font2.render(f"New high score: {self.score} - Difficulty: {self.difficulty}", 0, 'Yellow')
        else:
            text_score = self.font2.render(f"Your score: {self.score} - Difficulty: {self.difficulty}", 0, 'White')

        text_high_score = self.font2.render(f"Highest score: {Score.high_score_list[0][0]}", 0, 'White')
        # text2 = font.render(f"Press R to play again", 0, 'White')

        screen.blit(text_game_over, text_game_over.get_rect(center = (SCREEN_WIDTH / 2, 100)))
        screen.blit(text_score, text_score.get_rect(center = ((SCREEN_WIDTH / 2, 275))))
        screen.blit(text_high_score, text_high_score.get_rect(center = ((SCREEN_WIDTH / 2, 350))))
        # screen.blit(text2, text2.get_rect(center = ((SCREEN_WIDTH / 2, 400))))

        self.buttons["button_group"].draw(screen)

    def update(self, dt):
        self.transition(dt)
        if self.is_transitioned:
            self.render()
            self.buttons["button_group"].update()


class Particle():
    def __init__(self):
        self.rect = pygame.Rect(-1, random.randint(50, 700), 5, 5)
        self.speed = random.randint(1, 3)
        self.remove = False
        self.radius = random.randint(2, 5)
        self.radius = random.randint(2, 5)
        self.radius = random.randint(2, 5)

    def update(self):
        self.rect.x += self.speed
        pygame.draw.circle(screen,pygame.Color('White'), (self.rect.x, self.rect.y), self.radius)
        if self.rect.x > SCREEN_WIDTH:
            self.remove = True


class Background():
    def __init__(self, img, speed):
        self.x = 0
        self.y = 0
        self.speed = speed
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()
    def draw(self):
        screen.blit(self.img, (int(self.x), int(self.y)))
        screen.blit(self.img, (int(self.x + self.width), int(self.y)))
    def update(self, dt):
        self.x -= self.speed * dt * TARGET_FRAMERATE
        if self.x < -self.width - 100:
            self.x += self.width