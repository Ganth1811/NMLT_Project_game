from os import path

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_DIAGONAL = (SCREEN_WIDTH**2 + SCREEN_HEIGHT**2) ** (1/2)
TARGET_FRAMERATE = 60

INIT_SPEED = 10
MAX_SPEED = 23

class Score:
    high_score_list = []
    with open("high_score.txt", 'r') as f:
        high_score_list = [(int(data[0]), data[1].strip()) for data in [line.split(", ") for line in f.readlines()]]

        high_score_list = sorted(high_score_list, key=lambda x: x[0], reverse=True)