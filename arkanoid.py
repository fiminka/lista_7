import pygame
from pygame import gfxdraw
import os
from random import randint

# some colors we ude in the code
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TURQUOISE = (64, 224, 208)
PINK = (255, 105, 180)
ORCHID = (218, 112, 214)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

velocity = 2


class Brick:
    """This class creates one brick"""

    def __init__(self, x, y, w=50, h=20, color=TURQUOISE):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        pygame.draw.rect(window, self.color, self.rect)


class Bar:
    """This class creates a bar"""

    def __init__(self, x_loc, y_loc, w=65, h=10):
        self.x = x_loc
        self.y = y_loc
        self.w = w
        self.h = h

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(window, RED, self.rect)


class Ball:
    """This class creates a ball."""
    def __init__(self, x_loc, y_loc, size=14):
        self.x = x_loc
        self.y = y_loc
        self.color = WHITE
        self.counter = pygame.time.get_ticks()
        self.size = size

    def update(self):
        """Moving of the ball."""
        global ball, velocity
        global turn_ball, dir_ball, game

        if pygame.time.get_ticks() - self.counter > velocity:
            self.counter = pygame.time.get_ticks()
            if turn_ball == "left":
                ball.x -= 1
                if ball.x < 10:
                    turn_ball = "right"
            if dir_ball == 'down':
                ball.y += 1
            if dir_ball == 'up':
                ball.y -= 1
                if ball.y < 50:
                    dir_ball = 'down'
            if turn_ball == "right":
                ball.x += 1
                if ball.x > 590:
                    turn_ball = "left"

        gfxdraw.filled_circle(window, ball.x, ball.y, self.size // 2, self.color)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


def collision():
    """ function checks all the collisions found between different classes"""
    global ball, bar, dir_ball, turn_ball, vely, mouse_dir, bricks
    global diff, lives, level, score, running, game

    # ball and brick collision
    for i, brick in enumerate(bricks):
        if ball.rect.colliderect(brick):
            pygame.draw.rect(window, BLACK, brick.rect)
            window.blit(update_score_board(color="Black"), (12, 10))
            pygame.mixer.Sound.play(hitbrick)
            score += 10
            window.blit(update_score_board(), (12, 10))
            if dir_ball == "up":
                if ball.y == (brick.y + brick.h - 1):
                    dir_ball = "down"
                else:
                    if turn_ball == "left":
                        turn_ball = "right"
                    else:
                        turn_ball = "left"
            elif dir_ball == "down":
                if ball.y <= brick.y - 1:
                    dir_ball = "up"
                else:
                    if turn_ball == "left":
                        turn_ball = "right"
                    else:
                        turn_ball = "left"
            bricks.pop(i)
            if len(bricks) == 0:
                pygame.mixer.Sound.play(win)
                new_highest_score()
                window.fill(BLACK)
                write("YOU WIN!", 150, 200, color=GREEN)
                write("choose another game or come back to main menu by pressing m")
                ball.y = 300
                ball.x = 100
                if game == 1:
                    bricks = create_bricks_classic()
                if game == 2:
                    bricks = create_bricks2()
                if game == 3:
                    bricks = create_bricks3()
                if game == 4:
                    bricks = create_bricks4()
                if game == 5:
                    bricks = create_bricks5()
                show_bricks()
    # ball outside the window
    if ball.y > 610:
        ball.x = 500
        ball.y = 300
        lives -= 1
        if lives < 0:
            new_highest_score()
            score = 0
            level = 0
            dir_ball = 'down'
            turn_ball = 'left'
            back_to_menu()

    # ball and bar collision - bounce
    if ball.rect.colliderect(bar):
        pygame.mixer.Sound.play(hitbar)
        dir_ball = "up"
        if mouse_dir == "left" and turn_ball == "right":
            turn_ball = "left"
        if mouse_dir == "right" and turn_ball == "left":
            turn_ball = "right"


def create_bricks_classic():
    """The bricks pattern for classic game"""
    bricks = []
    for i in range(9):
        brick = Brick(10 + i * 65, 50)
        bricks.append(brick)
    for i in range(9):
        brick = Brick(10 + i * 65, 80, color=ORCHID)
        bricks.append(brick)
    for i in range(9):
        brick = Brick(10 + i * 65, 110)
        bricks.append(brick)
    for i in range(9):
        brick = Brick(10 + i * 65, 140, color=ORCHID)
        bricks.append(brick)
    return bricks


def create_bricks2():
    """The bricks pattern for ANKInoid game"""
    line1 = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1]
    line2 = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1]
    line3 = [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0]
    line4 = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0]
    line5 = [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    bricks = []
    for i, number in enumerate(line1):
        if number == 1:
            bricks.append(Brick(10 + i*25, 40, w=20, h=45, color=ORCHID))
        i += 1
    for i, number in enumerate(line2):
        if number == 1:
            bricks.append(Brick(10 + i*25, 80, w=20, h=45))
        i += 1
    for i, number in enumerate(line3):
        if number == 1:
            bricks.append(Brick(10 + i*25, 125, w=20, h=45, color=ORCHID))
        i += 1
    for i, number in enumerate(line4):
        if number == 1:
            bricks.append(Brick(10 + i*25, 165, w=20, h=45))
        i += 1
    for i, number in enumerate(line5):
        if number == 1:
            bricks.append(Brick(10 + i*25, 210, w=20, h=45, color=ORCHID))
        i += 1
    return bricks


def create_bricks3():
    """The bricks pattern for WIKAnoid game"""
    line1 = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]
    line2 = [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0]
    line3 = [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0]
    line4 = [1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1]
    line5 = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1]
    bricks = []
    for i, number in enumerate(line1):
        if number == 1:
            bricks.append(Brick(10 + i * 35, 40, w=30, h=35))
        i += 1
    for i, number in enumerate(line2):
        if number == 1:
            bricks.append(Brick(10 + i * 35, 80, w=30, h=35))
        i += 1
    for i, number in enumerate(line3):
        if number == 1:
            bricks.append(Brick(10 + i * 35, 120, w=30, h=35))
        i += 1
    for i, number in enumerate(line4):
        if number == 1:
            bricks.append(Brick(10 + i * 35, 160, w=30, h=35))
        i += 1
    for i, number in enumerate(line5):
        if number == 1:
            bricks.append(Brick(10 + i * 35, 200, w=30, h=35))
        i += 1
    return bricks


