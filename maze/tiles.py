import os
from typing import Tuple, List

import pygame
from pygame import Rect
from pygame.image import load
from pygame.surface import Surface


MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
TILE_FILE = "tiles2.png"

DIGIT_FILES = ["numbers_blue.png", "numbers_green.png", "numbers_lt_green.png", "numbers_purple.png",
               "numbers_red.png", "numbers_white.png", "numbers_yellow.png"]
DC_BLUE = 0
DC_GREEN = 1
DC_CYAN = 2
DC_PURPLE = 3
DC_RED = 4
DC_WHITE = 5
DC_YELLOW = 6

NUM_YEL_FILE = "numbers_yellow.png"
NUM_WHT_FILE = "numbers_white.png"
NUM_LG_FILE = "numbers_lt_green.png"

GROUND_RECT = Rect(0, 0, 32, 32)
BONE_RECT = Rect(32, 0, 32, 32)
CHEESE_RECT = Rect(64, 0, 32, 32)
WALL_RECT = Rect(96, 0, 32, 32)
MICE_RECT = Rect(0, 32, 128, 32)
CATS_RECT = Rect(0, 64, 128, 32)
DOGS_RECT = Rect(0, 96, 128, 32)

WEST_RECT = Rect(0, 0, 32, 32)
NORTH_RECT = Rect(32, 0, 32, 32)
EAST_RECT = Rect(64, 0, 32, 32)
SOUTH_RECT = Rect(96, 0, 32, 32)

ZERO_RECT = Rect(0, 0, 16, 32)
ONE_RECT = Rect(16, 0, 16, 32)
TWO_RECT = Rect(32, 0, 16, 32)
THREE_RECT = Rect(48, 0, 16, 32)
FOUR_RECT = Rect(64, 0, 16, 32)
FIVE_RECT = Rect(80, 0, 16, 32)
SIX_RECT = Rect(96, 0, 16, 32)
SEVEN_RECT = Rect(112, 0, 16, 32)
EIGHT_RECT = Rect(128, 0, 16, 32)
NINE_RECT = Rect(144, 0, 16, 32)


class Tiles:
    tiles: Surface
    num_yellow: Surface
    num_white: Surface
    num_lt_green: Surface
    ground: Surface
    bone: Surface
    cheese: Surface
    wall: Surface
    mice: Tuple[Surface, Rect, Rect, Rect, Rect]
    cats: Tuple[Surface, Rect, Rect, Rect, Rect]
    dogs: Tuple[Surface, Rect, Rect, Rect, Rect]

    digit_rects: List[Rect]
    digits: List[Surface]

    def __init__(self):
        file = os.path.join(MAIN_DIR, TILE_FILE)

        try:
            self.tiles = load(file).convert()
            self.digits = [load(os.path.join(MAIN_DIR, digit_file)).convert() for digit_file in DIGIT_FILES]
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))

        self.ground = self.tiles.subsurface(GROUND_RECT)
        self.bone = self.tiles.subsurface(BONE_RECT)
        self.cheese = self.tiles.subsurface(CHEESE_RECT)
        self.wall = self.tiles.subsurface(WALL_RECT)

        self.mice = (self.tiles.subsurface(MICE_RECT), WEST_RECT, NORTH_RECT, EAST_RECT, SOUTH_RECT)
        self.cats = (self.tiles.subsurface(CATS_RECT), WEST_RECT, NORTH_RECT, EAST_RECT, SOUTH_RECT)
        self.dogs = (self.tiles.subsurface(DOGS_RECT), WEST_RECT, NORTH_RECT, EAST_RECT, SOUTH_RECT)

        self.digit_rects = [ZERO_RECT, ONE_RECT, TWO_RECT, THREE_RECT, FOUR_RECT,
                            FIVE_RECT, SIX_RECT, SEVEN_RECT, EIGHT_RECT, NINE_RECT]
