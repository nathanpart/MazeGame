import sys
from typing import List

import pygame

from maze.maze_generate import MazeGenerator, MazeMap
from maze.maze_game import MazeGame as Game


class MazeGame:
    cur_move: List[int]
    player_scrolling: bool
    column: int
    row: int

    tiles: List
    maze_generator: MazeGenerator
    maze: MazeMap

    moves = [[0, 0], [-2, 0], [0, -2], [2, 0], [0, 2]]
    black = 0, 0, 0
    white = 255, 255, 255
    red = 255, 0, 0
    green = 0, 255, 0

    def __init__(self):
        pygame.init()

        self.maze_generator = MazeGenerator(49, 49)
        self.width = len(self.maze_generator.maze_image.map[0]) * 10
        self.height = len(self.maze_generator.maze_image.map) * 10

        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)

        self.wall = pygame.surface.Surface((10, 10))
        self.wall.fill(self.white)

        self.maze_exit = pygame.surface.Surface((10, 10))
        self.maze_exit.fill(self.red)
        self.exit_rect = pygame.Rect(self.width - 20, self.height - 20, 10, 10)

        self.player = pygame.surface.Surface((10, 10))
        self.player.fill(self.green)
        self.player_location = self.player.get_rect()

        self.clock = pygame.time.Clock()

    def new_maze(self):

        self.maze = self.maze_generator.get_maze()

        self.tiles = list()
        for row in range(0, self.maze.height):
            for col in range(0, self.maze.width):
                if self.maze.is_wall(col, row):
                    self.tiles.append((self.wall, pygame.Rect(col * 10, row * 10, 10, 10)))

        self.tiles.append((self.maze_exit, self.exit_rect))

        self.column = 1
        self.row = 1
        self.player_location.left = 10
        self.player_location.top = 10
        self.cur_move = self.moves[0]
        self.player_scrolling = False

    def main_loop(self):
        self.new_maze()
        print()
        print(self.maze_generator)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if not self.player_scrolling:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    if not self.maze.is_wall(self.column, self.row - 1):
                        self.cur_move = self.moves[2]
                        self.player_scrolling = True
                        self.row -= 1
                elif keys[pygame.K_LEFT]:
                    if not self.maze.is_wall(self.column - 1, self.row):
                        self.cur_move = self.moves[1]
                        self.player_scrolling = True
                        self.column -= 1
                elif keys[pygame.K_RIGHT]:
                    if not self.maze.is_wall(self.column + 1, self.row):
                        self.cur_move = self.moves[3]
                        self.player_scrolling = True
                        self.column += 1
                elif keys[pygame.K_DOWN]:
                    if not self.maze.is_wall(self.column, self.row + 1):
                        self.cur_move = self.moves[4]
                        self.player_scrolling = True
                        self.row += 1

            self.player_location = self.player_location.move(self.cur_move)

            self.screen.fill(self.black)
            self.screen.blits(self.tiles)
            self.screen.blit(self.player, self.player_location)
            pygame.display.flip()

            if (self.player_location.left % 10) == 0 and (self.player_location.top % 10) == 0:
                self.cur_move = self.moves[0]
                self.player_scrolling = False

            if (self.column * 10 == self.exit_rect.left) and (self.row * 10 == self.exit_rect.top):
                self.new_maze()

            self.clock.tick(40)


def main():
    Game().game_loop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
