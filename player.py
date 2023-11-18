import pygame
import sfx
import settings as st

pygame.init()


screen = pygame.display.set_mode((st.SCREEN_WIDTH, st.SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_position = (120, 500)

        #* initializing player spirte animations
        self.player_anim_frame = 0

        #* import player sprites and scale it    
        
        #* running
        self.player_run_anim = [pygame.image.load(f"img\\Sprites\\player_run{i}.png").convert_alpha() for i in range(1,5)]
        self.player_run_anim = [pygame.transform.scale_by(image, 4) for image in self.player_run_anim]

        #* jumping
        self.player_jump = pygame.image.load("img\\Sprites\\player_jump.png").convert_alpha()
        self.player_jump_anim = [self.player_jump]  + [pygame.image.load(f"img\\Sprites\\player_spin{i}.png").convert_alpha() for i in range(1,5)]
        self.player_jump_anim = [pygame.transform.scale_by(image, 4) for image in self.player_jump_anim]
        self.player_descend = pygame.transform.scale_by(pygame.image.load("img\\Sprites\\player_fall.png").convert_alpha(), 4)
        
        #* slashing
        self.player_slash_anim = [pygame.image.load(f"img\\Sprites\\player_attack{i}.png").convert_alpha() for i in range(1,5)]
        self.player_slash_anim = [pygame.transform.scale_by(image, 4) for image in self.player_slash_anim]

        self.image = self.player_run_anim[self.player_anim_frame]
        self.rect = self.image.get_rect(bottomleft = self.player_position)
        self.previous_position = self.rect.copy()
        
        #* jumping related 
        self.gravity = 1
        self.vertical_velocity = 0
        self.is_colliding = False
        self.jump_force = 18.5
        self.player_jump_frame = 0

        #* input related, see details in getPlayerInput()
        self.mouses_click = pygame.mouse.get_pressed()
        self.keys = pygame.key.get_pressed()
        self.is_dead = False
        
        #* slash
        self.slash_frame = 0
        self.is_slashing = 0
        
        self.score = 0
        
        #* hitbox
        self.hitbox = pygame.Rect(0, 0, 12 * 4, 22 * 4)
        self.hitbox.bottomleft = (self.rect.left + 6 * 4, self.rect.bottom)
        self.is_spinning = False
        

    #TODO: Get the player input 
    def getPlayerInput(self):

        #* This code check if the mouse is pressed once, prevent multiple input in 1 press
        self.keys = pygame.key.get_pressed()
        self.last_click = self.mouses_click
        self.mouses_click = pygame.mouse.get_pressed()

        if (self.keys[pygame.K_SPACE] and self.is_colliding):
            self.makePlayerJump()
        if self.mouses_click[0] and not self.last_click[0] and not self.is_slashing:
            bullets.add(Bullets(self.rect.right, self.rect.centery))
            self.is_slashing = True
            # print(self.is_slashing)
            #? There's an error that the player will shoot when you click start the game.
            #? I think it is related to the bug I told you (the sound duplicated one)

    def animatePlayerJump(self):
        self.player_jump_frame += 0.2

        if (self.player_jump_frame >= 5):
            self.player_jump_frame = 0
        self.image = self.player_jump_anim[int(self.player_jump_frame)]
        
        if self.player_jump_frame >= 1:
            self.is_spinning = True
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)

    def animatePlayerSlash(self):
        self.slash_frame += 0.4
        
        if (self.slash_frame >= 4):
            self.is_slashing = 0
            self.slash_frame = 0
            return
        
        self.image = self.player_slash_anim[int(self.slash_frame)]
        self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        

    #TODO: animate the player 
    def animatePlayer(self):
        self.player_anim_frame += 0.2

        if (self.player_anim_frame >= 4):
            self.player_anim_frame = 0

        if self.is_slashing:
            self.animatePlayerSlash()
            self.is_spinning = False  
        #* Check if player is above the ground level and is not on another platform
        elif (self.rect.bottom < 500 and not(self.is_colliding) and self.vertical_velocity < 6):
            self.animatePlayerJump()
        elif(self.rect.bottom < 500 and not(self.is_colliding) and self.vertical_velocity > 7):
            self.image = self.player_descend
            self.is_spinning = False
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        else:        
            self.player_jump_frame = 0
            self.image = self.player_run_anim[int(self.player_anim_frame)]
        

    #TODO: make the player jump
    def makePlayerJump(self):
        self.vertical_velocity = -self.jump_force
        sfx.player_jump.play()
        
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
    def handlePlatformCollision(self, platforms):    
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
    def handleEnemyCollision(self, enemy):
        if not enemy.is_shot:
            self.die()

    def collectCollectible(self, collectible):
        self.score += collectible.playerCollect()

    def handleAllCollisions(self, colliables, platforms):
        self.handlePlatformCollision(platforms)     
        for colliable in colliables:
            if self.hitbox.colliderect(colliable.rect):
                if colliable.type == "enemy":
                    self.handleEnemyCollision(colliable)
                if colliable.type == "obstacle":
                    self.die()
                if colliable.type == "diamond":
                    self.collectCollectible(colliable)
    
    def getHitbox(self):
        if not self.is_spinning:
            self.hitbox = pygame.Rect(0, 0, 12 * 4, 22 * 4)
            self.hitbox.bottomleft = (self.rect.left + 6 * 4, self.rect.bottom)
        else:
            self.hitbox = pygame.Rect(0, 0, 17 * 4, 17 * 4)
            self.hitbox.bottomleft = (self.rect.left, self.rect.bottom)
    
    #TODO: kill the player, thus ending the game
    def die(self):
        self.is_dead = True
        # self.kill()
    
    #TODO: update the state of the player
    def update(self):
        self.previous_pos = self.rect.copy()
        self.getPlayerInput()
        self.affectGravityOnPlayer()
        self.animatePlayer()
        self.getHitbox()
        



class Bullets(pygame.sprite.Sprite):
    def __init__(self, Player_right, Player_centery):
        super().__init__()

        self.Player_right, self.Player_centery = Player_right, Player_centery
        self.speed = 15
        self.image = pygame.transform.scale(pygame.image.load("img\\Sprites\\slash.png"), (110, 100)).convert_alpha()

        self.rect = self.image.get_rect(midleft = (self.Player_right - 30, self.Player_centery))

        sfx.player_shoot.play()

    def moveBullet(self):
        self.rect.x += self.speed
        if self.rect.left > st.SCREEN_WIDTH + 5 or self.rect.top < -5 or self.rect.bottom >= st.SCREEN_HEIGHT:
            self.kill()

    def update(self, colliables):
        self.moveBullet()

    def handlePlatformCollision(self, platform_group):
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                self.kill()

    def handleEnemyCollision(self, enemy_group):
        for enemy in enemy_group:
            if self.rect.colliderect(enemy.rect) and not enemy.is_shot:
                enemy.shot()
                self.kill()
                return enemy.given_score
        return 0


bullets = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()
