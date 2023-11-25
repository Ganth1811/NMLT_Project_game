import pygame
from random import choice
from math import sin, cos, pi, sqrt
from settings import SCREEN_DIAGONAL, SCREEN_WIDTH, TARGET_FRAMERATE
import sfx
from image import PlatformImg, EnemyImg, CollectibleImg, ObstacleImg

pygame.init()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.type = "platform"
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

        init_image = pygame.transform.scale_by(PlatformImg.platform, height / 16)

        self.image = init_image.subsurface(0, 0, self.width, self.height)
        self.rect = self.image.get_rect(topleft =  (self.x_pos, self.y_pos))

        self.previous_pos = self.rect.copy()

    #TODO: move the platform leftward by a given speed
    def movePlatform(self, speed, dt):
        self.rect.x -= speed * dt * TARGET_FRAMERATE
        if self.rect.right <= -5:
            self.kill()
            del self
    #TODO: update the state of the platform
    def update(self, speed, dt):
        self.previous_pos = self.rect.copy()
        self.movePlatform(speed, dt)

    def createDiamondPath(self, platform_type):
        diamond_list = []

        if platform_type == "long":
            num = 10
        elif platform_type == "short":
            num = 5

        step = self.width / num
        for i in range(1, num):
            diamond_list.append(Diamond(self.rect.left + step * i, self.rect.top - 20))

        return diamond_list


def generatePlatform(prev_platform_pos: pygame.Rect, platform_gap, platform_speed):
    #* separate two platforms by a certain distance relative to their speed
    platform_x = prev_platform_pos.right + platform_gap * (platform_speed / 7.0)

    #* manipulate the platform y value according to the previous platform position
    if prev_platform_pos.bottom >= 500:
        platform_y = choice([prev_platform_pos.top - 25] * 2 + [prev_platform_pos.top])
    
    elif prev_platform_pos.top <= 200:
        platform_y = choice([prev_platform_pos.top + 75] * 2 + [prev_platform_pos.top])
    
    else:
        platform_y = choice([prev_platform_pos.top - 50] + [prev_platform_pos.bottom + 100] * 3 +  [prev_platform_pos.top] * 2)

    #* get a random platform type and spawn it
    platform_type = choice(["long"] * 3 + ["short"] * 1)

    if platform_type == "long":
        platform_width = platform_speed * 80
    else:
        platform_width = platform_speed * 30

    return {
        "platform": Platform(platform_x, platform_y, platform_width, 64),
        "platform_type": platform_type,
        "platform_width": platform_width
    }

class Enemy(pygame.sprite.Sprite):
    def __init__(self, platform_x, platform_y):
        super().__init__()
        self.type = "enemy"
        #* initializing enemy spirte animations
        self.enemy_anim_frame = 0

        #* import player enemy and scale it
        self.enemy_run_anim = [pygame.transform.scale_by(image, 2) for image in EnemyImg.run_anim]
        self.enemy_death_anim = [pygame.transform.scale_by(image, 2) for image in EnemyImg.death_anim]

        self.enemy_anim_list = self.enemy_run_anim

        self.x_pos = platform_x
        self.y_pos = platform_y
        self.image = self.enemy_anim_list[self.enemy_anim_frame]
        self.rect = self.image.get_rect(bottomright = (self.x_pos, self.y_pos))

        self.is_shot = False
        #self.speed = Platform_speed * 1.2
        #self.platform_topright = Platform_topright

        self.given_score = 20

    def animateEnemy(self, dt):
        self.enemy_anim_frame += 0.2 * dt * TARGET_FRAMERATE

        if (self.enemy_anim_frame >= 6):
            if self.is_shot:
                self.kill()
            self.enemy_anim_frame = 0

        self.image = self.enemy_anim_list[int(self.enemy_anim_frame)]

    def moveEnemy(self, speed, dt):
        self.rect.x -= (speed + 0.1) * dt * TARGET_FRAMERATE
        if self.rect.right < 0:
            self.kill()

    def shot(self):
        self.is_shot = True
        self.enemy_anim_frame = 0
        self.enemy_anim_list = self.enemy_death_anim
        return self.given_score

    def update(self, speed, dt):
        self.animateEnemy(dt)
        self.moveEnemy(speed, dt)


