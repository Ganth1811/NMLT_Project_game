import pygame 
from random import randint, choice

pygame.init()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height, speed):
        super().__init__()
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill('RED')
        self.rect = self.image.get_rect(topleft = (x_pos, y_pos))

        
        self.previous_pos = self.rect.copy()
        self.speed = speed
        
    def movePlatform(self):
        self.rect.x -= self.speed
        if self.rect.right <= -5:
            self.kill()
    
    def update(self):
        self.previous_pos = self.rect.copy()
        self.movePlatform()  
        
    

class PlatformSpawner(object):
    def __init__(self):
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = 2500
    
    def generatePlatform(self, prev_platform_pos: pygame.Rect, platform_gap, platform_speed):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_spawn_time >= self.spawn_delay:            
            if prev_platform_pos.top <= 200:
                prev_platform_pos.y += 200
            
            platform_x = prev_platform_pos.right + platform_gap
            if prev_platform_pos.bottom >= 500:
                platform_y = randint(prev_platform_pos.top - 100, prev_platform_pos.bottom - 30)
            else:
                platform_y = randint(prev_platform_pos.top - 100, prev_platform_pos.bottom + 100)
            
            platform_type_set = ["long", "long", "long", "short"]
            platform_type = choice(platform_type_set)
            
            if platform_type == "long":
                platform_width = 500
            else:
                platform_width = 200
            
            
            return Platform(platform_x, platform_y, platform_width, 50, platform_speed)