def create_bricks4():
    """The bricks pattern for RANDOMoid game"""
    line1 = [randint(0, 1) for i in range(13)]
    line2 = [randint(0, 1) for i in range(13)]
    line3 = [randint(0, 1) for i in range(13)]
    line4 = [randint(0, 1) for i in range(13)]
    line5 = [randint(0, 1) for i in range(13)]
    bricks = []
    for i, number in enumerate(line1):
        if number == 1:
            bricks.append(Brick(10 + i * 45, 40, w=40, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line2):
        if number == 1:
            bricks.append(Brick(10 + i * 45, 80, w=40, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line3):
        if number == 1:
            bricks.append(Brick(10 + i * 45, 125, w=40, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line4):
        if number == 1:
            bricks.append(Brick(10 + i * 45, 165, w=40, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line5):
        if number == 1:
            bricks.append(Brick(10 + i * 45, 210, w=40, h=25, color=random_color()))
        i += 1
    return bricks


def create_bricks5():
    """The bricks pattern for TINYnoid game"""
    line1 = [randint(0, 1) for i in range(23)]
    line2 = [randint(0, 1) for i in range(23)]
    line3 = [randint(0, 1) for i in range(23)]
    line4 = [randint(0, 1) for i in range(23)]
    line5 = [randint(0, 1) for i in range(23)]
    line6 = [randint(0, 1) for i in range(23)]
    line7 = [randint(0, 1) for i in range(23)]
    bricks = []
    for i, number in enumerate(line1):
        if number == 1:
            bricks.append(Brick(10 + i * 25, 40, w=20, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line2):
        if number == 1:
            bricks.append(Brick(10 + i * 25, 80, w=20, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line3):
        if number == 1:
            bricks.append(Brick(10 + i * 25, 125, w=20, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line4):
        if number == 1:
            bricks.append(Brick(10 + i * 25, 165, w=20, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line5):
        if number == 1:
            bricks.append(Brick(10 + i * 25, 210, w=20, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line6):
        if number == 1:
            bricks.append(Brick(10 + i * 25, 210, w=20, h=25, color=random_color()))
        i += 1
    for i, number in enumerate(line7):
        if number == 1:
            bricks.append(Brick(10 + i * 25, 210, w=20, h=25, color=random_color()))
        i += 1
    return bricks


def random_color():
    """ function that chooses random color"""
    color = randint(1, 6)
    dict_col = {1: ORCHID, 2: PINK, 3: RED, 4: TURQUOISE, 5: WHITE, 6: GREEN}
    return dict_col[color]


def update_score_board(color=WHITE):
    global score, highest_score
    scr_brd_txt = f"Score: {score} Highest score: {highest_score} Lives: {lives} "
    score_board = big_font.render(scr_brd_txt, True, color)
    return score_board


def write(text, x, y, color=WHITE, ):
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(600 // 2, y))
    window.blit(text, text_rect)
    return text


def write_big(text, x, y, color=WHITE, ):
    text = big_font.render(text, True, color)
    text_rect = text.get_rect(center=(600 // 2, y))
    window.blit(text, text_rect)
    return text


def write_small(text, x, y, color=WHITE, ):
    text = small_font.render(text, True, color)
    text_rect = text.get_rect(center=(600 // 2, y))
    window.blit(text, text_rect)
    return text


def score_text():
    global game, scorefile

    if game == 1:
        scorefile = "score1.txt"
    if game == 2:
        scorefile = "score2.txt"
    if game == 3:
        scorefile = "score3.txt"
    if game == 4:
        scorefile = "score4.txt"
    if game ==5:
        scorefile = "score5.txt"

    return scorefile


def get_score():
    global highest_score, game

    scorefile = score_text()
    if scorefile in os.listdir():
        with open(scorefile, "r") as file:
            if file.readlines() == []:
                with open(scorefile, "w") as filewrite:
                    filewrite.write("0")
                    highest_score = 0
            else:
                with open(scorefile, "r") as file:
                    highest_score = int(file.readlines()[0])
    else:
        with open(scorefile, "w") as file:
            file.write("0")


def new_highest_score():
    """function checks highest scores in different levels"""
    global score
    scorefile = score_text()
    with open(scorefile, "r") as file:
        highest_score = int(file.readlines()[0])
    if score > highest_score:
        with open(scorefile, "w") as file:
            file.write(str(score))


def restart():
    """function that restarts all the static amounts"""
    global score, lives, level
    level = 0
    score = 0
    lives = 3
    window.fill(BLACK)
    ball.x = 300
    ball.y = 300
    ball.update()
    bar.update()


def restart1():
    """function that restarts bricks pattern in level 1"""
    global bricks
    restart()
    bricks = create_bricks_classic()
    show_bricks()


def restart2():
    """function that restarts bricks pattern in level 2"""
    global bricks
    restart()
    bricks = create_bricks2()
    show_bricks()


def restart3():
    """function that restarts bricks pattern in level 3"""
    global bricks
    restart()
    bricks = create_bricks3()
    show_bricks()


def restart4():
    """function that restarts bricks pattern in level 4"""
    global bricks
    restart()
    bricks = create_bricks4()
    show_bricks()


def restart5():
    """function that restarts bricks pattern in level 5"""
    global bricks
    restart()
    ball.size = 6
    bar.w = 30
    bricks = create_bricks5()
    show_bricks()


def show_bricks():
    """function makes bricks appear"""
    for brick in bricks:
        brick.update()


def back_to_menu():
    """function that brings player back to main menu"""
    new_highest_score()
    window.fill(BLACK)
    main_menu()


def mainloop():
    """function that creates a game in different levels"""
    global startx, mouse_dir, diff, game
    show_bricks()
    get_score()
    write_small("press m to come back to main menu", 450, 590)
    running = True
    while running:
        pygame.draw.rect(window, BLACK, (bar.x, bar.y, bar.w, bar.h))
        gfxdraw.filled_circle(window, ball.x, ball.y, ball.size // 2, BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                new_highest_score()
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    new_highest_score()
                    running = False
                if event.key == pygame.K_m:
                    back_to_menu()
            if event.type == pygame.KEYUP:
                if event.type == pygame.K_ESCAPE:
                    running = False

        mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]

        if pygame.mouse.get_pos()[1] > 600:
            bar.y = mouse_y

        if 5 < mouse_x < 590 - bar.w:
            bar.x = mouse_x
        diff = startx - mouse_x
        mouse_dir = check_mouse_dir(diff)
        startx = mouse_x
        ball.update()

        bar.update()
        collision()
        pygame.display.update()
        clock.tick(360)
    pygame.quit()


def check_mouse_dir(diff):
    """function checks the change of the position of the mouse"""
    global mouse_dir
    if diff < 0:
        mouse_dir = "right"
    elif diff > 0:
        mouse_dir = "left"
    else:
        mouse_dir = "stay"
    return mouse_dir


def main_menu():
    """function creates the main menu"""
    global game

    window.fill(BLACK)
    write_big("ARKANOID", 200, 120, color=RED)
    write("PRESS: ", 200, 200)
    write("1 - Classic", 150, 240)
    write("2 - ANKInoid", 150, 260)
    write("3 - WIKAnoid", 150, 280)
    write("4 - RANDOMoid", 150, 300)
    write("5 - TINYnoid", 150, 320)
    write("r - Rules", 150, 380)
    write("m - About me", 150, 400)
    write_small("press esc to exit", 200, 450, color=ORCHID)
    running = True
    while running:
        pygame.mixer.Sound.play(intro)
        for event in pygame.event.get():
            pygame.mixer.Sound.stop(intro)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                pygame.mixer.Sound.stop(intro)
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    game = 1
                    restart1()
                elif event.key == pygame.K_2:
                    game = 2
                    restart2()
                elif event.key == pygame.K_3:
                    game = 3
                    restart3()
                elif event.key == pygame.K_4:
                    game = 4
                    restart4()
                elif event.key == pygame.K_5:
                    game = 5
                    restart5()
                elif event.key == pygame.K_m:
                    window.fill(BLACK)
                    write("Hey, my name is Wiki!", 200, 100)
                    write("I'm studying Applied Mathematics at WUST.", 200, 150)
                    write("I have a cat named Toffik", 200, 180)
                    write("I love travelling and sports", 200, 210)
                    write_small("press b to come back to menu", 200, 430, color=ORCHID)
                elif event.key == pygame.K_r:
                    window.fill(BLACK)
                    write("Rules!", 200, 100, color=RED)
                    write("This is a game base on an arcade game Arkanoid", 200, 130)
                    write("Use mouse to move the bar and hit the ball.", 200, 160)
                    write("Try to kill all bricks", 200, 190)
                    write("There are 5 different levels", 200, 220)
                    write_small("press b to come back to menu", 200, 430, color=ORCHID)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5:
                    window.fill(BLACK)
                    mainloop()
                elif event.key == pygame.K_b:
                    window.fill(BLACK)
                    main_menu()

        pygame.display.update()
    pygame.quit()


# contant amounts
level = 0
lives = 3

turn_ball = 'right'
dir_ball = 'down'


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 512)
pygame.mixer.set_num_channels(32)

hitbar = pygame.mixer.Sound('sound_effects_paddle_hit.wav')
hitbrick = pygame.mixer.Sound('sound_effects_brick.wav')
win = pygame.mixer.Sound('sound_effects_level_complete.wav')
intro = pygame.mixer.Sound('sounds_intro.wav')


window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("ARKANOID")

clock = pygame.time.Clock()

background = pygame.image.load("background.png").convert()
pygame.mouse.set_visible(False)
mouse_dir = "stay"
diff = 0
score = 0
highest_score = 0
startx = 0

bar = Bar(100, 550)
ball = Ball(100, 300)

# fonts used in the GUI
small_font = pygame.font.Font(None, 17)
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 36)

pygame.event.set_grab(True)

main_menu()
