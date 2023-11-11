import pygame 
from random import randint, choice

pygame.init()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill('RED')
        self.rect = self.image.get_rect(topleft = (x_pos, y_pos))
        
        self.previous_pos = self.rect.copy()
    
    #TODO: move the platform leftward by a given speed
    def movePlatform(self, speed):
        self.rect.x -= speed
        if self.rect.right <= -5:
            self.kill()
            
    #TODO: update the state of the platform
    def update(self, speed):
        self.previous_pos = self.rect.copy()
        self.movePlatform(speed)  
        
    
#! My laptop encounters some lagging issues when running the game, but it is fine on stronger computers
#! Will think of a way to fix this, also try to make the game less frame dependent so it can run on multiple
#! platforms flawlessly
#! Also this platform generation logic is still pretty buggy, I'm thinking of a better sollution, in the mean time
#! this will get the job done.
class PlatformSpawner(object):
    def __init__(self):
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 2500
    
    def generatePlatform(self, prev_platform_pos: pygame.Rect, platform_gap, platform_speed):
        
        #* spawn the platform after 2.5s to prevent lag from continuous spawning
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_spawn_time >= self.spawn_delay:            
            if prev_platform_pos.top <= 200:
                prev_platform_pos.y += 200
            
            #* separate two platforms by a certain distance relative to their speed
            platform_x = prev_platform_pos.right + platform_gap * (platform_speed / 5.0)
            
            #* manipulate the platform y value according to the previous platform position
            if prev_platform_pos.bottom >= 500:
                platform_y = randint(prev_platform_pos.top - 50, prev_platform_pos.bottom - 30)
            else:
                platform_y = randint(prev_platform_pos.top - 50, prev_platform_pos.bottom + 100)
            
            #* get a random platform type and spawn it
            platform_type_set = ["long", "long", "long", "short"]
            platform_type = choice(platform_type_set)
            
            if platform_type == "long":
                platform_width = 600
            else:
                platform_width = 300
            
            return Platform(platform_x, platform_y, platform_width, 50)