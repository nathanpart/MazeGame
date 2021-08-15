from random import choice
from typing import Tuple

from pygame import Surface, Rect

from maze.cats import Cats, Cat
from maze.critters import Critter, CritterGroup
from maze.maze_generate import MazeMap
from maze.mouse import TheMouse
from maze.tiles import Tiles


class TheDog(Critter):
    cats: Cats
    cats_ate: int

    def __init__(self, maze_map: MazeMap, critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], cats: Cats, *groups):
        super().__init__(maze_map, critter_tiles, *groups)
        self.column = 1
        self.row = 1
        self.direction = choice(self.map.passages(self.column, self.row))
        self.cats = cats
        self.cats_ate = 0

    def update(self):
        super().update()
        cat_locations = self.cats.here_kitty_kitty()
        for cat, cat_column, cat_row in cat_locations:
            if self.column == cat_column and self.row == cat_row:
                dog_group = self.groups()[0]
                assert isinstance(dog_group, Dog)
                dog_group.eat_cat(cat)


class DogBlew(Exception):
    pass


class Dog(CritterGroup):
    dog: Critter
    cats_ate: int

    def __init__(self, tiles: Tiles, maze_map: MazeMap):
        self.tiles_mouse = tiles.mice
        self.tiles_dog = tiles.dogs
        self.cats_ate = 0

        super().__init__(maze_map, tiles.dogs, TheDog)

    def activate(self, mouse: TheMouse):
        assert isinstance(self.sprite, TheDog)
        self.sprite.column = mouse.column
        self.sprite.row = mouse.row
        self.sprite.direction = mouse.direction
        self.cats_ate = 0

    def deactivate(self):
        assert isinstance(self.sprite, TheDog)
        return self.sprite.column, self.sprite.row, self.sprite.direction

    def eat_cat(self, cat: Cat):
        cat.kill()
        self.cats_ate += 1
        if self.cats_ate == 3:
            self.pop()

    def pop(self):
        raise DogBlew()