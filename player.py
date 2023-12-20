import pygame

import sfx
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FRAMERATE
from image import PlayerImg, BulletImg

pygame.init()

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.player_position = (120, 500)

        #* initializing player spirte animations
        self.player_anim_frame = 0
        self.player_die_frame = 0

        #* running
        self.player_run_anim = PlayerImg.run_anim

        #* jumping
        self.player_jump_anim = PlayerImg.jump_anim
        self.player_descend = PlayerImg.descend

        #* slashing
        self.player_slash_anim = PlayerImg.slash_anim

        #* die and explode
        self.player_die_anim = PlayerImg.die_anim
        self.player_explode_anim = PlayerImg.explode_anim

        self.image = self.player_run_anim[self.player_anim_frame]
        self.rect = self.image.get_rect(bottomleft = self.player_position)
        self.previous_pos = self.rect.copy()

        #* jumping related
        self.gravity = 1
        self.vertical_velocity = 0
        self.is_colliding = False
        self.jump_force = 18
        self.player_jump_frame = 0

        #* input related, see details in getPlayerInput()
        self.mouses_click = pygame.mouse.get_pressed()
        self.keys = pygame.key.get_pressed()
        self.is_dead = False

        #* slash
        self.slash_frame = 0
        self.is_slashing = 0
        self.bullet_group = pygame.sprite.Group()
        self.score = 0

        #* hitbox
        self.hitbox = pygame.Rect(0, 0, 12 * 4, 22 * 4)
        self.hitbox.bottomleft = (self.rect.left + 6 * 4, self.rect.bottom)

        #* special power
        self.invicible_time = 0
        self.i_frame = 0
        self.shockwave = None
        self.multiplier_time = 0
        self.current_multiplier = 1
        self.multiplier_cd = 0
        self.invincible_cd = 0
        self.shock_wave_cd = 0

    #TODO: Get the player input
    def getPlayerInput(self):

        #* This code check if the mouse is pressed once, prevent multiple input in 1 press
        self.keys = pygame.key.get_pressed()
        self.last_click = self.mouses_click
        self.mouses_click = pygame.mouse.get_pressed()

        if (self.keys[pygame.K_SPACE] and self.is_colliding):
            self.makePlayerJump()
        if self.mouses_click[0] and not self.last_click[0] and not self.is_slashing:
            self.bullet_group.add(Bullet(self.rect.right, self.rect.centery))
            self.is_slashing = True
            #? There's an error that the player will shoot when you click start the game.

    def animatePlayerJump(self, dt):
        self.player_jump_frame += 0.2 * dt * TARGET_FRAMERATE

        if (self.player_jump_frame >= 5):
            self.player_jump_frame = 0
        self.image = self.player_jump_anim[int(self.player_jump_frame)]

    def animatePlayerSlash(self, dt):
        self.slash_frame += 0.4 * dt * TARGET_FRAMERATE

        if (self.slash_frame >= 4):
            self.is_slashing = 0
            self.slash_frame = 0
            return

        self.image = self.player_slash_anim[int(self.slash_frame)]


    #TODO: animate the player
    def animatePlayer(self, dt):

        if not self.is_dead:
            if self.invicible_time > 0:

                self.player_run_anim = PlayerImg.run_anim_invi

                #* jumping
                self.player_jump_anim = PlayerImg.jump_anim_invi
                self.player_descend = PlayerImg.descend_invi

                #* slashing
                self.player_slash_anim = PlayerImg.slash_anim_invi

            else:
                self.player_run_anim = PlayerImg.run_anim

                #* jumping
                self.player_jump_anim = PlayerImg.jump_anim
                self.player_descend = PlayerImg.descend

                #* slashing
                self.player_slash_anim = PlayerImg.slash_anim

            self.player_anim_frame += 0.2 * dt * TARGET_FRAMERATE

            if (self.player_anim_frame >= 4):
                self.player_anim_frame = 0

            if self.is_slashing:
                self.animatePlayerSlash(dt)
            #* Check if player is above the ground level and is not on another platform
            elif (self.rect.bottom < 500 and not(self.is_colliding) and self.vertical_velocity < 6):
                self.animatePlayerJump(dt)
            elif(self.rect.bottom < 500 and not(self.is_colliding) and self.vertical_velocity > 7):
                self.image = self.player_descend
            else:
                self.player_jump_frame = 0
                self.image = self.player_run_anim[int(self.player_anim_frame)]

            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)

        else:
            self.player_die_frame += 0.1 * dt * TARGET_FRAMERATE
            if self.player_die_frame > 12:
                self.player_die_frame = 12
            if self.player_die_frame < 4:
                self.image = self.player_die_anim[int(self.player_die_frame)]
                self.rect = self.image.get_rect(center = self.rect.center)
            else:
                self.image = self.player_explode_anim[int(self.player_die_frame) - 4]
                self.rect = self.image.get_rect(center = self.rect.center)

    #TODO: make the player jump
    def makePlayerJump(self):
        self.vertical_velocity = -self.jump_force
        sfx.player_jump.play()

    #TODO: pull the player down every frame by a constant amount
    def affectGravityOnPlayer(self, dt):
        self.vertical_velocity += self.gravity * dt * TARGET_FRAMERATE
        if self.vertical_velocity > 20:
            self.vertical_velocity = 20
        self.rect.y += self.vertical_velocity * dt * TARGET_FRAMERATE

        #* If the player falls out of the map, kill them
        if self.rect.top >= 700:
            self.die()

    #TODO: handle all the platform collision
    def handlePlatformCollision(self, platforms: list[pygame.sprite.Sprite]):
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
    def handleEnemyCollision(self, enemy: pygame.sprite.Sprite):
        if self.hitbox.colliderect(enemy.rect):
            if self.invicible_time == 0:
                if not enemy.is_shot:
                    self.die()
            else:
                return enemy.shot()
        return 0

    def becomeInvincible(self):
        self.invicible_time = 60 * 10
        self.i_frame = 30

    def collectCollectible(self, collectible: pygame.sprite.Sprite):
        self.score += collectible.playerCollect() * self.current_multiplier

    def handleAllCollisions(self, colliables: list[pygame.sprite.Sprite], platforms: list[pygame.sprite.Sprite]):
        self.handlePlatformCollision(platforms)
        for colliable in colliables:
            if self.hitbox.colliderect(colliable.rect):
                if colliable.type == "obstacle":
                    self.die()

                elif colliable.type == "coin":
                    self.collectCollectible(colliable)

                elif colliable.type == "potion":
                    self.becomeInvincible()
                    self.collectCollectible(colliable)
                    self.invincible_cd = self.invicible_time + TARGET_FRAMERATE * 15

                elif colliable.type == "orb":
                    self.collectCollectible(colliable)
                    self.shockwave = colliable.shockwave
                    self.shock_wave_cd = TARGET_FRAMERATE * 20

                elif colliable.type == "emerald":
                    self.collectCollectible(colliable)
                    self.multiplier_time = colliable.effect_time * TARGET_FRAMERATE
                    self.current_multiplier = colliable.multiplier
                    self.multiplier_cd = self.multiplier_time + TARGET_FRAMERATE * 15

    def getHitbox(self):
        if not self.is_dead:
            if not self.image in PlayerImg.jump_anim[1:]:
                self.hitbox = pygame.Rect(0, 0, 12 * 4, 22 * 4)
                self.hitbox.bottomleft = (self.rect.left + 6 * 4, self.rect.bottom)
            else:
                self.hitbox = pygame.Rect(0, 0, 17 * 4, 17 * 4)
                self.hitbox.bottomleft = (self.rect.left, self.rect.bottom)
        else:
            self.hitbox = pygame.Rect(0, 0, 12 * 4, 22 * 4)
            self.hitbox.bottomleft = (self.previous_pos.left + 6 * 4, self.previous_pos.bottom)

    #TODO: kill the player, thus ending the game
    def die(self):
        self.is_dead = True
        sfx.player_die.play()

    def countdown(self, dt):
        elapsed_time = 1 * dt * TARGET_FRAMERATE

        self.shock_wave_cd -= elapsed_time
        self.multiplier_cd -= elapsed_time
        self.invincible_cd -= elapsed_time

        if self.shock_wave_cd <= 0:
            self.shock_wave_cd = 0

        if self.multiplier_cd <= 0:
            self.multiplier_cd = 0

        if self.invincible_cd <= 0:
            self.invincible_cd = 0

        self.invicible_time -= elapsed_time
        if self.invicible_time <= 0:
            self.invicible_time = 0

        self.multiplier_time -= elapsed_time
        if self.multiplier_time <= 0:
            self.multiplier_time = 0
            self.current_multiplier = 1
        #print(int(self.i_frame/60))

    def flash(self, dt):
        self.i_frame -= 1 * dt * TARGET_FRAMERATE
        if self.i_frame <= 0:
            self.i_frame = 0
        if int(self.i_frame) % 2 == 0:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
        # print(int(self.i_frame))

    #TODO: update the state of the player
    def update(self, dt):
        self.previous_pos = self.rect.copy()
        self.getPlayerInput()
        self.affectGravityOnPlayer(dt)
        self.animatePlayer(dt)
        self.getHitbox()
        self.countdown(dt)
        self.flash(dt)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, Player_right, Player_centery):
        super().__init__()

        self.Player_right, self.Player_centery = Player_right, Player_centery
        self.speed = 15
        self.image = BulletImg.bullet

        self.rect = self.image.get_rect(midleft = (self.Player_right - 30, self.Player_centery))

        sfx.player_shoot.play()

    def moveBullet(self, dt):
        self.rect.x += self.speed * dt * TARGET_FRAMERATE
        if self.rect.left > SCREEN_WIDTH + 5 or self.rect.top < -5 or self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()

    def update(self, dt):
        self.moveBullet(dt)

    def handlePlatformCollision(self, platform_group: list[pygame.sprite.Sprite]):
        for platform in platform_group:
            if self.rect.colliderect(platform.rect):
                self.kill()
                break

    def handleEnemyCollision(self, enemy_group: list[pygame.sprite.Sprite]):
        for enemy in enemy_group:
            if self.rect.colliderect(enemy.rect) and not enemy.is_shot:
                self.kill()
                return enemy.shot()
        return 0
