import pygame
import random

ATK_SOUND_U = 'resources\sound_attack_boom.ogg'
ATK_SOUND_X = 'resources\sound_attack_twitch.ogg'
DEATH_SOUND = 'resources\sound_death.ogg'
VOLUME_LEVEL = 0.42

FILE_PATH_U = 'resources\monster1.png'
FILE_PATH_X = 'resources\monster2.png'

ALLIED_LOCATION = (0,0)
ENEMY_LOCATION = (100, 100)

# Constants
C_DAMAGE_MULTIPLIER = 1.2
C_MOVE_POWER_DIVISOR = 1.25

C_DEFENSE_MULTIPLIER = 0.25
C_REDUCTION_BASE = 8.4

C_XP_BOUNTY_MULTIPLIER = 16
C_GOLD_BOUNTY_MULTIPLIER = 40

C_LEVEL_CURVE_A = []
C_LEVEL_CURVE_B = []
C_LEVEL_CURVE_C = []
previous_amount_a = 0
previous_amount_b = 0
previous_amount_c = 0
gain_a = 6
gain_b = 14
gain_c = 20

STAT_STRENGTHS = ['legendary', 'strong', 'regular', 'weak', 'pathetic']
STAT_NAMES = ['hp', 'ph_atk', 'ph_def', 'mp_atk', 'mp_def', 'speed']
STAT_GAIN_STRENGTHS = {
    'legendary': 5.0, 'strong': 3.0,
    'regular': 1.75, 'weak': 1.20,
    'pathetic': 0.75
    }
STAT_BASE_FACTORS = {
    'hp': 3.0,
    'ph_atk': 30.0, 'ph_def': 2.0,
    'mp_atk': 25.0, 'mp_def': 2.0,
    'speed': 2.0
    }
STAT_GAINS_PER_LEVEL = {}
for stat in STAT_NAMES:
    STAT_GAINS_PER_LEVEL[stat] = {}
    for strength in STAT_STRENGTHS:
        STAT_GAINS_PER_LEVEL[stat][strength] = STAT_GAIN_STRENGTHS[strength] * STAT_BASE_FACTORS[stat]

for i in range(0, 50):
    C_LEVEL_CURVE_A.append(previous_amount_a + (gain_a*i))
    C_LEVEL_CURVE_B.append(previous_amount_b + (gain_b*i))
    C_LEVEL_CURVE_C.append(previous_amount_c + (gain_c*i))
    previous_amount_a = C_LEVEL_CURVE_A[i]
    previous_amount_b = C_LEVEL_CURVE_B[i]
    previous_amount_c = C_LEVEL_CURVE_C[i]
    #print '| Level %i = %i |' % (i+1, previous_amount_a)

