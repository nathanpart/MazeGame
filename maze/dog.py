from random import choice
from typing import Tuple

from pygame import Surface, Rect

from maze.critters import Critter, CritterGroup
from maze.maze_generate import MazeMap
from maze.mouse import TheMouse
from maze.tiles import Tiles


class TheDog(Critter):

    def __init__(self, maze_map: MazeMap, critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], *groups):
        super().__init__(maze_map, critter_tiles, *groups)
        self.column = 1
        self.row = 1
        self.direction = choice(self.map.passages(self.column, self.row))


class Dog(CritterGroup):
    dog: Critter

    def __init__(self, tiles: Tiles, maze_map: MazeMap):
        self.tiles_mouse = tiles.mice
        self.tiles_dog = tiles.dogs

        super().__init__(maze_map, tiles.dogs, TheDog)

    def activate(self, mouse: TheMouse):
        assert isinstance(self.sprite, TheDog)
        self.sprite.column = mouse.column
        self.sprite.row = mouse.row
        self.sprite.direction = mouse.direction
