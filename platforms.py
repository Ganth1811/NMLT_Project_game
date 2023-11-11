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
        self.rect = self.image.get_rect(topleft =  (self.x_pos, self.y_pos))
        self.image.fill('RED')
        
        self.previous_pos = self.rect.copy()
        
    #TODO: move the platform leftward by a given speed
    def movePlatform(self, speed):
        self.rect.x -= speed
        if self.rect.right <= -5:
            self.kill()
            del self
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
        # self.last_spawn_time = pygame.time.get_ticks()
        # self.spawn_delay = 2500
        pass
    
    def generatePlatform(self, prev_platform_pos: pygame.Rect, platform_gap, platform_speed):
        
        #* spawn the platform after 2.5s to prevent lag from continuous spawning
        # self.current_time = pygame.time.get_ticks()
        # if self.current_time - self.last_spawn_time >= self.spawn_delay:            
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
        
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self, Platform_topright):#, Platform_speed):
        super().__init__()

        #* initializing enemy spirte animations
        self.enemy_anim_frame = 0

        #* import player enemy and scale it
        self.enemy_run_anim = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\Enemy\\enemyRun{i}.png").convert_alpha() for i in range(1,7)]
        self.enemy_run_anim = [pygame.transform.rotozoom(image, 0, 2) for image in self.enemy_run_anim]

        self.enemy_death_anim = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\enemy-death\\enemy-death-{i}.png").convert_alpha() for i in range(1,7)]
        self.enemy_death_anim = [pygame.transform.rotozoom(image, 0, 2) for image in self.enemy_death_anim]

        self.enemy_anim_list = self.enemy_run_anim

        self.image = self.enemy_anim_list[self.enemy_anim_frame]
        self.rect = self.image.get_rect(bottomright = Platform_topright)
        
        self.is_shot = False
        #self.speed = Platform_speed * 1.2
        self.platform_topright = Platform_topright

    def animateEnemy(self):
        self.enemy_anim_frame += 0.2

        if (self.enemy_anim_frame >= 6):
            if self.is_shot:
                self.kill()
            self.enemy_anim_frame = 0
        
        self.image = self.enemy_anim_list[int(self.enemy_anim_frame)]

    def moveEnemy(self, speed):
        self.rect.x -= speed + 0.1
    
    def shot(self):
        self.is_shot = True
        self.enemy_anim_frame = 0
        self.enemy_anim_list = self.enemy_death_anim

    def update(self, speed):     
        self.destroy()
        self.animateEnemy()
        self.moveEnemy(speed)
    
    def destroy(self):
        if self.rect.right < 0:
            self.kill()
            del self