class Monster(object):
    #
    #
    def __init__(self, name, owner, level=None):
        print '| Creating UNIT of type: %s |' % name
        self.name = name
        self.owner = owner
        self.stats_randomized = False
        self.stats_calculated = False
        self.level_calculated = False
        self.xp = -1337
        self.xp_to_next = -8084
        self.x, self.y = (0, 0)
        if level:
            self.level = level
        else:
            self.level = 5
            
        self.setup_defaults()
        self.setup_sounds()
        self.setup_image()

    def setup_defaults(self):
        self.update_level()
        self.randomize_stat_gain()
        self.update_stats()
        self.hp = self.base_hp
        #self.moves = {
        #    'Claw': Move('Claw', 10, qwer_loc='q'),
        #    'Evil Claw': Move('Evil Claw', 5, qwer_loc='w')
        #    }
        self.moves = {
            'Attack': Move('Attack', 50, qwer_loc='q'),
            'Steal': Move('Steal', 50, qwer_loc='w'),
            'Magic': Move('Magic', 25, qwer_loc='e'),
            'Item': Move('Item', 0, qwer_loc='r')
            }

    def setup_sounds(self):
        self.sounds = {
            'move1': pygame.mixer.Sound(ATK_SOUND_U),
            'move2': pygame.mixer.Sound(ATK_SOUND_X),
            'death': pygame.mixer.Sound(DEATH_SOUND)
            }
        for sound in self.sounds:
            self.sounds[sound].set_volume(VOLUME_LEVEL)       

    def setup_image(self):
        self.image = pygame.image.load(FILE_PATH_X)
        self.size_x = 64
        self.size_y = 64
        self.rect = self.image.get_rect()
        self.update()

    def make_legendary(self):
        self.randomize_stat_gain(override='legendary')

    def randomize_stat_gain(self, override=None):
        self.stat_gains = {}
        for stat in STAT_NAMES:
            random_strength = STAT_STRENGTHS[random.randint(0, len(STAT_STRENGTHS)-1)]
            self.stat_gains[stat] = STAT_GAINS_PER_LEVEL[stat][random_strength]
            if override:
                self.stat_gains[stat] = STAT_GAINS_PER_LEVEL[stat][override]
        self.stats_randomized = True

    def update_stats(self):
        if self.level_calculated:
            self.base_hp = self.level * self.stat_gains['hp']
            self.ph_atk = self.level * self.stat_gains['ph_atk']
            self.ph_def = self.level * self.stat_gains['ph_def']
            self.mp_atk = self.level * self.stat_gains['mp_atk']
            self.mp_def = self.level * self.stat_gains['mp_def']
            self.speed = self.level * self.stat_gains['speed']
        else:
            self.update_level()
            self.update_stats()

    def update_level(self, looped=False):
        if self.xp != -1337:
            if self.xp >= self.xp_to_next:
                if self.xp >= C_LEVEL_CURVE_A[self.level+1] and self.xp >= C_LEVEL_CURVE_A[self.level+2]:
                    self.level += 2
                    self.xp_to_next = C_LEVEL_CURVE_A[self.level+1]
                    self.update_level(looped=True)
                if self.xp >= C_LEVEL_CURVE_A[self.level+1] and self.xp < C_LEVEL_CURVE_A[self.level+2]:
                    self.level += 1
                    self.xp_to_next = C_LEVEL_CURVE_A[self.level+1]
                    self.update_level(looped=True)
                if self.xp < C_LEVEL_CURVE_A[self.level+1]:
                    self.level_calculated = True
        else:
            self.xp = C_LEVEL_CURVE_A[self.level+1]
            self.xp_to_next = C_LEVEL_CURVE_A[self.level+2]
        self.level_calculated = True

    def get_xp_bounty(self):
        return self.level*C_XP_BOUNTY_MULTIPLIER

    def get_gold_bounty(self):
        return self.level*C_GOLD_BOUNTY_MULTIPLIER

    def update(self):
        if self.owner == 'player':
            self.x, self.y = ALLIED_LOCATION
        else:
            self.x, self.y = ENEMY_LOCATION
        self.rect.topleft = (self.x, self.y)

    def get_calculated_damage(self, target, move):
        # This is very basic and not real for now
        move_base_power = (move.power / C_MOVE_POWER_DIVISOR)
        atk_multiplier = (self.ph_atk * C_DAMAGE_MULTIPLIER)
        raw_damage = (move_base_power * atk_multiplier)

        def_multiplier = (target.ph_def * C_DEFENSE_MULTIPLIER)
        base_reduction = (raw_damage / C_REDUCTION_BASE)
        raw_reduction = (def_multiplier * base_reduction)
        
        return (raw_damage - raw_reduction)

def set_sprite_anchor_points(new_allied_location, new_enemy_location):
    global ALLIED_LOCATION, ENEMY_LOCATION
    ALLIED_LOCATION = new_allied_location
    ENEMY_LOCATION = new_enemy_location

class Move(object):
    #
    #
    def __init__(self, name, power, qwer_loc=None):
        self.name = name
        self.power = power
        self.qwer_loc = qwer_loc
