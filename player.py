import pygame
import sfx
pygame.init()

PLAYER_JUMP_FORCE = 17


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
        #* creating player sprite
        self.image = pygame.transform.scale(pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun1.png").convert_alpha(), (100,100))
        self.rect = self.image.get_rect(midbottom = (150, 500))

        #* initializing player spirte animations
        self.player_anim_frame = 0
        self.player_run1 =  pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun1.png").convert_alpha()
        self.player_run2 =  pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun2.png").convert_alpha()
        self.player_run3 =  pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun3.png").convert_alpha()
        self.player_run4 =  pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun4.png").convert_alpha()
        self.player_run5 =  pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun5.png").convert_alpha()
        self.player_run6 =  pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun6.png").convert_alpha()
        self.player_run_anim = [self.player_run1, self.player_run2, self.player_run3, self.player_run4, self.player_run5, self.player_run6]
        self.player_jump = pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\jump\playerJump1.png").convert_alpha()
        self.player_descend = pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\jump\playerJump2.png").convert_alpha()
        self.previous_pos = self.rect.copy()
        
        #* jumping related 
        self.gravity = 0.8
        self.vertical_velocity = 0
        self.isColliding = False
        
    def getPlayerInput(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_SPACE] and (self.rect.bottom == 500 or self.isColliding)):
            self.makePlayerJump()

    def animatePlayer(self):

        self.player_anim_frame += 0.2

        if (self.player_anim_frame >= 6):
            self.player_anim_frame = 0


        #* Check if player is above the ground level and is not on another platform
        if (self.rect.bottom < 500 and not(self.isColliding) and self.vertical_velocity < 0):
            self.image = pygame.transform.scale(self.player_jump, (100, 100))
        elif(self.rect.bottom < 500 and not(self.isColliding) and self.vertical_velocity > 0):
            self.image = pygame.transform.scale(self.player_descend, (100, 100))
        else:        
            self.image = pygame.transform.scale(self.player_run_anim[int(self.player_anim_frame)], (100, 100))

    def makePlayerJump(self):
        self.vertical_velocity = -PLAYER_JUMP_FORCE
        sfx.player_jump.play()
        

    def affectGravityOnPlayer(self):
        self.vertical_velocity += self.gravity 
        if self.vertical_velocity > 20:
            self.vertical_velocity = 20; 
        self.rect.y += self.vertical_velocity
        if(self.rect.bottom >= 500):
            self.rect.bottom = 500

    def handleCollision(self, platforms):    
        on_platform = False
        if platforms is not None:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):  
                    if self.previous_pos.right > platform.previous_pos.left:
                        if (self.previous_pos.bottom <= platform.previous_pos.top):
                            self.rect.bottom = platform.rect.top
                            on_platform = True
                            self.isColliding = True
                            self.vertical_velocity = 0        
                        else:
                            self.isColliding = False
                            self.vertical_velocity = 1    
                            print("vei")
                    else:
                        self.rect.right = platform.rect.left
                        self.vertical_velocity = 1
                        
            if not on_platform:  
                self.isColliding = False
                    
                    
                #* Check if the player is pushed out of the screen then enter the game over
                if (self.rect.right < -5):
                    self.die() 
                    
            
        
    def die(self):
        print("Die!")
    
    def update(self):
        self.previous_pos = self.rect.copy()
        self.getPlayerInput()
        self.affectGravityOnPlayer()
        self.animatePlayer()
        
        
player = pygame.sprite.Group()
player.add(Player())