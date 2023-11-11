import pygame
import sfx
import settings as st

pygame.init()



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
        #* creating player sprite
        self.image = pygame.transform.scale(pygame.image.load("Sunny-land-files\Graphical Assets\sprites\player\Run\playerRun1.png").convert_alpha(), (100,100))
        self.rect = self.image.get_rect(midbottom = (150, 500))

        #* initializing player spirte animations
        self.player_anim_frame = 0

        #* import player sprites and scale it
        self.player_run_anim = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\player\\Run\\playerRun{i}.png").convert_alpha() for i in range(1,7)]
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
            #? There's an error that the player will shoot when you click start the game.
            #? I think it is related to the bug I told you (the sound duplicated one)

    #TODO: animate the player 
    def animatePlayer(self):
        self.player_anim_frame += 0.2

        if (self.player_anim_frame >= 6):
            self.player_anim_frame = 0

        #* Check if player is above the ground level and is not on another platform
        if (self.rect.bottom < 500 and not(self.is_colliding) and self.vertical_velocity < 0):
            self.image = pygame.transform.scale(self.player_jump, (100, 100))
        elif(self.rect.bottom < 500 and not(self.is_colliding) and self.vertical_velocity > 0):
            self.image = pygame.transform.scale(self.player_descend, (100, 100))
        else:        
            self.image = pygame.transform.scale(self.player_run_anim[int(self.player_anim_frame)], (100, 100))

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
                    
    #TODO: kill the player, thus ending the game
    def die(self):
        self.is_dead = True
        self.kill()
    
    #TODO: update the state of the player
    def update(self):
        self.previous_pos = self.rect.copy()
        self.getPlayerInput()
        self.affectGravityOnPlayer()
        self.animatePlayer()



class Bullets(pygame.sprite.Sprite):
    def __init__(self, Player_right, Player_centery):
        super().__init__()

        self.Player_right, self.Player_centery = Player_right, Player_centery
        self.speed = 15
        self.init_image = pygame.Surface((10, 5))
        self.init_image.fill("darkgreen")

        #* Vector related: Shooting aim
        mouse_x = pygame.mouse.get_pos()[0] - Player_right
        mouse_y = pygame.mouse.get_pos()[1] - Player_centery
        self.vector_mouse = pygame.Vector2()
        self.vector_mouse.xy = mouse_x, mouse_y
        pygame.math.Vector2.normalize_ip(self.vector_mouse)

        #* Rotate the bullet base on its direction
        self.angle = self.vector_mouse.as_polar()[1]
        self.image = pygame.transform.rotate(self.init_image, self.angle)
        self.rect = self.image.get_rect(midleft = (self.Player_right, self.Player_centery))
        #? There's a problem when the rotate angle is about 45 degrees, the image becomes a square

        #* Precision related: see moveBullet()
        self.pos_x, self. pos_y = self.rect.x, self.rect.y

        sfx.player_shoot.play()

    def moveBullet(self):

        #* Because rect.x and rect.y can only be integer, the sai số will add up
        #* So I make variables that can hold the exact location of the bullet
        self.pos_x += self.vector_mouse.x * self.speed
        self.pos_y += self.vector_mouse.y * self.speed
        self.rect.x, self.rect.y = self.pos_x, self.pos_y

    def update(self):
        self.destroy()
        self.moveBullet()
    
    def destroy(self):

        #* Limit the angle
        if abs(self.angle) > 75:
            self.kill()
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
                break

bullets = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()
