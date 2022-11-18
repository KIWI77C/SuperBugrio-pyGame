import pygame
import const


class Item(pygame.sprite.Sprite):
    """
    Super Class Item, extend from pygame.sprite.Sprite

    :param item_set: use to initialize the size of the item
    :param group: use to set the item belonging group
    :param player_group: use to interact with the player
    """

    def __init__(self, item_set, group, player_group):
        self.group = group
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(item_set['image_path'])
        self.init_set = item_set
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.width = item_set['width']
        self.height = item_set['height']
        self.rect.x = item_set['x']
        self.rect.y = item_set['y']
        self.act_obj = player_group
        self.score = 0

    # reset method
    def reset(self, item_set):
        self.image = pygame.image.load(item_set['image_path'])
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.width = item_set['width']
        self.height = item_set['height']
        self.rect.x = item_set['x']
        self.rect.y = item_set['y']
        self.group.add(self)


class Door(Item):
    """
    Sub Class Door, extend from item, use to draw the portal door

    :param item_set: use to initialize the size of the item
    :param group: use to set the item belonging group
    :param player_group: use to interact with the player
    """

    def __init__(self, item_set, group, player_group):
        Item.__init__(self, item_set, group, player_group)
        self.image = pygame.image.load(item_set['image_path'])
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.width = item_set['width']
        self.height = item_set['height']
        self.rect.x = item_set['x']
        self.rect.y = item_set['y']
        self.group.add(self)
        self.act_obj = player_group
        # self.enemy = monster_group

    # jump function use to allow the player enter to the next state
    def jump(self):
        status = pygame.sprite.spritecollideany(self, self.act_obj)
        if status:
            const.music_sep.play()
            self.kill()
            return 1

    # provide update method to the MainPart.game class for the update method
    def update(self):
        self.jump()


class BloodVessel(Item):
    """
    Sub Class BloodVessel, extend from item, use to add player's HP

    :param item_set: use to initialize the size of the item
    :param group: use to set the item belonging group
    :param player_group: use to interact with the player
    :param slime: add blood on player
    """

    def __init__(self, item_set, group, player_group, slime):
        Item.__init__(self, item_set, group, player_group)
        self.image = pygame.image.load(item_set['image_path'])
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.width = item_set['width']
        self.height = item_set['height']
        self.rect.x = item_set['x']
        self.rect.y = item_set['y']
        self.group.add(self)
        self.player = slime
        self.act_obj = player_group

    # HP adding function
    def add_blood(self):
        status = pygame.sprite.spritecollideany(self, self.act_obj)
        if status:
            self.player.HP += 10
            const.music_sep.play()
            self.kill()

    # provide update method to the MainPart.game class for the update method
    def update(self):
        self.add_blood()


class Scroll(Item):
    """
    Sub Class Scroll, extend from item, use to draw the scroll to switch on the blink ability and add 300 HP

    :param item_set: use to initialize the size of the item
    :param group: use to set the item belonging group
    :param player_group: use to interact with the player
    """

    def __init__(self, item_set, group, player_group, slime):
        Item.__init__(self, item_set, group, player_group)
        self.image = pygame.image.load(item_set['image_path'])
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.width = item_set['width']
        self.height = item_set['height']
        self.rect.x = item_set['x']
        self.rect.y = item_set['y']
        self.group.add(self)
        self.player = slime
        self.act_obj = player_group

    # blink use to switch on the player blink ability
    def blink_skill(self):
        status = pygame.sprite.spritecollideany(self, self.act_obj)
        if status:
            self.player.bink = True
            self.player.HP += 300
            const.music_sep.play()
            self.kill()

    # provide update method to the MainPart.game class for the update method
    def update(self):
        self.blink_skill()
