from typing import Tuple

from pygame.rect import Rect
from pygame.surface import Surface

from maze.maze_generate import MazeMap, WEST, NORTH, EAST, SOUTH
from maze.sprites import MazeSprite


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

    @property
    def current_loc(self):
        return self.column, self.row

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