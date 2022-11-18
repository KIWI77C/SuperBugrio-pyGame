import pygame
import math

import Group_Class.ability
import const
import setup
import tools

pygame.init()


class Actor(pygame.sprite.Sprite):

    def __init__(self, image_path, actor_set, player_cd):
        super().__init__()
        self.actor_set = actor_set
        self.environment_group = None

        # Images
        self.image_right = pygame.transform.scale(pygame.image.load(image_path),
                                                  (self.actor_set['width'], self.actor_set['height']))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right

        # Rect
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.width = self.size[0]
        self.height = self.size[1]
        self.rect.x = actor_set['init_x']
        self.rect.y = actor_set['init_y']

        # Speed
        self.speed_x = actor_set['speed_x']
        self.speed_y = actor_set['speed_y']
        self.static_speed_x = self.speed_x
        self.higher_speed_x = self.speed_x * 2

        # Fighting const
        self.maxHP = self.actor_set['maxHP']
        self.HP = self.maxHP  # int
        self.DEF = self.actor_set['DEF']
        self.init_cd = player_cd

        # Status
        self.status = 'normal'
        self.move_available = True
        self.atk_obj = None
        self.front = 'right'

    def move_x_right(self, collide_group):
        self.image = self.image_right  # If the character moves to the right, the right-facing picture should be loaded
        self.rect.x += self.speed_x
        tools.board_judge(self)
        self.check_x_collision(collide_group)
        self.front = 'right'

    def move_x_left(self, collide_group):
        self.image = self.image_left
        self.rect.x -= self.speed_x
        tools.board_judge(self)
        self.check_x_collision(collide_group)
        self.front = 'left'

    # def move_fx_positive(self, x):
    #     self.image = self.image_right
    #     self.rect.x += self.speed_coefficient
    #     tools.board_judge(self)
    #     self.check_x_collision(x)
    #
    # def move_fx_negative(self, x):
    #     self.image = self.image_left
    #     self.rect.x -= self.speed_coefficient
    #     tools.board_judge(self)
    #     self.check_x_collision(x)

    #  Simulated gravity
    def gravity(self, collide_group):
        self.rect.y += self.speed_y
        tools.board_judge(self)
        self.check_y_collision(collide_group)

    #  detect collision
    def check_x_collision(self, collide_group):
        collision_environment = pygame.sprite.spritecollideany(self, collide_group)
        if collision_environment:
            self.adjust_x_position(collision_environment)

    def check_y_collision(self, collide_group):
        collision_environment = pygame.sprite.spritecollideany(self, collide_group)
        if collision_environment:
            self.adjust_y_position(collision_environment)

    def adjust_x_position(self, environment):
        if self.rect.x < environment.rect.x:
            self.rect.right = environment.rect.left
        else:
            self.rect.left = environment.rect.right

    def adjust_y_position(self, environment):
        if self.rect.bottom < environment.rect.bottom:
            self.rect.bottom = environment.rect.top
            self.speed_y = 0
        else:
            self.rect.top = environment.rect.bottom
            self.rect.top = environment.rect.bottom
            self.speed_y = 5

    def cd_check(self, sk_name):
        pass

    def shoot(self):
        pass

    def attack(self):
        pass

    # def update(self):
    #     pass


