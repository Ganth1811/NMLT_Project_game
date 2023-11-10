import pygame
from sys import exit
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import button as bt
import sfx
from player import player, bullets



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
        pygame.mixer_music.play(-1)
        self.clock = pygame.time.Clock()
            
    
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
        
        #background and other visual objects
        self.background = pygame.transform.scale(pygame.image.load("Sunny-land-files\\Graphical Assets\\environment\\Background\\Background.jpg").convert_alpha(), (1280, 720))
        self.ground_surface = pygame.Surface((1280,300))
        self.ground_surface.fill('darkolivegreen1')
        
        #background music
        self.bg_music = pygame.mixer_music.load("music\\bgm\\game_bg_music.mp3")
        pygame.mixer_music.play(-1)
        
        #player and bullets
        self.player = player
        self.bullets = bullets
    
    def processEvent(self, events):
        super().processEvent(events)
    
    def render(self):
        screen.fill('Black')
        screen.blit(self.background, (0, 0))
        screen.blit(self.ground_surface, (0, 500))
        self.player_group.draw(screen)
        self.platform_group.draw(screen)
        self.bullets.draw(screen)
    
    def update(self):
        self.generatePlatform()
        self.platform_group.update()
        self.player_group.update()
        self.player_sprite.handleCollision(self.platform_group.sprites())
        self.bullets.update()
        self.render()


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

