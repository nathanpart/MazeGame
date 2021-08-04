from random import randint, choice
from typing import Tuple, List, Optional

from pygame.rect import Rect
from pygame.sprite import Group
from pygame.surface import Surface

from maze.tiles import Tiles
from maze.maze_generate import MazeMap, EAST, WEST, NORTH, SOUTH, Point
from maze.mouse import Mouse, TheMouse
from maze.sprites import Critter


def eat_mouse(mouse: TheMouse):
    mouse.kill()


class Cat(Critter):
    activity: int
    is_chased: bool
    mouse_group: Optional[Mouse]

    def __init__(self, mouse: Mouse, maze_map: MazeMap,
                 critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], *sprites):
        self.mouse_group = mouse
        super().__init__(maze_map, critter_tiles, *sprites)

    def update(self):
        mouse = self.mouse_group.sprite
        if mouse is None:
            return              # Player is either between lives after being ate. Or in game over state

        assert isinstance(mouse, TheMouse)

        if not self.in_transit:
            if self.is_chased:
                self.direction = choice(self.map.passages(self.column, self.row, self.direction))
                if self.speed != 0:
                    self.in_transit = True
            else:
                if self.activity == 0:
                    self.activity = randint(1, 10)
                    self.speed = randint(0, 2)
                else:
                    self.activity -= 1
                if self.speed != 0:
                    self.direction = choice(self.map.passages(self.column, self.row))
                    self.in_transit = True
        if self.column == mouse.column and self.row == mouse.row:
            eat_mouse(mouse)
        super().update()

    def chased(self, dog_col: int, dog_row: int):
        self.is_chased = True
        self.speed = 2
        current_direction = self.direction
        flee_direction = self.direction
        if self.direction == EAST:
            if dog_row == self.row and dog_col < self.column:
                flee_direction = WEST       # Flee away from the chasing dog
        elif self.direction == NORTH:
            if dog_col == self.column and dog_row < self.row:
                flee_direction = SOUTH
        elif self.direction == WEST:
            if dog_row == self.row and dog_col > self.column:
                flee_direction = EAST       # Flee away from the chasing dog
        else:
            if dog_row == self.row and dog_row > self.row:
                flee_direction = NORTH
        self.direction = choice(self.map.passages(self.column, self.row, flee_direction))

        # Detect trapped cat
        if self.direction == current_direction and flee_direction != current_direction:
            self.speed = 0


class Cats(Group):
    count: int
    cats: Tuple[Surface, Rect, Rect, Rect, Rect]
    cell_width: int
    cell_height: int
    map: MazeMap
    mouse: Mouse

    def __init__(self, tiles: Tiles, maze_map: MazeMap, count: int, mouse: Mouse, *sprites):
        super(Cats, self).__init__()
        self.add(*sprites)
        self.count = count
        self.cats = tiles.cats
        self.map = maze_map
        self.mouse = mouse

    def reset(self, exclude_list: List[Point]):
        self.empty()
        for _ in range(0, self.count):
            cat = Cat(self.mouse, self.map, self.cats)
            self.add(cat)
            new_point = self.map.get_rand_cell()
            while new_point in exclude_list or new_point < Point(20, 30):
                new_point = self.map.get_rand_cell()
            cat.column = new_point.col
            cat.row = new_point.row
            cat.speed = 1

            exclude_list.append(new_point)

    def here_kitty_kitty(self) -> List[Tuple[Cat, int, int]]:
        locs = list()
        for cat in self:
            if isinstance(cat, Cat):
                locs.append((cat, cat.column, cat.row))
        return locs

    def ate_the_mouse(self):
        pass

    def update(self, *args, **kwargs) -> None:

        super().update(*args, **kwargs)