class Player(Actor):
    def __init__(self, image_path, actor_set, player_cd):
        super().__init__(image_path, actor_set, player_cd)
        self.monster_group = None
        self.blink = False

    def reset(self):
        self.status = 'normal'
        self.HP = self.maxHP

    # Process the player's input for manipulating the character
    def input_process(self, eventlst):
        for event in eventlst:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    self.status = 'shoot'
                    # const.music_shoot.play()
                elif event.key == pygame.K_k:
                    self.status = 'attack'
                    # const.music_attack.play()
                elif event.key == pygame.K_LSHIFT:
                    self.status = 'speed_up'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_j:
                    self.status = 'normal'
                elif event.key == pygame.K_LSHIFT:
                    self.status = 'normal'

    # finite state machine
    def process_state(self):
        if self.status == 'normal':
            self.normal()
        elif self.status == 'speed_up':
            self.speed_x_up()
        elif self.status == 'shoot':
            self.shoot()
        elif self.status == 'attack':
            try:
                if not self.atk_obj.alive():
                    self.status = 'normal'
                    self.move_available = True
                    self.atk_obj = None
                    return
            except AttributeError:
                pass
            self.attack()

    # check if player could attack or shoot
    def cd_check(self, sk_name):
        act_time = pygame.time.get_ticks()
        if (act_time - self.init_cd[sk_name]) > const.player_skill_cd[sk_name]:
            self.init_cd[sk_name] = act_time
            return True
        return False

    # speed_up, push L_shift to active
    def speed_x_up(self):
        self.speed_x = self.higher_speed_x

    # reset the speed if player is not pushing L_shift
    def normal(self):
        self.speed_x = self.static_speed_x

    # function for shoot
    def shoot(self):
        if (len(setup.P_BulletGroup) < 5) & self.cd_check('shoot'):
            new_bullet = Group_Class.ability.PlayerBullet(
                const.player_bullet_set, self, setup.P_BulletGroup, self.environment_group, self.monster_group)
            const.music_shoot.play()

    # function close attack
    def attack(self):
        if len(setup.P_AttackGroup) < 1 & self.cd_check('attack'):
            self.atk_obj = Group_Class.ability.PlayerAttack(
                const.player_attack_set, self, setup.P_AttackGroup, self.environment_group, self.monster_group)
            const.music_attack.play()

    # function for player taking damage
    def hurt(self, dam=10):
        self.HP -= dam - self.DEF

    # function for player's death
    def death(self):
        const.music_pd.play()
        self.reset()
        self.kill()

    # update player's states and parameters every frame
    def update(self, monster_group, env):
        self.environment_group = env
        self.monster_group = monster_group
        if (self.HP <= 0) | (self.rect.y > const.screen_height):
            self.death()
            return
        self.process_state()
        p_mon_collision = pygame.sprite.spritecollideany(self, monster_group)
        if p_mon_collision:
            self.adjust_x_position(p_mon_collision)


