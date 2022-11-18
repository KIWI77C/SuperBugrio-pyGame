# Data related to game initialization, including pre-loading images, pre-defining variables, etc

import pygame
import const
import Group_Class.Actor_Group
import Group_Class.Environment_Group
import Group_Class.Info_Group
import Group_Class.State_Group
import Group_Class.Item_Group

# 启动变量

# 时钟变量
import tools

clock = pygame.time.Clock()

# Level images
MenuImage = tools.get_image('Graphics/Menu_StartMenu.png', 0, 0, 1000, 800, const.screen_width, const.screen_height)
GameOverImage = tools.get_image('Graphics/Menu_GameOver.png', 0, 0, 1000, 800, const.screen_width, const.screen_height)
StateImage_1 = tools.get_image('Graphics/source.png', 125, 1255, 1000, 800, const.screen_width, const.screen_height)
StateImage_2 = pygame.image.load('Graphics/Map_level2.png')
StateImage_3 = pygame.image.load('Graphics/Map_level4.png')
GameWinImage = tools.get_image('Graphics/Menu_GameWin.png', 0, 0, 1000, 800, const.screen_width, const.screen_height)

# CoolDown dictionaries
Player_cd = {'shoot': 0, 'attack': 250}
Monster_cd = {'shoot': 0, 'attack': 0, 'blink': 0, 'iaii': 0, 'Morn Afah': -10000, 'boss_iaii': 0, 'boss_blink': 0,
              'bullet_avoid': 0}

# Player
Player_Group = pygame.sprite.Group()
slime = Group_Class.Actor_Group.Player('Graphics/player.png', const.actor_set, Player_cd)
Player_Group.add(slime)

# Environments
ButtonList = (pygame.Rect(264, 448, 220, 88), pygame.Rect(536, 448, 220, 88))
ButtonList2 = (pygame.Rect(196, 579, 266, 76), pygame.Rect(535, 579, 266, 76))
# Each environment object is named 'environment_ level _ SerialNumber _ Type'
Environment_Group_1 = pygame.sprite.Group()
environment_1_1_platform = Group_Class.Environment_Group.Environment(605, 255, 244, 80, Environment_Group_1)
environment_1_2_platform = Group_Class.Environment_Group.Environment(242, 415, 278, 80, Environment_Group_1)
environment_1_3_ground = Group_Class.Environment_Group.Environment(0, 675, 360, 300, Environment_Group_1)
environment_1_4_ground = Group_Class.Environment_Group.Environment(470, 675, 600, 250, Environment_Group_1)

Environment_Group_2 = pygame.sprite.Group()
Environment_Group_2 = Environment_Group_1

Environment_Group_3 = pygame.sprite.Group()
environment_2_1_ground = Group_Class.Environment_Group.Environment(0, 675, 1000, 300, Environment_Group_3)
environment_2_2_wall = Group_Class.Environment_Group.Environment(360, 480, 80, 345, Environment_Group_3)
environment_2_3_platform = Group_Class.Environment_Group.Environment(0, 230, 350, 45, Environment_Group_3)
environment_2_4_platform = Group_Class.Environment_Group.Environment(500, 330, 400, 45, Environment_Group_3)
environment_2_5_platform = Group_Class.Environment_Group.Environment(900, 200, 100, 30, Environment_Group_3)
Environment_Group_2 = Environment_Group_3

Environment_Group_4 = pygame.sprite.Group()
environment_3_1_ground = Group_Class.Environment_Group.Environment(0, 675, 1000, 300, Environment_Group_4)
# EnvironmentList = [Environment_Group_1]

# Monsters
MonsterGroup01 = pygame.sprite.Group()
# Each monster object is named 'TypeName & Number _ level number_ Serial number'
Ghost01_01_01 = Group_Class.Actor_Group.Ghost(const.Ghost01_01_01, MonsterGroup01, Monster_cd)
Shooter01_01_01 = Group_Class.Actor_Group.Shooter(const.Shooter01_01_01, MonsterGroup01, Monster_cd)
Shooter02_01_01 = Group_Class.Actor_Group.Shooter(const.Shooter02_01_01, MonsterGroup01, Monster_cd)

