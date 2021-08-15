from typing import Tuple, Optional

from pygame.rect import Rect
from pygame.sprite import GroupSingle
from pygame.surface import Surface

from maze.maze_generate import MazeMap, WEST, NORTH, EAST, SOUTH
from maze.mouse import TheMouse
from maze.sprites import MazeSprite
from maze.tiles import Tiles


class Critter(MazeSprite):
    """
    A sub class of MazeSprite add functionality that is common to the dog and cat
    """

    tiles: Surface
    dir_rects: Tuple[Rect, Rect, Rect, Rect]
    _direction: int
    in_transit: bool
    speed: int
    speeds = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    def __init__(self, maze_map: MazeMap, critter_tiles: Tuple[Surface, Rect, Rect, Rect, Rect], *groups):
        """
        Initialize the critter specific fields

        :param maze_map: the MazeMap of the maze the critter lives in
        :param critter_tiles: The critter's tile tuple
        :param groups:  Any groups the critter sprite is associated with
        """
        super().__init__(maze_map, *groups)

        self.tiles, *self.dir_rects = critter_tiles
        self.direction = 0
        self.speed = 2
        self.in_transit = False

    @property
    def direction(self):
        """
        Property of the critters current direction
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        assert 0 <= value < 4
        self._direction = value
        self.image = self.tiles.subsurface(self.dir_rects[value])

    @property
    def current_loc(self):
        return self.column, self.row

    def move_west(self):
        """
        Start the sprite moving to the location to the west
        """
        self.in_transit = True
        self.direction = WEST

    def move_north(self):
        """
        Start the sprite moving to the location to the north
        """
        self.in_transit = True
        self.direction = NORTH

    def move_east(self):
        """
        Start the sprite moving to the location to the east
        """
        self.in_transit = True
        self.direction = EAST

    def move_south(self):
        """
        Start the sprite moving to the location to the south
        """
        self.in_transit = True
        self.direction = SOUTH

    def update(self):
        """
        Update the critter's sprite location for the next frame
        """
        if self.in_transit:
            mask = self.speeds[self._direction]
            self.rect = self.rect.move(mask[0] * self.speed, mask[1] * self.speed)
            if (self.rect.top % 32 == 0) and (self.rect.left % 32 == 0):
                self.in_transit = False
                self.column += [-1, 0, 1, 0][self._direction]
                self.row += [0, -1, 0, 1][self._direction]


class CritterGroup(GroupSingle):
    tiles: Tuple[Surface, Rect, Rect, Rect, Rect]

    def __init__(self, maze_map: MazeMap, critter: Tuple[Surface, Rect, Rect, Rect, Rect], critter_class):
        self.tiles = critter
        self.critter_class = critter_class
        super().__init__(critter_class(maze_map, self.tiles))

    def update(self, *args, **kwargs) -> bool:
        restore_tiles = args[0]
        assert isinstance(restore_tiles, list)

        if self.sprite is None:
            return False
        restore_tiles.append(self.sprite.rect.copy())
        super().update()
        return True

    def critter_reset(self, maze_map: MazeMap):
        self.add(self.critter_class(maze_map, self.tiles))

    def get_location(self) -> Optional[Rect]:
        if self.sprite:
            assert isinstance(self.sprite, Critter)
            return self.sprite.rect.copy()
        return None

    @property
    def current_loc(self):
        if self.sprite:
            assert isinstance(self.sprite, Critter)
            return self.sprite.current_loc
        else:
            return 0, 0

    def move(self, maze_map: MazeMap, x: int, y: int, s_dir: int):
        s = self.sprite
        if s:
            assert isinstance(s, Critter)
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