class Enemy(Actor):
    def __init__(self, monster_set, group, enemy_cd):
        pygame.sprite.Sprite.__init__(self)
        self.init_set = monster_set
        #  Group
        self.group = group
        self.group.add(self)
        #  Image
        self.image_right = pygame.image.load(monster_set['image_path'])
        self.image_right = pygame.transform.scale(self.image_right,
                                                  (const.actor_set['width'], const.actor_set['height']))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_left
        # Rect
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.width = self.size[0]
        self.height = self.size[1]
        self.rect.x = monster_set['init_x']
        self.rect.y = monster_set['init_y']
        # Speed
        self.speed_x = monster_set['speed_x']
        self.speed_y = monster_set['speed_y']
        # Fighting
        self.maxHP = 1
        self.HP = self.maxHP  # int
        self.DEF = 0
        self.patrol_center = {'x': self.rect.x, 'y': self.rect.y}
        self.scope = monster_set['scope']
        self.atk_range = monster_set['atk_range']
        self.init_cd = enemy_cd
        self.atk_obj = None
        # Status
        self.front = 'left'
        self.bullet = None
        self.status = 'patrol'
        self.interval = monster_set['p_interval']

    # reset enemies' parameters and states
    def reset(self, monster_set):
        # self.image_right = pygame.image.load(monster_set['image_path'])
        # self.image_right = pygame.transform.scale(self.image_right, self.size)
        # self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_left
        # self.rect = self.image.get_rect()
        # self.size = self.image.get_size()
        # self.width = self.size[0]
        # self.height = self.size[1]
        # position reset
        self.rect.x = monster_set['init_x']
        self.rect.y = monster_set['init_y']
        self.speed_x = monster_set['speed_x']
        self.speed_y = monster_set['speed_y']
        self.patrol_center = {'x': self.rect.x, 'y': self.rect.y}
        self.front = 'left'
        # self.maxHP = const.actor_set['maxHP']
        self.HP = self.maxHP  # int
        # self.atk_range = monster_set['atk_range']
        self.bullet = None
        self.status = 'patrol'
        # self.scope = monster_set['scope']
        self.interval = monster_set['p_interval']
        if not self.alive():
            self.group.add(self)

    def move_x(self, dist, mission=0):
        if dist < 0:
            self.image = self.image_left
            self.front = 'left'
        else:
            self.image = self.image_right
            self.front = 'right'
        self.rect.x += dist
        self.check_x_collision(self.environment_group)

    def check_x_collision(self, x):
        collision_environment = pygame.sprite.spritecollideany(self, x)
        if collision_environment:
            self.adjust_x_position(collision_environment)
            self.speed_x *= -1

    # make sure the enemy always face the player
    def front_correction(self):
        if self.rect.centerx > setup.slime.rect.centerx:
            self.front = 'left'
            self.image = self.image_left
        else:
            self.front = 'right'
            self.image = self.image_right

    def cd_check(self, sk_name):
        act_time = pygame.time.get_ticks()
        if (act_time - self.init_cd[sk_name]) > const.ShooterandGhost_init_cd[sk_name]:
            self.init_cd[sk_name] = act_time
            return True
        return False

    # enemy will patrol at first. When the player approaches, the enemy will track the player. The enemy will eneter
    # a state of fight. The enemy can switch from one state to another
    def search(self, mission):
        dist_x = setup.slime.rect.centerx - self.rect.centerx
        dist_y = setup.slime.rect.centery - self.rect.centery
        if (self.scope > math.hypot(dist_x, dist_y)) & setup.slime.alive():
            if abs(dist_x) > self.atk_range:
                norm_vector = dist_x // abs(dist_x)
                self.status = 'track'
                self.speed_x = abs(self.speed_x) * norm_vector
            else:
                self.status = 'fight'
        else:
            self.status = 'patrol'

    # finite-state machine
    def process_state(self, mission):
        if self.status == 'patrol':
            self.patrol(mission)
        elif self.status == 'track':
            self.track(mission)
        elif self.status == 'fight':
            self.fight()

    def patrol(self, mission):
        self.move_x(self.speed_x, mission)
        if tools.interval_judge(self, self.interval, self.patrol_center):
            self.speed_x *= -1

    def track(self, mission):
        self.move_x(self.speed_x, mission)
        self.patrol_center['x'] = self.rect.x
        self.patrol_center['y'] = self.rect.y

    def fight(self):
        self.shoot()

    # function for shoot
    def shoot(self):
        if self.cd_check('shoot'):
            if self.bullet is None:
                new_bullet = Group_Class.ability.EnemyBullet(
                    const.monster_bullet_set, self, setup.E_BulletGroup, self.environment_group, setup.Player_Group)
                self.bullet = new_bullet
            else:
                if not self.bullet.alive():
                    self.bullet.reset(self.bullet.init_set)
            return True
        return False

    # function of attack
    def attack(self):
        if self.cd_check('attack'):
            if self.atk_obj is None:
                self.atk_obj = Group_Class.ability.EnemyAttack(
                    const.monster_atk_set, self, setup.E_AttackGroup, self.environment_group, setup.Player_Group)
            elif not self.atk_obj.alive():
                self.atk_obj.reset(const.player_attack_set)
            return True
        else:
            return False

    def hurt(self, dam=1):
        damage = dam - self.DEF
        if damage > 0:
            self.HP -= damage

    def death(self):
        self.kill()
        return self.rect.x, self.rect.y

    # update player's states and parameters every frame
    def update(self, mission, env):
        self.environment_group = env
        if (self.HP <= 0) | (self.rect.y > const.screen_height):
            self.death()
            return
        self.front_correction()
        self.search(mission)
        self.process_state(mission)
        self.check_x_collision(setup.Player_Group)
        self.speed_y += 5
        self.gravity(mission)


"""

Class for a kind of enemy, extend from Enemy

"""


class Ghost(Enemy):
    def fight(self):
        self.attack()


"""

Class for a kind of enemy, extend from Enemy

"""


class Shooter(Enemy):
    def fight(self):
        self.shoot()


"""

Class for a kind of enemy, extend from Enemy

"""


