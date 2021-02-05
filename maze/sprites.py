from random import randrange
from typing import Tuple, Optional, List

import pygame
from pygame.rect import Rect
from pygame.sprite import AbstractGroup
from pygame.surface import Surface

from maze.mazegenerate import WEST, NORTH, EAST, SOUTH, MazeMap


class MazeSprite(pygame.sprite.Sprite):
    _column: int
    _row: int
    map: MazeMap

    def __init__(self, maze_map: MazeMap, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self._column = 0
        self._row = 0
        self.rect = Rect(0, 0, 32, 32)
        self.map = maze_map

    def _compute_location(self):
        self.rect.top = self._row * 32
        self.rect.left = self._row * 32

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = value
        self._compute_location()

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value
        self._compute_location()


class Critter(MazeSprite):
    tiles: Surface
    dir_rects: Tuple[Rect, Rect, Rect, Rect]
    _direction: int
    in_transit: bool
    speed: int
    speeds = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    def __init__(self, maze_map: MazeMap, critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], *groups):
        super().__init__(maze_map, *groups)

        self.tiles, *self.dir_rects = critter_tiles
        self.direction = 0
        self.speed = 2
        self.in_transit = False

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        assert 0 <= value < 4
        self._direction = value
        self.image = self.tiles.subsurface(self.dir_rects[value])

    def move_west(self):
        self.in_transit = True
        self.direction = WEST

    def move_north(self):
        self.in_transit = True
        self.direction = NORTH

    def move_east(self):
        self.in_transit = True
        self.direction = EAST

    def move_south(self):
        self.in_transit = True
        self.direction = SOUTH

    def update(self):
        if self.in_transit:
            mask = self.speeds[self._direction]
            self.rect = self.rect.move(mask[0] * self.speed, mask[1] * self.speed)
            if (self.rect.top % 32 == 0) and (self.rect.left % 32 == 0):
                self.in_transit = False
                self.column += [-1, 0, 1, 0][self._direction]
                self.row += [0, -1, 0, 1][self._direction]


class Item(MazeSprite):

    def __init__(self, maze_map: MazeMap, tile: Surface, *groups):
        super().__init__(maze_map, *groups)
        self.image = tile

    def place_in_cell(self, cell_x, cell_y, cell_map: Optional[List[List[str]]] = None):
        col = (cell_x * 2) + 1
        row = (cell_y * 2) + 1

        if cell_map is None:
            self.column = col
            self.row = row
            return

        options = [(col, row)]
        if cell_map[col + 1][row] == ' ':
            options.append((col + 1, row))
        if cell_map[col][row + 1] == ' ':
            options.append((col, row + 1))

        selection = randrange(0, len(options)) if len(options) > 1 else 0
        self.column, self.row = options[selection]
