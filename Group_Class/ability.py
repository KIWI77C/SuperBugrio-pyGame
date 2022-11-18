import pygame
import tools

pygame.init()

"""

Super Bullet Class

"""


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_set, owner, group, environ_group):
        super().__init__()
        self.init_set = bullet_set
        self.groups = group
        # Images
        self.groups.add(self)
        self.width = bullet_set['width']
        self.height = bullet_set['height']
        self.image = pygame.image.load(bullet_set['image_path'])
        self.image_right = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        # Rect and owner
        self.rect = self.image.get_rect()
        self.owner = owner
        # Speed
        self.speed = bullet_set['speed']
        # direction
        if self.owner.front == 'right':
            self.rect.midleft = self.owner.rect.midright
            self.image = self.image_right
        else:
            self.rect.midright = self.owner.rect.midleft
            self.image = self.image_left
            self.speed *= -1
        self.state_env = environ_group
        self.atk = bullet_set['atk']

    # collision with environment check
    def check_env_col(self):
        env_col = pygame.sprite.spritecollideany(self, self.state_env)
        if env_col:
            self.death()

    def death(self):
        self.kill()

    def update(self):
        pass


"""

class extend from Bullet, for player's bullet

"""


class PlayerBullet(Bullet):
    def __init__(self, bullet_set, owner, group, environ_group, ene_group):
        super().__init__(bullet_set, owner, group, environ_group)
        self.enemy_group = ene_group

    # collision with enemy check
    def check_ene_col(self):
        ene_col = pygame.sprite.spritecollideany(self, self.enemy_group)
        if ene_col:
            ene_col.hurt(self.atk)
            self.death()

    def update(self):
        self.rect.x += self.speed
        if tools.board_judge(self):
            self.kill()
        self.check_env_col()
        self.check_ene_col()


class EnemyBullet(Bullet):
    def __init__(self, bullet_set, owner, group, environ_group, player_group):
        super().__init__(bullet_set, owner, group, environ_group)
        self.player = player_group
        self.alive_time = pygame.time.get_ticks()

    def reset(self, bullet_set):
        self.width = self.init_set['width']
        self.height = bullet_set['height']
        self.image = pygame.image.load(bullet_set['image_path'])
        self.image_right = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.speed = bullet_set['speed']
        if self.owner.front == 'right':
            self.rect.midleft = self.owner.rect.midright
        else:
            self.image = self.image_left
            self.rect.midleft = self.owner.rect.midleft
            self.speed *= -1
        if not self.alive():
            self.groups.add(self)
        self.atk = self.init_set['atk']
        self.alive_time = pygame.time.get_ticks()

    # collision with player check
    def check_player_col(self):
        pl_col = pygame.sprite.spritecollideany(self, self.player)
        if pl_col:
            pl_col.hurt(self.atk)
            self.death()

    def update(self):
        self.rect.x += self.speed
        if not self.owner.alive():
            self.kill()
        elif tools.board_judge(self):
            self.kill()
        self.check_env_col()
        self.check_player_col()


"""

class extend from PlayerBullet, for player's attack
It is essentially a bullet with speed equal 0

"""


class PlayerAttack(PlayerBullet):
    def __init__(self, bullet_set, owner, group, environ_group, ene_group):
        super().__init__(bullet_set, owner, group, environ_group, ene_group)
        self.alive_time = pygame.time.get_ticks()
        self.con_time = 250

    def death(self):
        self.atk = 0

    def update(self):
        time = pygame.time.get_ticks()
        if time - self.alive_time > self.con_time:
            self.kill()
            self.atk = 1
            return
        if self.owner.front == 'right':
            self.rect.midleft = self.owner.rect.midright
        else:
            self.rect.midright = self.owner.rect.midleft
        self.check_ene_col()


"""

class extend from EnemyBullet, for enemies' attack
It is essentially a bullet with speed equal 0

"""


class EnemyAttack(EnemyBullet):
    def __init__(self, bullet_set, owner, group, environ_group, player_group):
        super().__init__(bullet_set, owner, group, environ_group, player_group)
        self.con_time = 250

    def death(self):
        self.atk = 0

    def update(self):
        time = pygame.time.get_ticks()
        if time - self.alive_time > self.con_time:
            self.kill()
            self.atk = 10
            return
        if self.owner.front == 'right':
            self.rect.midleft = self.owner.rect.midright
        else:
            self.rect.midright = self.owner.rect.midleft
        self.check_player_col()


class BossBulletCheck(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

    def reset(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def check_bullet(self, group):
        col = pygame.sprite.spritecollideany(self, group)
        if col:
            return True
        return False
