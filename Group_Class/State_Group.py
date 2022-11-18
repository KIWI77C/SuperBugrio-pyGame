import pygame
import setup
import const

pygame.init()


class State:
    """
    The State group is mainly used to switch between levels and interfaces
    """
    def __init__(self, image, environment_group, monster_group, item_group, item_door):
        self.image = image
        self.environment = environment_group
        self.monster = monster_group
        self.finish = False
        self.keys = []
        self.static_mon_lst = []
        self.item = item_group
        self.door = item_door
        self.static_item_lst = []
        self.static_door_lst = []
        for mon in self.monster:
            self.static_mon_lst.append(mon)
        for ele in self.item:
            self.static_item_lst.append(ele)

        for ele in self.door:
            self.static_door_lst.append(ele)

    def update(self, eventlst):
        """
        The state update method is used to implement player actions
        including actions related to characters and menu clicks (subclasses).
        """
        if len(self.monster) == 0:  # If all enemies die, the current level is complete
            if len(self.door) == 0:
                self.finish = True
                return
        self.keys = pygame.key.get_pressed()
        #  position operation
        if setup.slime.move_available:
            if self.keys[pygame.K_d]:
                setup.slime.move_x_right(self.environment)
            if self.keys[pygame.K_a]:
                setup.slime.move_x_left(self.environment)
            if (self.keys[pygame.K_SPACE]) & (setup.slime.speed_y == 0):  # Make sure you jump only on the platform
                const.music_jump.play()  # jump sound
                setup.slime.speed_y = -56
        #  special operation
        setup.slime.input_process(eventlst)


class MainMenu(State):
    """
    The only difference with the MainMenu class is that updates are menu-specific operations
    """
    def update(self, eventlst):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            if self.environment[0].collidepoint(pos):
                self.finish = True
                setup.slime.reset()
                setup.slime.rect.x = 0
                if not setup.slime.alive():
                    setup.Player_Group.add(setup.slime)
            if self.environment[1].collidepoint(pos):
                pygame.quit()
