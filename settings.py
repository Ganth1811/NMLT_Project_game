from os import path
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_DIAGONAL = (SCREEN_WIDTH**2 + SCREEN_HEIGHT**2) ** (1/2)
TARGET_FRAMERATE = 60

MAX_SPEED = 23

class score:
    high_score = 0

    if path.exists('high_score.txt'):
        with open('high_score.txt', 'r') as file:
            high_score = int(file.read())
        