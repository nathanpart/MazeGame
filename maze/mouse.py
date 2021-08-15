from random import choice
from typing import Tuple, Optional

from pygame.rect import Rect
from pygame.surface import Surface

from maze.maze_generate import MazeMap
from maze.critters import Critter, CritterGroup


class TheMouse(Critter):

    def __init__(self, maze_map: MazeMap, critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], *groups):
        super().__init__(maze_map, critter_tiles, *groups)
        self.column = 1
        self.row = 1
        self.direction = choice(self.map.passages(self.column, self.row))


class Mouse(CritterGroup):
    def exit_dog(self, column, row, direction):
        assert isinstance(self.sprite, TheMouse)
        self.sprite.column = column
        self.sprite.row = row
        self.sprite.direction = direction
