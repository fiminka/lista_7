import pygame
from pygame.locals import *
import random

# Some colours we use in the game
turquoise = (64, 224, 208)
orange = (255, 165, 0)
pink = (255, 105, 180)
orchid = (218, 112, 214)
black = (0, 0, 0)
white = (250, 250, 250)

# Static amounts
lives = 3
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 420


class Brick(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, weight=40, height=15, color=turquoise):
        pygame.sprite.Sprite.__init__(self)
        self.brx = 0
        self.bry = 0
        self.brickW = weight
        self.brickH = height
        self.brickCol = color


class Bar(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, weight, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.barX = x_loc
        self.barY = y_loc
        self.barW = weight
        self.barH = height
        self.barCol = color
        self.image = pygame.Surface((self.barW, self.barH))
        self.image.fill(self.barCol)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, 0.9*SCREEN_HEIGHT)

    def update(self):
        self.rect.move_ip(self.barX, self.barY)

        if self.rect.left < 0
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= SCREEN_HEIGHT/4:
            self.rect.top = SCREEN_HEIGHT/4
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Ball(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc, color):
        pygame.sprite.Sprite.__init__(self)
        self.ballCol = color
        self.inMove = False
        self.image = pygame.Surface((10, 10))
        self.image.fill(self.ballCol)
        self.rect = self.image.get_rect()
        self.x = x_loc
        self.y = y_loc

    def update(self):
        if not self.inMove:


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x_loc, y_loc):
        pygame.sprite.Sprite.__init__(self)
        self.bomX = x_loc
        self.bomY = y_loc
        self.image = pygame.Surface((5, 5))
        self.image.fill(black)
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()
        else:
            self.rect.move_ip(0, 4)


def main_menu():
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Wikanoid")
    window.fill(turquoise)
    pygame.display.flip()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(black)
        pygame.draw.line(window, white, [0,30], [750, 30], 2)
        font = pygame.font.Font(None, 28)
        txt = font.render("Score: " + str(score), 1, white)
        window.blit(txt, (18, 15))
        txt = font.render("Best score: "+ str(best_score), 1, white)
        window.blit(txt, (700, 15))

        pygame.display.flip()

        clock.tick(120)


main_menu()
