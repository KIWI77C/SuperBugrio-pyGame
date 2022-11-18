import pygame
import const


class Info:
    def __init__(self, init_position, content, font='small fonts', size=18):

        self.font = pygame.font.SysFont(font, size, 1)
        self.init_position = init_position
        self.content = content
        self.image = self.font.render(self.content, 1, pygame.Color('white'))

    def update(self, screen):
        screen.blit(self.image, self.init_position)
