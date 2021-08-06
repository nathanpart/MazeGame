import sys
from typing import Tuple, Optional

import pygame
from pygame import Rect, Color
from pygame.surface import Surface
from pygame.time import Clock

from maze.config import BOARD_WIDTH, BOARD_HEIGHT, MAZE_WIDTH, MAZE_HEIGHT, BACKGROUND_COLOR, HEAD_WIDTH, HEAD_HEIGHT
from maze.game_state import GameState
from maze.maze import Maze
from maze.maze_generate import MazeGenerator, MazeMap
from maze.mouse import Mouse
from maze.tiles import Tiles


class MazeGame:
    play_game: bool
    maze: Maze
    mouse: Optional[Mouse]

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

    def title_screen(self):
        pass

    def new_level(self):
        self.map = self.generator.get_maze()
        self.maze.new_maze(self.map)

        # To Do level cheeses, bones, and cats

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

            self.screen.fill(BACKGROUND_COLOR)
            self.mouse.draw(self.maze.surface)
            self.maze.draw(self.screen, Rect(0, 32, 32, 32), None, self.mouse.get_location())
            self.game_state.draw(self.screen, Rect(0, 0, HEAD_WIDTH, HEAD_HEIGHT))

            pygame.display.flip()

            self.clock.tick(40)

    def next_mouse(self):
        return self.game_state.next_life()
