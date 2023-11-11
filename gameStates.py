import pygame
from sys import exit
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import button as bt
import sfx
from player import player, bullets, Player
from platforms import Platform, PlatformSpawner, Enemy
import random



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
    def __init__(self):
        super(State, self).__init__()
    
    def processEvent(self, events):
        super().processEvent(events)
    
    def render(self):
        pass
    
    def update(self):
        pass
    
    

class MainGame(State):
    def __init__(self):
        super(State, self).__init__()
        
        #* background and other visual objects
        self.background = pygame.transform.scale(pygame.image.load("Sunny-land-files\\Graphical Assets\\environment\\Background\\Background.jpg").convert_alpha(), (1280, 720))
        self.ground_surface = pygame.Surface((1280,300))
        self.ground_surface.fill('darkolivegreen1')
        
        #* background music
        self.bg_music = pygame.mixer_music.load("music\\bgm\\game_bg_music.mp3")
        pygame.mixer_music.play(-1)
        
        #* player and bullets
        self.player_group = pygame.sprite.Group(Player())
        self.player_sprite: Player = self.player_group.sprites()[0]
        
        #* platforms
        self.platform_group = pygame.sprite.Group()
        self.init_platform = Platform(100, 500, 1200, 100)
        self.platform_group.add(Platform(0, 500, 3000, 100)) #* initial platform
        self.platform_spawner = PlatformSpawner()
        self.prev_platform_pos = self.init_platform.rect
        self.platform_speed = 10
        
        #* enemy
        self.enemy_group = pygame.sprite.Group()
        
        #* time
        self.start_time = pygame.time.get_ticks()
        self.dt = 0
        self.spawn_delay = 400
        self.bullets = bullets
    
    def processEvent(self, events):
        super().processEvent(events)
        if self.player_sprite.is_dead:
            pygame.mixer_music.unload()
            sfx.player_die.play()
            return GameOver()
            
    
        
    def generatePlatform(self):
        #* Increasing the speed by a constant each frame
        self.platform_speed = self.platform_speed + 0.05 / 40
        
        #* ensuring the speed does not exceed the maximum value
        if self.platform_speed >= 30:
            self.platform_speed = 30
        #print(self.platform_speed)
        
        #* spawn a platform
        platform = self.platform_spawner.generatePlatform(self.prev_platform_pos, 100, self.platform_speed)
        enemy = Enemy(platform.rect.topright, platform.speed)
        self.enemy_group.add(enemy)
        
        if platform is not None:   
            self.prev_platform_pos = platform.rect
            self.platform_group.add(platform)
    
    def render(self):
        screen.fill('Black')
        screen.blit(self.background, (0, 0))
        #screen.blit(self.ground_surface, (0, 500))
        self.platform_group.draw(screen)
        self.enemy_group.draw(screen)
        self.bullets_group.draw(screen)
        self.player_group.draw(screen)
    
    def update(self):
        if not self.player_sprite.is_dead:
            self.dt = pygame.time.get_ticks() / 1000
            
            self.generatePlatform()
            self.platform_group.update(self.platform_speed)
            
            self.player_group.update()
            self.enemy_group.update()
            
            self.player_sprite.handleCollision(self.platform_group.sprites())
            self.bullets_group.update()
            for bullet in self.bullets_group.sprites():
                bullet.handlePlatformCollision(self.platform_group.sprites())
                bullet.handleEnemyCollision(self.enemy_group.sprites())
            
            self.render()

class GameOver(State):
    def __init__(self):
        super(State, self).__init__()
        self.is_transitioned = False
        self.transition_counter = 0
        
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
                if event.key == pygame.K_SPACE:
                    return MainGame()

    #TODO: displaying text
    def render(self):
        #! This is just temporary
        font = pygame.font.Font("font.ttf", 35)
        text = font.render(f"GAME OVER", 0, 'White')
        text2= font.render(f"press space to play again", 0, 'White')
        screen.blit(text, (SCREEN_WIDTH / 2 - 100, 300))
        screen.blit(text2, (SCREEN_WIDTH / 2 - 200, 400))
        
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