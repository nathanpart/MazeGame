from typing import List

from pygame import Rect
from pygame.surface import Surface

from maze.Tiles import Tiles
from maze.mazegenerate import MazeGenerator


class MazeGame:
    maze: Surface
    background: Surface
    wall: Surface
    maze_generator: MazeGenerator
    map: List[List[str]]
    maze_width: int
    maze_height: int

    tiles: Tiles
    background_color = (156, 102, 47)

    def __init__(self):
        self.maze_width = 101
        self.maze_height = 101

        maze = Surface((self.maze_width * 32, self.maze_height * 32))
        maze.fill(self.background_color)

        self.tiles = Tiles()
        self.wall = self.tiles.wall
        self.background = self.tiles.ground

        self.maze_generator = MazeGenerator(self.maze_width, self.maze_height)

    def new_maze(self):
        self.maze_generator.generate()
        self.map = self.maze_generator.maze_image

        for row in range(0, self.maze_height):
            for column in range(0, self.maze_width):
                rect = Rect(column * 32, row * 32, 32, 32)
                if self.map[column][row] == '#':
                    self.maze.blit(self.wall, rect)
                else:
                    self.maze.blit(self.background, rect)






