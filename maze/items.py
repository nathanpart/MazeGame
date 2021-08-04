from typing import Union, Sequence, List

from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from maze.game_state import GameState
from maze.maze_generate import MazeMap, Point
from maze.mouse import TheMouse
from maze.sprites import MazeSprite


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