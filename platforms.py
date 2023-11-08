import pygame 

pygame.init()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height, screen):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill('RED')
        
        self.screen = screen
        self.previous_pos = self.rect.copy()
        
    def movePlatform(self):
        self.rect.x -= 10
        
    
    def update(self):
        self.previous_pos = self.rect.copy()
        self.movePlatform()  
        
    
        