class SaberGhost(Enemy):
    def __init__(self, monster_set, group, enemy_cd):
        super().__init__(monster_set, group, enemy_cd)
        self.fight_state = 'blink'

    def cd_check(self, sk_name):
        act_time = pygame.time.get_ticks()
        if (act_time - self.init_cd[sk_name]) > const.SaberGhost_init_cd[sk_name]:
            self.init_cd[sk_name] = act_time
            return True
        return False

    # finite-state machine to let this type of enemy could teleport to player's back and attack
    def fight(self):
        if self.fight_state == 'blink':
            if self.cd_check('blink'):
                dist = setup.slime.rect.centerx - self.rect.centerx
                if setup.slime.front == 'right':
                    self.move_x(dist - math.ceil(setup.slime.width / 2 + math.ceil(self.width / 2) + 5))
                elif setup.slime.front == 'left':
                    self.move_x(dist + math.ceil(setup.slime.width / 2 + math.ceil(self.width / 2) + 5))
                self.init_cd['attack'] = pygame.time.get_ticks()
                self.fight_state = 'attack'
            else:
                self.shoot()
                self.fight_state = 'attack'
        elif self.fight_state == 'attack':
            if self.attack():
                self.fight_state = 'blink'
                self.init_cd['shoot'] = pygame.time.get_ticks()


"""

Class for a kind of enemy, extend from Enemy

"""


class SamuraiGhost(Enemy):
    def __init__(self, monster_set, group, enemy_cd):
        super().__init__(monster_set, group, enemy_cd)
        self.fight_status = 'iaii'

    def cd_check(self, sk_name):
        act_time = pygame.time.get_ticks()
        if (act_time - self.init_cd[sk_name]) > const.SamuraiGhost_init_cd[sk_name]:
            self.init_cd[sk_name] = act_time
            return True
        return False

    # finite-state machine to let this type of enemy could sprint and attack at the same time
    def fight(self):
        if self.cd_check('iaii'):
            self.fight_status = 'iaii'
        elif (pygame.time.get_ticks() - self.init_cd['iaii']) > 1000:
            self.fight_status = 'wait'
        if self.fight_status == 'iaii':
            self.attack()
            if self.atk_obj.atk != 0:
                if self.rect.centerx < setup.slime.rect.centerx:
                    self.move_x(abs(2 * self.speed_x))
                else:
                    self.move_x(-abs(2 * self.speed_x))


"""

Class for a kind of enemy, extend from Enemy
This type of enemy could shoot or attack at close range according to the distance from the player

"""


class Ghooter(Enemy):
    def fight(self):
        dist = abs(setup.slime.rect.centerx - self.rect.centerx)
        if 450 > dist >= 80:
            self.shoot()
        elif dist < 80:
            self.attack()


"""

The Boss, extend from Enemy
Boss state have three parts. The maxhp of Boss is 15. 
Part1； HP is in [15, 10],  

"""


