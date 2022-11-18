#  Here are some of the tool functions that are likely to be called widely
import random
import time
import pygame

import const
import setup
from const import screen_width, screen_height


def board_judge(target):
    """
    :param target: should be sprite object
    :return: Whether or not there was a collision(boolean)
    """
    collision = True
    if target.rect.x < 0:
        target.rect.x = 0
    elif target.rect.x > screen_width - target.rect.width:
        target.rect.x = screen_width - target.rect.width
    elif target.rect.y < 0:
        target.rect.y = 0
        target.speed_y = 5
    else:
        collision = False
    return collision


def clean_bullet():
    """
    Clears bullets fired by players and enemies from the screen
    """
    for p_bul in setup.P_BulletGroup:
        p_bul.kill()
    for b_bul in setup.E_BulletGroup:
        b_bul.kill()


def interval_judge(obj, interval, center):
    """
    Enemy patrol area judgment
    """
    if obj.rect.x < (center['x'] - interval):
        obj.rect.x = center['x'] - interval
        return True
    if obj.rect.x > (center['x'] + interval):
        obj.rect.x = center['x'] + interval
        return True
    return False


def get_image(source, x, y, width, height, width_trans, height_trans):
    """
    Cut the desired portion from a larger picture
    """
    image = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a transparent Surface object
    init_image = pygame.image.load(source)
    image.blit(init_image, (0, 0), (x, y, width, height))
    image = pygame.transform.scale(image, (width_trans, height_trans))
    return image

