from random import randrange, randint, choice
from typing import Tuple, List, Optional

from pygame.rect import Rect
from pygame.sprite import Group
from pygame.surface import Surface

from maze.Tiles import Tiles
from maze.mazegenerate import MazeMap, EAST, WEST, NORTH, SOUTH
from maze.mouse import TheMouse
from maze.sprites import Critter


class Cat(Critter):
    activity: int
    is_chased: bool
    mouse: Optional[TheMouse]

    def __init__(self, mouse: TheMouse, maze_map: MazeMap,
                 critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], *sprites):
        self.mouse = mouse
        super().__init__(maze_map, critter_tiles, *sprites)

    def update(self):
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
        if self.column == self.mouse.column and self.row == self.mouse.row:
            self.eat_mouse()
        super().update()

    def eat_mouse(self):
        self.mouse.kill()
        self.mouse = None

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
    mouse: TheMouse

    def __init__(self, tiles: Tiles, maze_map: MazeMap, count: int, mouse: TheMouse, *sprites):
        super(Cats, self).__init__()
        self.add(*sprites)
        self.count = count
        self.cats = tiles.cats
        self.map = maze_map
        self.mouse = mouse

    def reset(self):
        self.empty()
        for i in range(0, self.count):
            cat = Cat(self.mouse, self.map, self.cats, self)
            cat.column, cat.row = self.map.getRandCell()
            cat.row = randrange(11, self.cell_height, 2)

            cat.speed = 1

    def here_kitty_kitty(self) -> List[Tuple[Cat, int, int]]:
        locs = list()
        for cat in self:
            if isinstance(cat, Cat):
                locs.append((cat, cat.column, cat.row))
        return locs
