import pygame
from pygame.rect import Rect
from pygame.sprite import AbstractGroup

from maze.maze_generate import MazeMap


class MazeSprite(pygame.sprite.Sprite):
    """
    pyGame Sprite subclass that is designed to represent a sprite that is positioned inside the maze
    """
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
        """
        Update our rect top and left coordinates to reflect current location in maze.  This is internal function is
        called from the row and column setters.
        """
        self.rect.top = self._row * 32
        self.rect.left = self._column * 32

    @property
    def column(self):
        """
        Property holding the column where the sprite is positioned in the maze
        """
        return self._column

    @column.setter
    def column(self, value):
        self._column = value
        self._compute_location()

    @property
    def row(self):
        """
        Property holding the row of where the sprite is positioned in the maze
        """
        return self._row

    @row.setter
    def row(self, value):
        self._row = value
        self._compute_location()