class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y,):
        super().__init__()

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.anim_frame = 0
        self.anim_list: list
        self.image: pygame.Surface
        self.rect: pygame.Rect
        self.type: str
        self.given_score: int
        self.sound: pygame.mixer.Sound

    def animateCollectible(self, dt):
        self.anim_frame += 0.2 * dt * TARGET_FRAMERATE

        if (self.anim_frame >= len(self.anim_list)):
            self.anim_frame = 0

        self.image = self.anim_list[int(self.anim_frame)]

    def moveCollectible(self, speed, dt):
        self.rect.x -= speed * dt * TARGET_FRAMERATE

    def update(self, speed, dt):
        self.moveCollectible(speed, dt)
        self.animateCollectible(dt)
        self.destroy()

    def playerCollect(self):
        self.sound.play()
        self.kill()
        return self.given_score

    def destroy(self):
        if self.rect.right < 0:
            self.kill()


class Diamond(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.anim_list = [pygame.transform.scale_by(image, 2) for image in CollectibleImg.diamond_anim]
        self.image = self.anim_list[self.anim_frame]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.type = "diamond"
        self.given_score = 5
        self.sound = sfx.player_collect_diamond

class InvicibleCherry(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.type = "cherry"
        self.anim_list = [pygame.transform.scale_by(image, 3) for image in CollectibleImg.cherry_anim]
        self.given_score = 0
        self.image = self.anim_list[self.anim_frame]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.sound = sfx.player_collect_cherry

class RemoveHostile(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.type = "removehostile"
        self.anim_list = [pygame.Surface((20, 20))]
        self.given_score = 0
        self.image = self.anim_list[self.anim_frame]
        self.image.fill('red')
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.sound = sfx.player_collect_cherry
        self.shockwave = None
    
    def playerCollect(self):
        self.sound.play()
        self.shockwave = Shockwave(self.rect.centerx, self.rect.centery)
        self.kill()
        return self.given_score

class Shockwave():
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = 5
        self.width = 10
        self.over = False
    
    def drawShockwave(self, screen, dt):
        pygame.draw.circle(screen, 'darkgray', (self.pos_x, self.pos_y), self.radius, self.width)
        self.radius += 25 * dt * TARGET_FRAMERATE
        self.over = self.radius > SCREEN_DIAGONAL
    
    def clearHostile(self, hostiles):
        for hostile in hostiles:
            distance = ((hostile.rect.x - self.pos_x)**2 + (hostile.rect.y - self.pos_y)**2) ** (1/2)
            if distance <= self.radius and hostile.rect.left < SCREEN_WIDTH:
                hostile.kill()

class Multiplier(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.anim_frame = 0
        self.anim_list = [pygame.Surface((20, 20))]
        self.image = self.anim_list[self.anim_frame]
        self.image.fill('darkgreen')
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.type = "multipler"
        self.given_score = 0
        self.sound = sfx.player_collect_cherry
        self.multipler = 2
        self.effect_time = 10


#* a very simple obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image):
        super().__init__()
        self.type = "obstacle"
        self.image = pygame.transform.scale_by(pygame.image.load(image), 2).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))
        self.rect.width -= 4
        self.rect.height -= 4

    def moveObstacle(self, platform_speed, dt):
        self.rect.x -= platform_speed * dt * TARGET_FRAMERATE

    def destroy(self):
        if self.rect.right <= -1:
            self.kill
            del self

    def update(self, platform_speed, dt):
        self.moveObstacle(platform_speed, dt)
        self.destroy()


    def createDiamondPath(self, player, speed, number = 9):
        gravity = -player.gravity
        jump_force = player.jump_force
        diamond_list = []

        #* v_peak = v0 + gt <=> t = (v_peak - v0)/g, v_peak = 0, v0 = jump_force
        time_max_height = -jump_force / gravity
        #* peak_y = h_max = h0 + v0t + 1/2*gt^2, h0 = 0, v0 = jump_force, t = time_max_height
        peak_y = jump_force * time_max_height + 1/2 * gravity * time_max_height**2
        peak_x = time_max_height * speed
        step_angle = pi / (number - 1)

        for i in range(number):
            angle = step_angle * i
            pos_x = peak_x * cos(angle) + self.rect.centerx
            pos_y = -(peak_y * sin(angle)) + self.rect.centery
            diamond_list.append(Diamond(pos_x, pos_y))

        return diamond_list
    
        