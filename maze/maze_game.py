from typing import Tuple

import pygame
from pygame import Rect, Color
from pygame.surface import Surface
from pygame.time import Clock

from maze.cats import Cats
from maze.dog import Dog
from maze.game_state import GameState
from maze.maze import Maze
from maze.maze_generate import MazeGenerator, NORTH
from maze.mouse import Mouse
from maze.tiles import Tiles


class MazeGame:
    maze: Maze
    cats: Cats
    dog: Dog
    mouse: Mouse

    game_state: GameState
    tiles: Tiles
    generator: MazeGenerator
    mouse_tile: Surface
    mouse_recs: Tuple[Rect]

    size = 320, 352
    background = Color(156, 102, 47)
    screen: Surface
    clock: Clock

    def __init__(self):
        pygame.init()

        background = self.background
        self.tiles = Tiles()
        self.generator = MazeGenerator(101, 101)

        self.mouse_tile, *self.mouse_recs = self.tiles.mice
        self.game_state = GameState(background, self.mouse_tile.subsurface(self.mouse_recs[NORTH]), self.tiles.bone)

        self.mouse = Mouse(self.game_state, self.tiles, self.generator.maze_image)
        self.cats = Cats(self.tiles, self.generator.maze_image, 15, self.mouse)
        self.dog = Dog(self.tiles, self.generator.maze_image, self.mouse, self.cats)

        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(background)
        self.clock = Clock()