MonsterGroup02 = pygame.sprite.Group()
Ghost01_02_01 = Group_Class.Actor_Group.SamuraiGhost(const.SamuraiGhost_02_01, MonsterGroup02, Monster_cd)
SaberGhost01_02_01 = Group_Class.Actor_Group.SaberGhost(const.SaberGhost01_02_01, MonsterGroup02, Monster_cd)
Ghooter01_02_01 = Group_Class.Actor_Group.Ghooter(const.Ghooter_02_01, MonsterGroup02, Monster_cd)

MonsterGroupBoss = pygame.sprite.Group()
Boss = Group_Class.Actor_Group.Boss(const.Boss, MonsterGroupBoss, Monster_cd)

Mission_list_01 = [MonsterGroup01, MonsterGroup02, MonsterGroupBoss]

# Bullet
P_BulletGroup = pygame.sprite.Group()  # bullets of player
P_AttackGroup = pygame.sprite.Group()  # attack of player
E_BulletGroup = pygame.sprite.Group()  # bullet of monster
E_AttackGroup = pygame.sprite.Group()  # attack of monster

# Info
Info_hint = Group_Class.Info_Group.Info((0, 0), 'monitor information')

# Item groups set
Item_Group = pygame.sprite.Group()
Item_Group2 = pygame.sprite.Group()
Item_Group3 = pygame.sprite.Group()
Item_Door = pygame.sprite.Group()
# Items instance initialize
item_blood_vessel_01_01 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker01_set, Item_Group, Player_Group,
                                                             slime)
item_blood_vessel_01_02 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker02_set, Item_Group, Player_Group,
                                                             slime)
item_blood_vessel_01_03 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker03_set, Item_Group, Player_Group,
                                                             slime)
item_blood_vessel_01_04 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker04_set, Item_Group, Player_Group,
                                                             slime)
item = [item_blood_vessel_01_01, item_blood_vessel_01_02, item_blood_vessel_01_03, item_blood_vessel_01_04]
item_door = Group_Class.Item_Group.Door(const.item_door_set, Item_Door, Player_Group)

item_blood_vessel_02_01 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker02_set, Item_Group2, Player_Group,
                                                             slime)
item_blood_vessel_02_02 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker03_set, Item_Group2, Player_Group,
                                                             slime)
item_blood_vessel_02_03 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker01_set, Item_Group2, Player_Group,
                                                             slime)
item_scroll_02_01 = Group_Class.Item_Group.Scroll(const.item_scroll_set, Item_Group2, Player_Group, slime)

item_blood_vessel_03_01 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker01_set, Item_Group3, Player_Group,
                                                             slime)
item_blood_vessel_03_02 = Group_Class.Item_Group.BloodVessel(const.item_blood_beaker03_set, Item_Group3, Player_Group,
                                                             slime)

Item_lst = [Item_Group, Item_Group2, Item_Group3]
Item_door_lst = [Item_Door, Item_Door, Item_Door]

# State & Level
MainMenu = Group_Class.State_Group.MainMenu(MenuImage, ButtonList, [], [], [])
GameOver = Group_Class.State_Group.MainMenu(GameOverImage, ButtonList2, [], [], [])
GameWin = Group_Class.State_Group.MainMenu(GameWinImage, ButtonList2, [], [], [])
State01 = Group_Class.State_Group.State(StateImage_1, Environment_Group_1, MonsterGroup01, Item_Group, Item_Door)
State02 = Group_Class.State_Group.State(StateImage_2, Environment_Group_2, MonsterGroup02, Item_Group2, Item_Door)
State03 = Group_Class.State_Group.State(StateImage_3, Environment_Group_4, MonsterGroupBoss, Item_Group3, Item_Door)
StateList = [MainMenu, State01, State02, State03, GameOver, GameWin]
StateNum = len(StateList)
