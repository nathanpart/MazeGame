import sys
from typing import Tuple, Optional

import pygame
from pygame import Rect, Color
from pygame.surface import Surface
from pygame.time import Clock

from maze.config import BOARD_WIDTH, BOARD_HEIGHT, MAZE_WIDTH, MAZE_HEIGHT, BACKGROUND_COLOR, HEAD_WIDTH, HEAD_HEIGHT
from maze.game_state import GameState
from maze.items import ItemGroup
from maze.maze import Maze
from maze.maze_generate import MazeGenerator, MazeMap, Point
from maze.mouse import Mouse
from maze.tiles import Tiles


class MazeGame:
    play_game: bool
    maze: Maze
    mouse: Optional[Mouse]
    cheese: Optional[ItemGroup]
    bones: Optional[ItemGroup]

    game_state: GameState
    tiles: Tiles
    generator: MazeGenerator
    map: MazeMap
    mouse_tile: Surface
    mouse_recs: Tuple[Rect]

    size = BOARD_WIDTH, BOARD_HEIGHT
    background = Color(156, 102, 47)
    screen: Surface
    clock: Clock

    level: int

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(BACKGROUND_COLOR)
        self.clock = Clock()

        self.tiles = Tiles()

        self.generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        self.maze = Maze(self.tiles)

        self.mouse_tile, *self.mouse_recs = self.tiles.mice
        self.game_state = GameState(self.tiles)

        self.mouse = None
        self.cheese = None
        self.bones = None

        self.level = 0

    def title_screen(self):
        pass

    def new_level(self):
        self.map = self.generator.get_maze()
        self.maze.new_maze(self.map)

        if self.cheese is None:
            self.cheese = ItemGroup(self.game_state, self.map, self.tiles.cheese, 1, 0)
        if self.bones is None:
            self.bones = ItemGroup(self.game_state, self.map, self.tiles.bone, 5, 1)

        exclude_list = [Point(1, 1)]
        self.cheese.new_game(exclude_list, 50)
        self.bones.new_game(exclude_list, 10)

    def game_loop(self):
        self.new_level()
        self.game_state.new_game()

        if self.mouse is None:
            self.mouse = Mouse(self.tiles, self.map)
        else:
            self.mouse.mouse_reset(self.map)

        self.play_game = True
        while self.play_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.mouse.move_up(self.map)
            elif keys[pygame.K_LEFT]:
                self.mouse.move_left(self.map)
            elif keys[pygame.K_RIGHT]:
                self.mouse.move_right(self.map)
            elif keys[pygame.K_DOWN]:
                self.mouse.move_down(self.map)

            # Update mouse - returns False if mouse got ate
            if not self.mouse.update():
                if self.next_mouse():
                    self.mouse.mouse_reset(self.map)
                else:
                    self.play_game = False      # Game Over

            self.cheese.update(self.mouse.sprite)
            self.bones.update(self.mouse.sprite)

            self.screen.fill(BACKGROUND_COLOR)

            self.mouse.draw(self.maze.surface)
            self.cheese.draw(self.maze.surface)
            self.bones.draw(self.maze.surface)

            self.maze.draw(self.screen, Rect(0, 32, 32, 32), None, self.mouse.get_location())
            self.game_state.draw(self.screen, Rect(0, 0, HEAD_WIDTH, HEAD_HEIGHT))

            pygame.display.flip()

            self.clock.tick(40)

    def next_mouse(self):
        self.game_state.lives -= 1
        return self.game_state.lives > 0
