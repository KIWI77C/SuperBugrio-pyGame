import time

import pygame
import const
import setup
import tools



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(const.screen_size)
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.running = True
        self.eventlst = []
        self.environment = []
        self.state_image = []
        self.monster = []
        self.item = []
        self.door = []
        self.start_time = time.time()

    def update(self, x, monster_group, item_group, item_door):
        setup.slime.update(monster_group, self.environment)
        for p_bul in setup.P_BulletGroup:
            p_bul.update()
        for p_atk in setup.P_AttackGroup:
            p_atk.update()
        for mon in monster_group:
            mon.update(x, self.environment)
        for e_bul in setup.E_BulletGroup:
            e_bul.update()
        for e_atk in setup.E_AttackGroup:
            e_atk.update()
        for ele in item_group:
            ele.update()
        if len(self.monster) == 0:
            for ele in item_door:
                ele.update()

    def run(self, x):  # x The x variable is used to declare which level (interface) to run
        pygame.init()
        pygame.mixer.music.play(100)  # Load the background music of the game, 100 is the  times of loop playback
        while self.running:
            current_state = setup.StateList[x]  # load the current level
            self.state_image = current_state.image
            self.environment = current_state.environment
            self.monster = current_state.monster
            self.item = current_state.item

            self.door = current_state.door
            self.eventlst = pygame.event.get()
            for event in self.eventlst:
                if event.type == pygame.QUIT:
                    pygame.quit()

            #  operation
            current_state.update(self.eventlst)

            # update the y position
            if (x != 0) & (x != setup.StateNum - 1) & (x != setup.StateNum - 2):
                if setup.slime.speed_y < 44:  # Restrict falling speed or it may cross the platform
                    setup.slime.speed_y += 5  # Simulated gravity effect
                setup.slime.gravity(self.environment)
                self.update(self.environment, self.monster, self.item, self.door)

            #  draw
            self.screen.blit(self.state_image, (0, 0))  # level background
            # Graphics are drawn only in normal game levels
            if (x != 0) & (x != setup.StateNum - 1) & (x != setup.StateNum - 2):
                setup.Player_Group.draw(self.screen)  # player
                setup.Mission_list_01[x - 1].draw(self.screen)  # monster
                setup.P_BulletGroup.draw(self.screen)  # player bullets
                setup.P_AttackGroup.draw(self.screen)  # player attacks
                setup.E_BulletGroup.draw(self.screen)  # monster bullets
                setup.E_AttackGroup.draw(self.screen)  # monster attacks
                # setup.Item_Group.draw(self.screen)  # items
                setup.Item_lst[x - 1].draw(self.screen)  # items
                if len(self.monster) == 0:
                    setup.Item_door_lst[x - 1].draw(self.screen)  # items
          # menu
            if (x != 0) & (x != setup.StateNum - 1) & (x != setup.StateNum - 2):
                menu_background = pygame.Surface((1000, 60), pygame.SRCALPHA)
                menu_background.blit(pygame.image.load('Graphics/InfoMenu.png'), (0, 0), (0, 0, 1000, 60))
                HPImage = const.font.render(f'{setup.slime.HP}', 1, pygame.Color(255, 255, 255))
                StateNumber = const.font.render(f'{x}', 1, pygame.Color(255, 255, 255))
                time_now = int(time.time() - self.start_time)
                TimeImage = const.font.render(f'{time_now}', 1, pygame.Color(255, 255, 255))
                menu_background.blit(HPImage, (142, 18))
                menu_background.blit(StateNumber, (550, 18))
                menu_background.blit(TimeImage, (900, 18))
                menu_background.set_alpha(300)
                self.screen.blit(menu_background, (0, 0))

            pygame.display.flip()
            setup.clock.tick(const.FPS)

            """
            level switch
            """
            if not setup.slime.alive():  # if player dies
                x = setup.StateNum - 2  # GameOver
                tools.clean_bullet()  # clean the bullets
                setup.slime.rect.y = 0
                for mon in current_state.static_mon_lst:  # reset the monster
                    mon.death()
                    mon.reset(mon.init_set)
                for ele in current_state.static_item_lst:  # reset the items
                    ele.reset(ele.init_set)
                # -------------------------------
                for ele in current_state.static_door_lst:  # reset the items
                    ele.reset(ele.init_set)
                self.start_time = time.time()
                current_state.finish = False
                continue
            if current_state.finish:
                if (x == setup.StateNum - 2) | (x == setup.StateNum - 1):  # GameOver or GameWin
                    x = 0  # return to the start menu
                    tools.clean_bullet()  # clean the bullet
                    setup.slime.rect.x = 0
                    setup.slime.rect.y = 0
                    current_state.finish = False
                    self.start_time = time.time()
                    continue
                if x == setup.StateNum - 3:
                    x = setup.StateNum - 1
                    tools.clean_bullet()
                    setup.slime.rect.x = 0
                    setup.slime.rect.y = 0
                    for mon in current_state.static_mon_lst:
                        mon.death()
                        mon.reset(mon.init_set)
                    for ele in current_state.static_item_lst:
                        ele.reset(ele.init_set)

                    # -------------------------------
                    for ele in current_state.static_door_lst:  # reset the items
                        ele.reset(ele.init_set)
                    current_state.finish = False
                    continue
                else:  # Complete the level properly
                    x += 1  # next level
                    for mon in current_state.static_mon_lst:
                        mon.death()
                        mon.reset(mon.init_set)
                    for ele in current_state.static_item_lst:
                        ele.reset(ele.init_set)

                    # -------------------------------
                    for ele in current_state.static_door_lst:  # reset the items
                        ele.reset(ele.init_set)
                    tools.clean_bullet()
                    setup.slime.rect.x = 0
                    setup.slime.rect.y = 0
                    current_state.finish = False
                    #  transitions
                    if (x != setup.StateNum - 1) & (x != setup.StateNum - 2):
                        if x == 1:  # background story
                            self.screen.blit(pygame.image.load('Graphics/story.png'), (0, 0))
                            pygame.display.flip()
                            wait = True
                            while wait:
                                for event in pygame.event.get():
                                    if (event.type == pygame.KEYDOWN) | (event.type == pygame.MOUSEBUTTONDOWN):
                                        wait = False
                        self.screen.fill(pygame.Color('black'))
                        StateNumber = const.font.render(f'Level {x}', 1, pygame.Color('white'))
                        self.screen.blit(StateNumber, (400, 300))
                        pygame.display.flip()
                        time.sleep(2)
                    continue
