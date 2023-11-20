import pygame
from random import randint, choice
from math import sin, cos, pi
import sfx

pygame.init()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__()
        self.type = "platform"
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height

        init_image = pygame.transform.scale_by(pygame.image.load("img\\Bg\\platform.png").convert_alpha(), height / 16)

        self.image = init_image.subsurface(0, 0, self.width, self.height)
        self.rect = self.image.get_rect(topleft =  (self.x_pos, self.y_pos))

        self.previous_pos = self.rect.copy()

    #TODO: move the platform leftward by a given speed
    def movePlatform(self, speed):
        self.rect.x -= speed
        if self.rect.right <= -5:
            self.kill()
            del self
    #TODO: update the state of the platform
    def update(self, speed):
        self.previous_pos = self.rect.copy()
        self.movePlatform(speed)

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
    if prev_platform_pos.top <= 200:
        prev_platform_pos.y += 200

    #* separate two platforms by a certain distance relative to their speed
    platform_x = prev_platform_pos.right + platform_gap * (platform_speed / 7.0)

    #* manipulate the platform y value according to the previous platform position
    if prev_platform_pos.bottom >= 500:
        platform_y = choice([prev_platform_pos.top - 50 - 25, prev_platform_pos.y - 25, prev_platform_pos.top])
        
    else:
        platform_y = choice([prev_platform_pos.top - 50, prev_platform_pos.bottom + 100, prev_platform_pos.bottom + 100, prev_platform_pos.bottom + 100, prev_platform_pos.top])

    #* get a random platform type and spawn it
    platform_type = choice(["long"] * 3 + ["short"] * 1)

    if platform_type == "long":
        platform_width = platform_speed * 70
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
        self.enemy_run_anim = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\Enemy\\enemyRun{i}.png").convert_alpha() for i in range(1,7)]
        self.enemy_run_anim = [pygame.transform.rotozoom(image, 0, 2) for image in self.enemy_run_anim]

        self.enemy_death_anim = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\enemy-death\\enemy-death-{i}.png").convert_alpha() for i in range(1,7)]
        self.enemy_death_anim = [pygame.transform.rotozoom(image, 0, 2) for image in self.enemy_death_anim]

        self.enemy_anim_list = self.enemy_run_anim

        self.x_pos = platform_x
        self.y_pos = platform_y
        self.image = self.enemy_anim_list[self.enemy_anim_frame]
        self.rect = self.image.get_rect(bottomright = (self.x_pos, self.y_pos))

        self.is_shot = False
        #self.speed = Platform_speed * 1.2
        #self.platform_topright = Platform_topright

        self.given_score = 20

    def animateEnemy(self):
        self.enemy_anim_frame += 0.2

        if (self.enemy_anim_frame >= 6):
            if self.is_shot:
                self.kill()
            self.enemy_anim_frame = 0

        self.image = self.enemy_anim_list[int(self.enemy_anim_frame)]

    def moveEnemy(self, speed):
        self.rect.x -= speed + 0.1
        if self.rect.right < 0:
            self.kill()

    def shot(self):
        self.is_shot = True
        self.enemy_anim_frame = 0
        self.enemy_anim_list = self.enemy_death_anim
        return self.given_score

    def update(self, speed):
        self.animateEnemy()
        self.moveEnemy(speed)


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

    def animateCollectible(self):
        self.anim_frame += 0.2

        if (self.anim_frame >= len(self.anim_list)):
            self.anim_frame = 0

        self.image = self.anim_list[int(self.anim_frame)]

    def moveCollectible(self, speed):
        self.rect.x -= speed

    def update(self, speed):
        self.moveCollectible(speed)
        self.animateCollectible()
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

        self.anim_list = [pygame.image.load(f"Sunny-land-files\\Graphical Assets\\sprites\\gem\\gem-{i}.png").convert_alpha() for i in range(1,6)]
        self.anim_list = [pygame.transform.scale_by(image, 2) for image in self.anim_list]

        self.image = self.anim_list[self.anim_frame]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.type = "diamond"
        self.given_score = 5
        self.sound = sfx.player_collect_diamond

class InvicibleCherry(Collectible):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.type = "cherry"
        self.anim_list = [pygame.image.load(f"img\\collectibles\\cherry-{i}.png").convert_alpha() for i in range(1,8)]
        self.anim_list = [pygame.transform.scale_by(image, 3) for image in self.anim_list]
        self.given_score = 0
        self.image = self.anim_list[self.anim_frame]
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.sound = sfx.player_collect_cherry

#* a very simple obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image):
        super().__init__()
        self.type = "obstacle"
        self.image = pygame.transform.scale_by(pygame.image.load(image), 2).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))
        self.rect.width -= 4
        self.rect.height -= 4

    def moveObstacle(self, platform_speed):
        self.rect.x -= platform_speed

    def destroy(self):
        if self.rect.right <= -1:
            self.kill
            del self

    def update(self, platform_speed):
        self.moveObstacle(platform_speed)
        self.destroy()


    def createDiamondPath(self, player, speed, number = 9):
        gravity = -player.gravity
        jump_force = player.jump_force
        diamond_list = []

        # v_peak = v0 + gt <=> t = (v_peak - v0)/g, v_peak = 0, v0 = jump_force
        time_max_height = -jump_force / gravity
        # peak_y = h_max = h0 + v0t + 1/2*gt^2, h0 = 0, v0 = jump_force, t = time_max_height
        peak_y = jump_force * time_max_height + 1/2 * gravity * time_max_height**2
        peak_x = time_max_height * speed
        step_angle = pi / (number - 1)

        for i in range(number):
            angle = step_angle * i
            pos_x = peak_x * cos(angle) + self.rect.centerx
            pos_y = -(peak_y * sin(angle)) + self.rect.centery
            diamond_list.append(Diamond(pos_x, pos_y))

        return diamond_list
    
        