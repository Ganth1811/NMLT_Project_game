import pygame
from random import choice
from math import sin, cos, pi

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

    #TODO: update the state of the platform
    def update(self, speed, dt):
        self.previous_pos = self.rect.copy()
        self.movePlatform(speed, dt)

    def generatePlatform(prev_platform_pos: pygame.Rect, platform_gap: int, platform_speed: float):
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
        self.anim_frame = 0

        #* import player enemy


        self.run_anim = choice([EnemyImg.enemy1_run, EnemyImg.enemy2_run])
        self.death_anim = EnemyImg.death_anim

        self.anim_list = self.run_anim
        self.len_anim_list = len(self.anim_list)

        self.x_pos = platform_x
        self.y_pos = platform_y
        self.image = self.anim_list[self.anim_frame]
        self.rect = self.image.get_rect(bottomright = (self.x_pos, self.y_pos))

        self.is_shot = False
        #self.speed = Platform_speed * 1.2
        #self.platform_topright = Platform_topright

        self.given_score = 20

    def animateEnemy(self, dt):
        self.len_anim_list = len(self.anim_list)
        self.anim_frame += 0.2 * dt * TARGET_FRAMERATE

        if (self.anim_frame >= self.len_anim_list):
            if self.is_shot:
                self.kill()
            self.anim_frame = 0

        self.image = self.anim_list[int(self.anim_frame)]

    def moveEnemy(self, speed, dt):
        self.rect.x -= (speed + 0.1) * dt * TARGET_FRAMERATE
        if self.rect.right < 0:
            self.kill()

    def shot(self):
        self.is_shot = True
        self.anim_frame = 0
        self.anim_list = self.death_anim
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


class Coin(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.anim_list = CollectibleImg.coin_anim
        self.image = self.anim_list[self.anim_frame]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.type = "coin"
        self.given_score = 5
        self.sound = sfx.player_collect_coin

    def spawnCoinCurve(player, speed: int, center: tuple, replace = False,  number = 9):
        gravity = -player.gravity
        jump_force = player.jump_force
        coin_list = []
        mid = int(number / 2)

        #* v_peak = v0 + gt <=> t = (v_peak - v0)/g, v_peak = 0, v0 = jump_force
        time_max_height = -jump_force / gravity
        #* peak_y = h_max = h0 + v0t + 1/2*gt^2, h0 = 0, v0 = jump_force, t = time_max_height
        peak_y = jump_force * time_max_height + 1/2 * gravity * time_max_height**2
        peak_x = time_max_height * speed
        step_angle = pi / (number - 1)

        for i in range(number):
            angle = step_angle * i
            pos_x = peak_x * cos(angle) + center[0]
            pos_y = -(peak_y * sin(angle)) + center[1]
            if i == mid:
                if not replace:
                    coin_list.append(Coin(pos_x, pos_y))
            else:
                coin_list.append(Coin(pos_x, pos_y))

        return coin_list

    def spawnCoin(platform: pygame.Rect, type: str):
        coin_list = []

        if type == "long":
            num = 10
        elif type == "short":
            num = 5

        step = platform.width / num
        for i in range(1, num):
            coin_list.append(Coin(platform.left + step * i, platform.top - 20))

        return coin_list

class InvinciblePotion(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.type = "potion"
        self.anim_list = CollectibleImg.invincibility_anim
        self.given_score = 0
        self.image = self.anim_list[self.anim_frame]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.sound = sfx.player_collect_cherry

class MagicOrb(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.type = "orb"
        self.anim_list = CollectibleImg.rainbow_orb_anim
        self.given_score = 0
        self.image = self.anim_list[self.anim_frame]
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

class Emerald(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.anim_frame = 0
        self.anim_list = CollectibleImg.multiplier_anim
        self.image = self.anim_list[self.anim_frame]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.type = "emerald"
        self.given_score = 0
        self.sound = sfx.player_collect_cherry
        self.multiplier = 2
        self.effect_time = 10


#* a very simple obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, obstacle_type):
        super().__init__()
        self.obstacle_type = obstacle_type
        self.type = "obstacle"
        self.anim_frame = 0

        if self.obstacle_type == "high":
            self.anim_list = ObstacleImg.suriken_anim
            self.image = self.image = self.anim_list[self.anim_frame]
            self.len_anim_list = len(self.anim_list)

        elif self.obstacle_type == "low":
            self.image = ObstacleImg.spike

        self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))
        self.rect.width -= 8
        self.rect.height -= 8

    def moveObstacle(self, platform_speed, dt):
        self.rect.x -= platform_speed * dt * TARGET_FRAMERATE
        if self.rect.right <= -1:
            self.kill()

    def animateCollectible(self, dt):
        if self.obstacle_type == "high":
            self.anim_frame += 0.5 * dt * TARGET_FRAMERATE

            if (self.anim_frame >= len(self.anim_list)):
                self.anim_frame = 0

            self.image = self.anim_list[int(self.anim_frame)]

    def update(self, platform_speed, dt):
        self.moveObstacle(platform_speed, dt)
        self.animateCollectible(dt)

