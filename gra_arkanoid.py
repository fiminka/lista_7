import pygame

# Some colours we use in the game
turquoise = (64, 224, 208)
orange = (255, 165, 0)
pink = (255, 105, 180)
orchid = (218, 112, 214)
black = (0, 0, 0)

class Brick:
    def __init__(self, x_loc, y_loc, weight=40, height=15, color=turquoise):
        self.x = x_loc
        self.y = y_loc
        self.w = weight
        self.h = height
        self.col = color
        self.rect = pygame.Rect(self.x, self.y, self.h, self.w)


class Bar:
    def __init__(self, x_loc, y_loc, weight=40, height=15, color=orchid):
        self.x = x_loc
        self.y = y_loc
        self.w = weight
        self.h = height
        self.col = color
        self.rect = pygame.Rect(self.x, self.y, self.h, self.w)


class Ball:
    def __init__(self, x_loc, y_loc, size=7):
        self.x = x_loc
        self.y = y_loc
        self.size = size
