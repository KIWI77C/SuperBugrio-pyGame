import pygame


class Environment(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, group):
        super().__init__()
        self.group = group
        self.rect = pygame.Rect(x, y, width, height)
        self.group.add(self)
