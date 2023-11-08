import pygame
import sfx
import settings as st

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #* initializing player spirte animations
        self.player_anim_frame = 0
        player_run1 = pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\Run\\playerRun1.png").convert_alpha()
        player_run2 = pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\Run\\playerRun2.png").convert_alpha()
        player_run3 = pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\Run\\playerRun3.png").convert_alpha()
        player_run4 = pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\Run\\playerRun4.png").convert_alpha()
        player_run5 = pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\Run\\playerRun5.png").convert_alpha()
        player_run6 = pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\Run\\playerRun6.png").convert_alpha()

        #* Scale player sprite
        player_run1 = pygame.transform.scale(player_run1, (100, 100))
        player_run2 = pygame.transform.scale(player_run2, (100, 100))
        player_run3 = pygame.transform.scale(player_run3, (100, 100))
        player_run4 = pygame.transform.scale(player_run4, (100, 100))
        player_run5 = pygame.transform.scale(player_run5, (100, 100))
        player_run6 = pygame.transform.scale(player_run6, (100, 100))

        self.player_run_anim = [player_run1, player_run2, player_run3, player_run4, player_run5, player_run6]

        self.player_jump = pygame.transform.scale(pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\jump\\playerJump1.png").convert_alpha(), (100, 100))
        self.player_descend = pygame.transform.scale(pygame.image.load("Sunny-land-files\\Graphical Assets\\sprites\\player\\jump\\playerJump2.png").convert_alpha(), (100, 100))

        self.image = pygame.transform.scale(self.player_run_anim[self.player_anim_frame], (100,100))
        self.rect = self.image.get_rect(midbottom = (150, 500))
        self.previous_position = self.rect.copy()
        
        #* jumping related 
        self.gravity = 0.8
        self.vertical_velocity = 0
        self.isColliding = False

        #* input related, see details in getPlayerInput()
        self.keys = pygame.key.get_pressed()
        
    def getPlayerInput(self):

        #* This code check if the button is pressed once, prevent multiple input in 1 press
        self.last_keys = self.keys
        self.keys = pygame.key.get_pressed()

        if (self.keys[pygame.K_SPACE] and (self.rect.bottom == 500 or self.isColliding)):
            self.makePlayerJump()
        if self.keys[pygame.K_a] and not self.last_keys[pygame.K_a]:
            bullets.add(Bullets(self.rect.right, self.rect.centery))

    def animatePlayer(self):

        self.player_anim_frame += 0.2

        if (self.player_anim_frame >= 6):
            self.player_anim_frame = 0


        #* Check if player is above the ground level and is not on another platform
        if (self.rect.bottom < 500 and not(self.isColliding) and self.vertical_velocity < 0):
            self.image = self.player_jump
        elif(self.rect.bottom < 500 and not(self.isColliding) and self.vertical_velocity > 0):
            self.image = self.player_descend
        else:        
            self.image = self.player_run_anim[int(self.player_anim_frame)]

    def makePlayerJump(self):
        self.vertical_velocity = -17
        sfx.player_jump.play()
        

    def affectGravityOnPlayer(self):
        self.vertical_velocity += self.gravity
        if self.vertical_velocity > 20:
            self.vertical_velocity = 20
        self.rect.y += self.vertical_velocity
        if (self.rect.bottom >= 500):
            self.rect.bottom = 500

    def checkCollision(self, platform):    
        
        if self.rect.colliderect(platform.rect):
            #print("Collided")    
            if self.previous_position.right > platform.previous_pos.left:
                print("COLLIDED UP")
                if (self.previous_position.bottom <= platform.previous_pos.top):
                    self.rect.bottom = platform.rect.top
                    self.isColliding = True
                    self.vertical_velocity = 0
                elif (self.previous_position.top >= platform.previous_pos.bottom):
                    self.isColliding = False
                    self.vertical_velocity = 1
            else:
                if self.previous_position.right <= platform.previous_pos.left:
                    self.rect.right = platform.rect.left
                    self.vertical_velocity = 1
        else:
            self.isColliding = False
        
        #^ Check if the player is pushed out of the screen then enter the game over
        if (self.rect.right < -5):
            self.die() 
        
    def die(self):
        print("Die!")
    
    def update(self):
        self.previous_position = self.rect.copy()
        self.getPlayerInput()
        self.affectGravityOnPlayer()
        self.animatePlayer()

class Bullets(pygame.sprite.Sprite):
    def __init__(self, Player_right, Player_centery):
        super().__init__()

        self.Player_right, self.Player_centery = Player_right, Player_centery
        self.speed = 5
        self.init_image = pygame.Surface((10, 5))
        self.init_image.fill("green")

        #* Vector related: Shooting aim
        mouse_x = pygame.mouse.get_pos()[0] - Player_right
        mouse_y = pygame.mouse.get_pos()[1] - Player_centery
        self.vector_mouse = pygame.Vector2()
        self.vector_mouse.xy = mouse_x, mouse_y
        pygame.math.Vector2.normalize_ip(self.vector_mouse)

        #* Rotate the bullet base on it's direction
        self.angle = self.vector_mouse.as_polar()[1]
        self.image = pygame.transform.rotate(self.init_image, self.angle)
        self.rect = self.image.get_rect(midleft = (self.Player_right, self.Player_centery))
        #? There's a problem when the rotate angle is about 45 degrees, the image becomes a square

        #* Precision related: see animateBullet()
        self.pos_x, self. pos_y = self.rect.x, self.rect.y

    def animateBullet(self):

        #* Because rect.x and rect.y can only be integer, the sai số will add up
        #* So I make another variables that can hold the exact location of the bullet
        self.pos_x += self.vector_mouse.x * self.speed
        self.pos_y += self.vector_mouse.y * self.speed
        self.rect.x, self.rect.y = self.pos_x, self.pos_y

    def update(self):
        self.destroy()
        self.animateBullet()
    
    def destroy(self):
        #* Limit the angle
        if abs(self.angle) > 75:
            self.kill()
        if self.rect.left > st.SCREEN_WIDTH + 5 or self.rect.top < -5 or self.rect.bottom >= 500:
            self.kill()

bullets = pygame.sprite.Group()

player = pygame.sprite.GroupSingle()
player.add(Player())