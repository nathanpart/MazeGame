from random import randrange, randint, choice
from typing import Tuple, List

from pygame.rect import Rect
from pygame.sprite import GroupSingle
from pygame.surface import Surface

from maze.Tiles import Tiles
from maze.mazegenerate import MazeMap
from maze.sprites import Critter


class TheMouse(Critter):

    def update(self):
        super().update()


class Mouse(GroupSingle):
    count: int
    cats: Tuple[Surface, Rect, Rect, Rect, Rect]
    cell_width: int
    cell_height: int
    map: MazeMap

    def __init__(self, tiles: Tiles, maze_map: MazeMap):
        super(Mouse, self).__init__(TheMouse(maze_map, tiles.mice))
        self.map = maze_map

    def deploy(self, col, row):

