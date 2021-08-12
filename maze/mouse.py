from random import choice
from typing import Tuple, Optional

from pygame.rect import Rect
from pygame.sprite import GroupSingle
from pygame.surface import Surface

from maze.tiles import Tiles
from maze.game_state import GameState
from maze.maze_generate import MazeMap
from maze.critters import Critter


class TheMouse(Critter):

    def __init__(self, maze_map: MazeMap, critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], *groups):
        super().__init__(maze_map, critter_tiles, *groups)
        self.column = 1
        self.row = 1
        self.direction = choice(self.map.passages(self.column, self.row))


class Mouse(GroupSingle):
    count: int
    tiles: Tuple[Surface, Rect, Rect, Rect, Rect]
    restore_rect: Rect
    back_ground: Surface

    def __init__(self, tiles: Tiles, maze_map: MazeMap):
        self.tiles = tiles.mice
        super(Mouse, self).__init__(TheMouse(maze_map, self.tiles))
        self.restore_rect = Rect(1, 1, 32, 32)
        self.back_ground = tiles.ground

    def update(self, *args, **kwargs) -> bool:
        if self.sprite is None:
            return False
        self.restore_rect = self.sprite.rect.copy()
        super(Mouse, self).update()
        return True

    def pre_draw(self, surface: Surface):
        surface.blit(self.back_ground, self.restore_rect)

    def mouse_reset(self, maze_map: MazeMap):
        self.add(TheMouse(maze_map, self.tiles))

    def get_location(self) -> Optional[Rect]:
        if self.sprite:
            assert isinstance(self.sprite, TheMouse)
            return self.sprite.rect.copy()
        return None

    @property
    def current_loc(self):
        if self.sprite:
            assert isinstance(self.sprite, TheMouse)
            return self.sprite.current_loc
        else:
            return 0, 0

    def move(self, maze_map: MazeMap, x: int, y: int, s_dir: int):
        s = self.sprite
        if s:
            assert isinstance(s, TheMouse)
            if s.in_transit:
                return
            dir_funcs = [s.move_north, s.move_east, s.move_south, s.move_west]
            if not maze_map.is_wall(x, y):
                dir_funcs[s_dir]()

    def move_up(self, maze_map: MazeMap):
        x, y = self.current_loc
        self.move(maze_map, x, y - 1, 0)

    def move_down(self, maze_map: MazeMap):
        x, y = self.current_loc
        self.move(maze_map, x, y + 1, 2)

    def move_left(self, maze_map: MazeMap):
        x, y = self.current_loc
        self.move(maze_map, x - 1, y, 3)

    def move_right(self, maze_map: MazeMap):
        x, y = self.current_loc
        self.move(maze_map, x + 1, y, 1)
