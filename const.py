import threading
import pygame

pygame.init()

# Game name
pygame.display.set_caption("Super Bugrio")

# Game Const
FPS = 30
font = pygame.font.SysFont('small fonts', 44, 1)
icon = pygame.image.load("Graphics/player.png")
pygame.display.set_icon(icon)

# Screen Const
screen_width = 1000
screen_height = 800
screen_size = (screen_width, screen_height)

# Player initialization Const
actor_set = {'width': 50, 'height': 50, 'maxHP': 100, 'DEF': 0, 'init_x': 0, 'init_y': 440, 'speed_x': 10, 'speed_y': 0}
player_skill_cd = {'shoot': 250, 'attack': 250}

# Monster initialization Const
ShooterandGhost_init_cd = {'shoot': 1500, 'attack': 1500}
SaberGhost_init_cd = {'shoot': 750, 'attack': 1000, 'blink': 2500}
SamuraiGhost_init_cd = {'shoot': 750, 'attack': 250, 'iaii': 2000}
Boss_init_cd = {'shoot': 1300, 'attack': 500, 'Morn Afah': 10000, 'boss_iaii': 2500, 'boss_blink': 2500,
                'bullet_avoid': 5000}
Boss_shooter_init_cd = {'shoot': 500}

# Each environment object is named 'environment_ level _ SerialNumber _ Type'
Shooter01_01_01 = {'image_path': 'Graphics/ghost1.png', 'init_x': 720, 'init_y': 150, 'maxHP': 100,
                   'speed_x': -2, 'speed_y': 0, 'scope': 400, 'p_interval': 80, 'atk_range': 250}
Shooter02_01_01 = {'image_path': 'Graphics/ghost2.png', 'init_x': 720, 'init_y': 575, 'maxHP': 100,
                   'speed_x': -5, 'speed_y': 0, 'scope': 550, 'p_interval': 80, 'atk_range': 350}
Shooter03_01_01 = {'image_path': 'Graphics/ghost3.png', 'init_x': 150, 'init_y': 150, 'maxHP': 100,
                   'speed_x': -2, 'speed_y': 0, 'scope': 400, 'p_interval': 80, 'atk_range': 250}
Ghost01_01_01 = {'image_path': 'Graphics/ghost1.png', 'init_x': 370, 'init_y': 250, 'maxHP': 100,
                 'speed_x': -5, 'speed_y': 0, 'scope': 250, 'p_interval': 80, 'atk_range': 79}
SaberGhost01_02_01 = {'image_path': 'Graphics/ghost3.png', 'init_x': 740, 'init_y': 300, 'maxHP': 100,
                      'speed_x': -6, 'speed_y': 0, 'scope': 450, 'p_interval': 80, 'atk_range': 250}
SamuraiGhost_02_01 = {'image_path': 'Graphics/ghost4.png', 'init_x': 370, 'init_y': 250, 'maxHP': 100,
                      'speed_x': -3, 'speed_y': 0, 'scope': 400, 'p_interval': 80, 'atk_range': 400}
Ghooter_02_01 = {'image_path': 'Graphics/ghost5.png', 'init_x': 720, 'init_y': 575, 'maxHP': 100,
                 'speed_x': -5, 'speed_y': 0, 'scope': 550, 'p_interval': 80, 'atk_range': 400}
Boss = {'image_path': 'Graphics/bigboss.png', 'init_x': 500, 'init_y': 150, 'width': 100, 'height': 100, 'maxHP': 15,
        'speed_x': -5, 'speed_y': 0, 'scope': 400, 'p_interval': 80, 'atk_range': 1000}
Boss_shooter = {'image_path': 'Graphics/ghost1.png', 'init_x': 0, 'init_y': 150, 'maxHP': 100,
                'speed_x': 0, 'speed_y': 0, 'scope': 1000, 'p_interval': 80, 'atk_range': 1000}

# Bullet Const
player_bullet_set = {'image_path': 'Graphics/Bullet_player.png', 'width': 20, 'height': 20, 'speed': 13, 'atk': 1}
player_attack_set = {'image_path': 'Graphics/ItemSword.png', 'width': 40, 'height': 40, 'speed': 0, 'atk': 1}
monster_bullet_set = {'image_path': 'Graphics/Bullet_enemy.png', 'width': 20, 'height': 20, 'speed': 6, 'atk': 10}
monster_atk_set = {'image_path': 'Graphics/ItemSword.png', 'width': 40, 'height': 40, 'speed': 0, 'atk': 10}

# Item constant
item_blood_beaker01_set = {'image_path': 'Graphics/ItemBottle.png', 'width': 32, 'height': 63, 'x': 60, 'y': 550}
item_blood_beaker02_set = {'image_path': 'Graphics/ItemBottle.png', 'width': 32, 'height': 32, 'x': 700, 'y': 180}
item_blood_beaker03_set = {'image_path': 'Graphics/ItemBottle.png', 'width': 16, 'height': 16, 'x': 700, 'y': 550}
item_blood_beaker04_set = {'image_path': 'Graphics/ItemBottle.png', 'width': 16, 'height': 16, 'x': 400, 'y': 650}
item_scroll_set = {'image_path': 'Graphics/ItemScroll.png', 'width': 16, 'height': 16, 'x': 910, 'y': 100}
item_door_set = {'image_path': 'Graphics/ItemDoor.png', 'width': 16, 'height': 16, 'x': 800, 'y': 555}

# Background music
pygame.mixer.music.load("Music/background.mp3")
# background music used by https://freesound.org/people/josefpres/sounds/610926/

# Other Sound
music_jump = pygame.mixer.Sound("Music/jump.mp3")  # jump
music_jump.set_volume(0.9)
music_pd = pygame.mixer.Sound("Music/player death.mp3")  # death
music_pd.set_volume(0.9)
music_shoot = pygame.mixer.Sound("Music/shoot.mp3")  # shoot
music_shoot.set_volume(1.4)
music_sep = pygame.mixer.Sound("Music/special_effects.mp3")  # special
music_sep.set_volume(0.4)
music_attack = pygame.mixer.Sound("Music/attacks.mp3")  # attack
music_attack.set_volume(0.6)

# LOCK = threading.RLock()
