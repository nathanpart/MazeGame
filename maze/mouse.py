from random import randrange, randint, choice
from typing import Tuple, List, Optional

from pygame.rect import Rect
from pygame.sprite import GroupSingle
from pygame.surface import Surface

from maze.tiles import Tiles
from maze.game_state import GameState
from maze.maze_generate import MazeMap, Point
from maze.sprites import Critter


class TheMouse(Critter):

    def __init__(self, maze_map: MazeMap, critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], *groups):
        super().__init__(maze_map, critter_tiles, *groups)
        self.column = 1
        self.row = 1
        self.direction = choice(self.map.passages(self.column, self.row))


class Mouse(GroupSingle):
    count: int
    tiles: Tuple[Surface, Rect, Rect, Rect, Rect]
    map: MazeMap
    game_state: GameState

    def __init__(self, game_state: GameState, tiles: Tiles, maze_map: MazeMap):
        super(Mouse, self).__init__()
        self.map = maze_map
        self.game_state = game_state
        self.tiles = tiles.mice

    def update(self, *args, **kwargs) -> None:
        if self.sprite is None:
            if self.game_state.next_life():
                self.add(TheMouse(self.map, self.tiles))
        super(Mouse, self).update()

    def mouse_reset(self):
        self.add(TheMouse(self.map, self.tiles))

    def get_location(self) -> Optional[Rect]:
        if self.sprite:
            assert isinstance(self.sprite, TheMouse)
            return self.sprite.rect.copy()
        return None
