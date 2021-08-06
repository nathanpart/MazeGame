from typing import List

from pygame.sprite import Group
from pygame.surface import Surface

from maze.game_state import GameState
from maze.maze_generate import MazeMap, Point
from maze.mouse import TheMouse
from maze.sprites import MazeSprite


class Item(MazeSprite):
    game_state: GameState
    score_delta: int
    bone_delta: int

    def __init__(self, col: int, row: int, game_state: GameState, maze_map: MazeMap,
                 tile: Surface, score_delta: int, bone_delta: int, *groups):
        super().__init__(maze_map, *groups)
        self.image = tile
        self.column = col
        self.row = row
        self.game_state = game_state
        self.score_delta = score_delta
        self.bone_delta = bone_delta

    def update(self, *args, **kwargs) -> None:
        mouse = args[0]
        assert isinstance(mouse, TheMouse)
        if self.column == mouse.column and self.row == mouse.row:
            self.game_state.score += self.score_delta
            self.game_state.bones += self.bone_delta
            self.kill()


class ItemGroup(Group):
    game_state: GameState
    item_count: int
    tile: Surface
    map: MazeMap
    score_delta: int
    bone_delta: int

    def __init__(self, game_state: GameState, maze_map: MazeMap, tile: Surface, score_delta: int, bone_delta: int):
        super().__init__([])
        self.game_state = game_state
        self.map = maze_map
        self.tile = tile
        self.score_delta = score_delta
        self.bone_delta = bone_delta

    def new_game(self, exclude_list: List[Point], item_count: int):
        self.empty()
        for _ in range(0, item_count):
            new_point = self.map.get_rand_cell()
            while new_point in exclude_list:
                new_point = self.map.get_rand_cell()
            item = Item(new_point.col, new_point.row, self.game_state, self.map,
                        self.tile, self.score_delta, self.bone_delta)
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
