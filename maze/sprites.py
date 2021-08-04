from typing import Tuple, Union, Sequence, List

import pygame
from pygame.rect import Rect
from pygame.sprite import AbstractGroup, Group, Sprite
from pygame.surface import Surface

from maze.game_state import GameState
from maze.maze_generate import WEST, NORTH, EAST, SOUTH, MazeMap, Point
from maze.mouse import TheMouse


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
    game_state: GameState
    score_func: str

    def __init__(self, col: int, row: int, game_state: GameState, score_func: str,
                 maze_map: MazeMap, tile: Surface, *groups):
        super().__init__(maze_map, *groups)
        self.image = tile
        self.column = col
        self.row = row
        self.game_state = game_state
        self.score_func = score_func

    def update(self, *args, **kwargs) -> None:
        mouse = args[0]
        assert isinstance(mouse, TheMouse)
        if self.column == mouse.column and self.row == mouse.row:
            if hasattr(self.game_state, self.score_func):
                getattr(self.game_state, self.score_func)()
            else:
                raise AttributeError("Game state does not have method %s" % self.score_func)
            self.kill()


class ItemGroup(Group):
    game_state: GameState
    score_fund: str
    item_count: int
    tile: Surface
    map: MazeMap

    def __init__(self, game_state: GameState, score_func: str, item_count: int,
                 maze_map: MazeMap, tile: Surface, *sprites: Union[Sprite, Sequence[Sprite]]) -> None:
        super().__init__(*sprites)
        self.game_state = game_state
        self.score_fund = score_func
        self.item_count = item_count
        self.map = maze_map
        self.tile = tile

    def new_game(self, exclude_list: List[Point]):
        self.empty()
        for _ in range(0, self.item_count):
            new_point = self.map.get_rand_cell()
            while new_point in exclude_list:
                new_point = self.map.get_rand_cell()
            item = Item(new_point.col, new_point.row, self.game_state, self.score_fund, self.map, self.tile)
            self.add(item)
            exclude_list.append(new_point)

    def item_locations(self) -> List[Point]:
        item_list = list()
        for item in self.sprites():
            assert isinstance(item, Item)
            item_list.append(Point(item.column, item.row))
        return item_list

    @property
    def is_empty(self) -> bool:
        return len(self.sprites()) == 0
