from datetime import datetime

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_DIAGONAL = (SCREEN_WIDTH**2 + SCREEN_HEIGHT**2) ** (1/2)
TARGET_FRAMERATE = 60

INIT_SPEED = 10
MAX_SPEED = 23

is_muted = False

class Score:
    high_score_list = []
    with open("high_score.txt", 'r') as f:
        for i in range(5):
            line = f.readline().split(", ")
            high_score_list.append((int(line[0]), line[1].strip()))

        high_score_list = sorted(high_score_list, key = lambda x: x[0], reverse = True)

    def updateHighScore(score: int):
        is_new_high_score = False
        if Score.high_score_list[4][0] < score:
            for i in range(5):
                if Score.high_score_list[i][0] < score:
                    Score.high_score_list.insert(i, (score, datetime.now().strftime("%d/%m/%Y %H:%M")))
                    if i == 0:
                        is_new_high_score = True
                    break

            Score.high_score_list.pop(-1)

            with open("high_score.txt", 'w') as f:
                f.writelines([f"{score}, {date}\n" for score, date in Score.high_score_list])

        return is_new_high_score