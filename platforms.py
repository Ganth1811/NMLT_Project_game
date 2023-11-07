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
        self.rect = self.image.get_rect(topleft = (self.x_pos, self.y_pos))
        self.image.fill('RED')
        self.screen = screen
        self.previous_pos = self.rect.copy()

    def movePlatform(self):
        self.x_pos -= 10
        if (self.x_pos <= -1000):
            self.x_pos = 1280
        
    def drawPlatform(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        self.previous_pos = self.rect.copy()
        self.movePlatform()
        self.drawPlatform()
        
    def __del__(self):
        pass    
        
        
    
        