class Boss(Enemy):
    def __init__(self, monster_set, group, enemy_cd):
        super().__init__(monster_set, group, enemy_cd)
        self.iaii_state = True
        self.maxHP = self.init_set['maxHP']
        self.HP = self.maxHP
        self.DEF = 0
        self.image_right = pygame.transform.scale(self.image_right, (self.init_set['width'], self.init_set['height']))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.rect = self.image_right.get_rect()
        self.player_input = None
        self.status = 'track'
        self.fight_state = 'part1'
        self.part2_status = 'Morn Afah'
        self.part3_status = 'iaii'
        self.shooterlst = []
        self.bulletlst = []
        self.rect.x = monster_set['init_x']
        self.rect.y = monster_set['init_y']
        self.avoid_rect = Group_Class.ability.BossBulletCheck(
            self.rect.x - 50, self.rect.y, self.width + 100, self.height)

    def cd_check(self, sk_name):
        act_time = pygame.time.get_ticks()
        if (act_time - self.init_cd[sk_name]) > const.Boss_init_cd[sk_name]:
            self.init_cd[sk_name] = act_time
            return True
        return False

    def search(self, mission):
        dist_x = setup.slime.rect.centerx - self.rect.centerx
        dist_y = setup.slime.rect.centery - self.rect.centery
        if (self.scope > math.hypot(dist_x, dist_y)) & setup.slime.alive():
            if abs(dist_x) > self.atk_range:
                norm_vector = dist_x // abs(dist_x)
                self.status = 'track'
                self.speed_x = abs(self.speed_x) * norm_vector
            else:
                self.status = 'fight'

    def fight(self):
        self.avoid_rect.rect.x = self.rect.x - 50
        self.avoid_rect.rect.y = self.rect.y - 50
        if self.fight_state == 'part1':
            self.shoot()
            self.attack()
        elif self.fight_state == 'part2':
            if self.part2_status == 'Morn Afah':
                self.MornAfah()
            elif self.part2_status == 'boss_blink':
                self.Boss_blink()
            elif self.part2_status == 'shoot':
                self.shoot()
                self.part2_status = 'Morn Afah'
        elif self.fight_state == 'part3':
            self.Attack_check()
            if self.part3_status == 'reflect':
                self.Reflect()
            elif self.part3_status == 'counterattack':
                self.CounterAttack()
            elif self.part3_status == 'iaii':
                self.Boss_iaii()

    def MornAfah(self):
        if self.cd_check('Morn Afah'):
            # bullet shoot
            if len(setup.MonsterGroupBoss) < 4:
                self.shooterlst.append(Group_Class.Actor_Group.Ghost(
                    const.Ghost01_01_01, setup.MonsterGroupBoss, setup.Monster_cd))
                self.shooterlst.append(Group_Class.Actor_Group.Ghost(
                    const.Ghooter_02_01, setup.MonsterGroupBoss, setup.Monster_cd))
            self.part2_status = 'boss_blink'
        else:
            self.part2_status = 'boss_blink'

    def Boss_iaii(self):
        if self.cd_check('boss_iaii'):
            self.iaii_state = True
        elif (pygame.time.get_ticks() - self.init_cd['boss_iaii']) > 750:
            self.part3_status = 'iaii'
            self.iaii_state = True
            return
        if self.iaii_state:
            self.attack()
            if self.atk_obj.atk != 0:
                if self.rect.centerx < setup.slime.rect.centerx:
                    self.move_x(abs(2 * self.speed_x))
                else:
                    self.move_x(-abs(2 * self.speed_x))

    def Boss_blink(self):
        if self.cd_check('boss_blink'):
            dist = setup.slime.rect.centerx - self.rect.centerx
            if setup.slime.front == 'right':
                self.move_x(dist - math.ceil(setup.slime.width / 2 + math.ceil(self.width / 2) + 5))
            elif setup.slime.front == 'left':
                self.move_x(dist + math.ceil(setup.slime.width / 2 + math.ceil(self.width / 2) + 5))
            self.init_cd['attack'] = pygame.time.get_ticks()
        else:
            self.attack()
            self.part2_status = 'shoot'

    def Attack_check(self):
        dist = setup.slime.rect.centerx - self.rect.centerx
        if setup.slime.status in ['shoot']:
            self.part3_status = 'reflect'
            return
        if (abs(dist) < (55 + self.width / 2)) & (setup.slime.status in ['shoot', 'attack']):
            self.part3_status = 'counterattack'

    def Reflect(self):
        self.shoot()
        self.part3_status = 'iaii'

    def CounterAttack(self):
        self.attack()
        self.part3_status = 'wait'

    def shoot(self):
        if self.cd_check('shoot'):
            if len(self.bulletlst) < 3:
                new_bullet = Group_Class.ability.EnemyBullet(
                    const.monster_bullet_set, self, setup.E_BulletGroup, self.environment_group, setup.Player_Group)
                self.bullet = new_bullet
                self.bulletlst.append(self.bullet)
            else:
                return False
            for bullet in self.bulletlst:
                if not bullet.alive():
                    bullet.reset(bullet.init_set)
                    try:
                        self.bulletlst.pop(bullet)
                    except TypeError:
                        pass
            return True
        return False

    def update(self, mission, env):
        self.environment_group = env
        if 10 >= self.HP > 5:
            self.fight_state = 'part2'
        elif self.HP <= 5:
            self.fight_state = 'part3'
        if (self.HP <= 0) | (self.rect.y > const.screen_height):
            self.death()
            return
        i = 0
        for bullet in self.bulletlst:
            if not bullet.alive():
                self.bulletlst.pop(i)
            i += 1
        self.front_correction()
        self.search(mission)
        self.process_state(mission)
        self.check_x_collision(setup.Player_Group)
        self.speed_y += 5
        self.gravity(mission)


"""

Class for a kind of enemy, extend from Enemy
This type of enemy will be summoned by the Boss.

"""
