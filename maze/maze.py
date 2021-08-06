from typing import Union

from pygame import Rect
from pygame.surface import Surface

from maze.config import BACKGROUND_COLOR, PLAY_WIDTH, PLAY_HEIGHT, MAZE_HEIGHT, MAZE_WIDTH, SURFACE_WIDTH, \
    SURFACE_HEIGHT, RIGHT_SCROLL_LIM, \
    LEFT_SCROLL_LIM, MID_PLAY_WIDTH, BOT_SCROLL_LIM, TOP_SCROLL_LIM, MID_PLAY_HEIGHT
from maze.maze_generate import MazeGenerator, MazeMap
from maze.tiles import Tiles


class Maze(object):
    surface: Surface
    background: Surface
    wall: Surface
    maze_generator: MazeGenerator
    map: MazeMap

    maze_width: int
    maze_height: int

    tiles: Tiles
    background_color = BACKGROUND_COLOR

    rect = Rect(0, 0, PLAY_WIDTH, PLAY_HEIGHT)
    last_rect: Rect

    def __init__(self, tiles: Tiles):
        self.maze_width = MAZE_WIDTH
        self.maze_height = MAZE_HEIGHT

        self.surface = Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
        self.surface.fill(self.background_color)

        self.tiles = tiles
        self.wall = self.tiles.wall
        self.background = self.tiles.ground
        self.last_rect = Rect(0, 0, 0, 0)

    def new_maze(self, maze: MazeMap):
        # Generate new maze and render it into the maze surface
        self.map = maze

        for row in range(0, MAZE_HEIGHT):
            for column in range(0, MAZE_WIDTH):
                rect = Rect(column * 32, row * 32, 32, 32)
                if self.map.is_wall(column, row):
                    self.surface.blit(self.wall, rect)
                else:
                    self.surface.blit(self.background, rect)

    def update(self) -> bool:
        pass

    def draw(self, surface: Surface, dest_rect: Rect,
             dog_location: Union[Rect, None], mouse_location: Union[Rect, None]):

        critter_location = (dog_location if dog_location is not None else
                            (mouse_location if mouse_location is not None else self.last_rect))

        rect = self.rect.copy()
        if RIGHT_SCROLL_LIM > critter_location.left > LEFT_SCROLL_LIM:
            rect.left = critter_location.left - LEFT_SCROLL_LIM
        elif critter_location.left < MID_PLAY_WIDTH:
            rect.left = 0
        else:
            rect.left = RIGHT_SCROLL_LIM - MID_PLAY_WIDTH

        if BOT_SCROLL_LIM > critter_location.top > TOP_SCROLL_LIM:
            rect.top = critter_location.top - TOP_SCROLL_LIM
        elif critter_location.top < MID_PLAY_HEIGHT:
            rect.top = 0
        else:
            rect.top = BOT_SCROLL_LIM - MID_PLAY_HEIGHT

        surface.blit(self.surface, dest_rect, rect)
