import pygame
import sfx
import settings as st

pygame.init()


screen = pygame.display.set_mode((st.SCREEN_WIDTH, st.SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
        #* creating player sprite
        self.image = pygame.transform.scale(pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun1.png").convert_alpha(), (100,100))
        self.rect = self.image.get_rect(midbottom = (150, 500))

        #* initializing player spirte animations
        self.player_anim_frame = 0

        #* import player sprites and scale it
        self.player_run_anim = [pygame.image.load(f"img\\Sprites\\player_run{i}.png").convert_alpha() for i in range(1,5)]
        self.player_run_anim = [pygame.transform.scale(image, (100, 100)) for image in self.player_run_anim]

        self.player_jump = pygame.transform.scale(pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\jump\\playerJump1.png").convert_alpha(), (100, 100))
        self.player_descend = pygame.transform.scale(pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\jump\\playerJump2.png").convert_alpha(), (100, 100))

        self.image = self.player_run_anim[self.player_anim_frame]
        self.rect = self.image.get_rect(midbottom = (150, 500))
        self.previous_position = self.rect.copy()
        
        #* jumping related 
        self.gravity = 1
        self.vertical_velocity = 0
        self.is_colliding = False
        self.jump_force = 17

        #* input related, see details in getPlayerInput()
        self.mouses_click = pygame.mouse.get_pressed()
        self.keys = pygame.key.get_pressed()
        self.is_dead = False    
        
        #* slash
        self.slash_hitbox = None
        self.slash_counter = 0
        self.is_slashing = 0
        
    #TODO: Get the player input 
    def getPlayerInput(self):

        #* This code check if the mouse is pressed once, prevent multiple input in 1 press
        self.keys = pygame.key.get_pressed()
        self.last_click = self.mouses_click
        self.mouses_click = pygame.mouse.get_pressed()

        if (self.keys[pygame.K_SPACE] and self.is_colliding):
            self.makePlayerJump()
        if self.mouses_click[0] and not self.last_click[0]:
            bullets.add(Bullets(self.rect.right, self.rect.centery))
            # self.is_slashing = True
            #? There's an error that the player will shoot when you click start the game.
            #? I think it is related to the bug I told you (the sound duplicated one)

    #TODO: animate the player 
    def animatePlayer(self):
        self.player_anim_frame += 0.2

        if (self.player_anim_frame >= 4):
            self.player_anim_frame = 0

        #* Check if player is above the ground level and is not on another platform
        if (self.rect.bottom < 500 and not(self.is_colliding) and self.vertical_velocity < 0):
            self.image = self.player_jump
        elif(self.rect.bottom < 500 and not(self.is_colliding) and self.vertical_velocity > 0):
            self.image = self.player_descend
        else:        
            self.image = self.player_run_anim[int(self.player_anim_frame)]

    #TODO: make the player jump
    def makePlayerJump(self):
        self.vertical_velocity = -self.jump_force
        sfx.player_jump.play()
        
    def strike(self):
        if (self.slash_counter >= 30):
            self.slash_counter = 0
            self.is_slashing = False
            self.slash_hitbox = None
        
        
        if self.is_slashing:
            self.slash_hitbox = pygame.Rect(self.rect.right, self.rect.top, 100, 100)
            pygame.draw.rect(screen, "Green", self.slash_hitbox)
            self.slash_counter += 1
            print("Strike")
        
    #TODO: pull the player down every frame by a constant amount
    def affectGravityOnPlayer(self):
        self.vertical_velocity += self.gravity 
        if self.vertical_velocity > 20:
            self.vertical_velocity = 20; 
        self.rect.y += self.vertical_velocity
        
        #* If the player falls out of the map, kill them
        if self.rect.top >= 700:
            self.die()

    #TODO: handle all the platform collision
    def handleCollision(self, platforms):    
        on_platform = False
        
        #* If exists at least one platform, check for the player collision with the platforms
        if platforms is not None:
            for platform in platforms:
                if self.rect.colliderect(platform.rect):  
                    #* check If the player entered the platform x on the last frame
                    if self.previous_pos.right > platform.previous_pos.left:
                        #* If the player successfully jumped on the platform
                        if (self.previous_pos.bottom <= platform.previous_pos.top):
                            self.rect.bottom = platform.rect.top
                            on_platform = True
                            self.is_colliding = True
                            self.vertical_velocity = 0    
                        
                        #? If the player was under a platform, they bong their head and falls down (this is nearly impossible to happen when there are no ground)    
                        else:
                            self.is_colliding = False
                            self.vertical_velocity = 1    
                            
                        #* If the player failed to jump on the platform, they are pushed leftward
                    else:
                        self.rect.right = platform.rect.left
                        self.vertical_velocity = 1
            
            #* if the player is not on any platforms present then they are not colliding with any platforms           
            if not on_platform:  
                self.is_colliding = False
                    
                    
                #* Check if the player is pushed out of the screen then enter the game over
                if (self.rect.right < -5):
                    self.die()
                    

    #TODO: handle enemy collisions
    def handleConllision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.die()
    
    
    #TODO: kill the player, thus ending the game
    def die(self):
        self.is_dead = True
        # self.kill()
    
    #TODO: update the state of the player
    def update(self):
        self.previous_pos = self.rect.copy()
        self.getPlayerInput()
        self.strike()
        self.affectGravityOnPlayer()
        self.animatePlayer()
        self.destroy()
    
    def destroy(self):
        if self.rect.top >= st.SCREEN_HEIGHT + 5:
            self.kill()



class Bullets(pygame.sprite.Sprite):
    def __init__(self, Player_right, Player_centery):
        super().__init__()

        self.Player_right, self.Player_centery = Player_right, Player_centery
        self.speed = 15
        self.image = pygame.Surface((10, 5))
        self.image.fill("darkgreen")

        self.rect = self.image.get_rect(midleft = (self.Player_right, self.Player_centery + 15))


        sfx.player_shoot.play()

    def moveBullet(self):
        self.rect.x += self.speed

    def update(self):
        self.destroy()
        self.moveBullet()
    
    def destroy(self):
        if self.rect.left > st.SCREEN_WIDTH + 5 or self.rect.top < -5 or self.rect.bottom >= st.SCREEN_HEIGHT:
            self.kill()

    def handlePlatformCollision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.kill()
                break

    def handleEnemyCollision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect) and not enemy.is_shot:
                enemy.shot()
                self.kill()
                return True
        return False

bullets = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()
