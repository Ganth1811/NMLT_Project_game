import pygame 

pygame.init()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height, screen):
        super().__init__()
        
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft =  (self.x_pos, self.y_pos))
        self.image.fill('RED')
        
        self.screen = screen
        self.previous_pos = self.rect.copy()

        self.speed = 10
        
    def movePlatform(self):
        self.rect.x -= self.speed
    
    def update(self):
        self.previous_pos = self.rect.copy()
        self.movePlatform()



class Enemy(pygame.sprite.Sprite):
    def __init__(self, Platform_topright, Platform_speed):
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
        self.speed = Platform_speed * 1.2
        self.platform_topright = Platform_topright

    def animateEnemy(self):
        self.enemy_anim_frame += 0.2

        if (self.enemy_anim_frame >= 6):
            if self.is_shot:
                self.kill()
            self.enemy_anim_frame = 0
        
        self.image = self.enemy_anim_list[int(self.enemy_anim_frame)]

    def moveEnemy(self):
        self.rect.x -= self.speed
    
    def shot(self):
        self.is_shot = True
        self.enemy_anim_frame = 0
        self.enemy_anim_list = self.enemy_death_anim

    def update(self):     
        self.destroy()
        self.animateEnemy()
        self.moveEnemy()
    
    def destroy(self):
        if self.rect.right < 0:
            self.kill()



