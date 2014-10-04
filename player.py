#

# 3rd party imports
import pygame

# Local imports
import monster

# Globals
FILE_PATH = 'resources\player.png'


class Player(object):
    #
    #
    def __init__(self):
        self.name = 'player'
        self.characters = []
        self.x = 400
        self.y = 400
        self.size = (32, 32)
        self.size_multiplier = 1.50
        self.frame_index = 0
        self.speed = 16.0
        self.image = pygame.image.load(FILE_PATH)
        self.rect = self.image.get_rect()
        self.setup()

    def setup(self):
        self.characters.append(monster.Monster('George', 'player', level=9))
        self.characters.append(monster.Monster('Cloud', 'player', level=13))
        for char in self.characters:
            char.make_legendary()
        self.in_party = self.characters

    def get_active_monster(self):
        return self.in_party[0]

    def move(self, direction, multi):
        if multi:
            speed = self.speed * 0.72
            self.x += (speed * direction[0])
            self.y += (speed * direction[1])
        else:
            self.x += (self.speed * direction[0])
            self.y += (self.speed * direction[1])

    def update(self):
        self.rect.topleft = (self.x, self.y)
