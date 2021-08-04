import os
from typing import Tuple

import pygame
from pygame import Rect
from pygame.image import load
from pygame.surface import Surface


MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
TILE_FILE = "maze_tiles.png"

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


class Tiles:
    tiles: Surface
    ground: Surface
    bone: Surface
    cheese: Surface
    wall: Surface
    mice: Tuple[Surface, Rect, Rect, Rect, Rect]
    cats: Tuple[Surface, Rect, Rect, Rect, Rect]
    dogs: Tuple[Surface, Rect, Rect, Rect, Rect]

    def __init__(self):
        file = os.path.join(MAIN_DIR, TILE_FILE)

        try:
            self.tiles = load(file).convert()
        except pygame.error:
            raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))

        self.ground = self.tiles.subsurface(GROUND_RECT)
        self.bone = self.tiles.subsurface(BONE_RECT)
        self.cheese = self.tiles.subsurface(CHEESE_RECT)
        self.wall = self.tiles.subsurface(WALL_RECT)

        self.mice = (self.tiles.subsurface(MICE_RECT), WEST_RECT, NORTH_RECT, EAST_RECT, SOUTH_RECT)
        self.mice = (self.tiles.subsurface(MICE_RECT), WEST_RECT, NORTH_RECT, EAST_RECT, SOUTH_RECT)
        self.mice = (self.tiles.subsurface(MICE_RECT), WEST_RECT, NORTH_RECT, EAST_RECT, SOUTH_RECT)
