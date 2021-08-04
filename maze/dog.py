from random import choice
from typing import Tuple, List, Optional

from pygame.rect import Rect
from pygame.sprite import GroupSingle
from pygame.surface import Surface

from maze.tiles import Tiles
from maze.cats import Cats, Cat
from maze.maze_generate import MazeMap, WEST, EAST, NORTH, SOUTH, Point
from maze.mouse import Mouse, TheMouse
from maze.critters import Critter


class TheDog(Critter):
    chased_cat: Optional[Cat]
    way_points: List[Point]
    search_time: int

    @property
    def is_chasing(self):
        return self.chased_cat is not None

    def __init__(self, maze_map: MazeMap, tiles: Tuple[Surface, Rect, Rect, Rect, Rect],
                 col: int, row: int, cat: Optional[Cat], *group):
        super(TheDog, self).__init__(maze_map, tiles, *group)
        self.chased_cat = cat

        self.way_points = [Point(cat.column, cat.row)]
        self.speed = 4

        if self.is_chasing:
            if cat.column == col:
                self.column = col
                self.row = (row + 1) if (cat.row > row) else (row - 1)
            else:
                self.row = row
                self.column = (col + 1) if (cat.column > col) else (col - 1)
        else:
            self.search_time = 10
            d = choice(self.map.passages(col, row))
            self.column = [col - 1, col, col + 1, col][d]
            self.row = [row, row - 1, row, row + 1][d]

    def update(self):
        if not self.in_transit:
            if not self.is_chasing:
                if self.search_time == 0:
                    self.kill()             # Reached time to disappear
                    return
                dog_group = self.groups()[0]
                assert isinstance(dog_group, Dog)
                kitty = dog_group.find_cat(self.column, self.row)
                if kitty is None:
                    self.search_time -= 1
                    moves = [self.move_east, self.move_north, self.move_west, self.move_south]
                    moves[choice(self.map.passages(self.column, self.row, self.direction))]()
                else:
                    # Cat detected - the chase is on
                    self.chased_cat = kitty
                    self.way_points = [Point(kitty.column, kitty.row)]

            if self.is_chasing:
                # Track chased cat
                cat_way_point = Point(self.chased_cat.column, self.chased_cat.row)
                if cat_way_point != self.way_points[-1]:
                    self.way_points.append(cat_way_point)

                # If we reach the a way point remove it
                if self.way_points[0].here(self.column, self.row):
                    del self.way_points[0]

                    # If we removed the last way point we have reached the cat so we eat it
                    if len(self.way_points) == 0:
                        self.eat_cat()
                        return

                # Keep moving towards the current way point
                if len(self.way_points) != 0:
                    way_point = self.way_points[0]
                    if way_point.col == self.column:
                        if way_point.row < self.row:
                            self.move_north()
                        else:
                            self.move_south()
                    else:
                        if way_point.col < self.column:
                            self.move_east()
                        else:
                            self.move_west()

        super().update()

    def eat_cat(self):
        self.chased_cat.kill()
        self.chased_cat = None
        self.search_time = 5


class Dog(GroupSingle):
    tiles_dog: Tuple[Surface, Rect, Rect, Rect, Rect]
    count: int
    cell_width: int
    cell_height: int
    map: MazeMap
    cats: Cats
    mouse: Mouse
    cat_chase: bool
    chased_cat: Optional[Cat]

    def __init__(self, tiles: Tiles, maze_map: MazeMap, mouse: Mouse, cats: Cats):
        super(Dog, self).__init__(None)
        self.tiles_dog = tiles.dogs
        self.map = maze_map
        self.cat_chase = False
        self.cats = cats
        self.mouse = mouse

    def deploy(self):
        mouse = self.mouse.sprite
        assert isinstance(mouse, TheMouse)

        col = mouse.column
        row = mouse.row

        chased_cat = self.find_cat(col, row)

        self.add(TheDog(self.map, self.tiles_dog, col, row, chased_cat, self))

    def find_cat(self, col: int, row: int) -> Optional[Cat]:
        min_col = col
        while WEST in self.map.passages(min_col, row):
            min_col -= 1
        max_col = col
        while EAST in self.map.passages(max_col, row):
            max_col += 1
        min_row = row

        while NORTH in self.map.passages(col, min_row):
            min_row -= 1
        max_row = row
        while SOUTH in self.map.passages(col, max_row):
            max_row += 1

        delta_row = 0
        delta_col = 0
        delta_row_cat = None
        delta_col_cat = None
        cat_locations = self.cats.here_kitty_kitty()
        for cat, cat_col, cat_row in cat_locations:
            if (cat_row == row) and (min_col <= cat_col <= max_col) and abs(cat_col - col) < delta_col:
                delta_col = cat_col - col
                delta_col_cat = cat
            if (cat_col == col) and (min_row <= cat_row <= max_row) and (abs(cat_row - row) < delta_row):
                delta_row = cat_row - row
                delta_row_cat = cat

        if delta_col != 0 and abs(delta_col) < abs(delta_row):
            chased_cat = delta_col_cat
        elif delta_row != 0:
            chased_cat = delta_row_cat
        else:
            chased_cat = None
        return chased_cat

    def get_location(self) -> Optional[Rect]:
        if self.sprite:
            assert isinstance(self.sprite, TheMouse)
            return self.sprite.rect.copy()
        return None
