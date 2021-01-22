import sys

import pygame

from maze.generate import Maze


def print_maze():
    tiles = list()
    loc_map = list()
    cur_move = list()
    player_scrolling = False

    col = 1
    row = 1

    def new_maze():
        nonlocal tiles, loc_map, cur_move, player_scrolling, col, row

        maze.generate()

        tiles = list()
        col = 0
        row = 0
        loc_map = list()
        for line in maze.maze_image:
            loc_map.append(list())
            for ch in line:
                if ch == '#':
                    tiles.append((wall, pygame.Rect(col * 10, row * 10, 10, 10)))
                col += 1
                loc_map[row].append(ch)
            col = 0
            row += 1

        tiles.append((maze_exit, exit_rect))

        col = 1
        row = 1
        player_location.left = 10
        player_location.top = 10
        cur_move = moves[0]
        player_scrolling = False

    pygame.init()

    black = 0, 0, 0
    white = 255, 255, 255

    maze = Maze(50, 50)
    width = len(maze.maze_image[0]) * 10
    height = len(maze.maze_image) * 10

    size = width, height
    screen = pygame.display.set_mode(size)

    wall = pygame.surface.Surface((10, 10))
    wall.fill(white)

    maze_exit = pygame.surface.Surface((10, 10))
    maze_exit.fill((255, 0, 0))
    exit_rect = pygame.Rect(width - 20, height - 20, 10, 10)

    player = pygame.surface.Surface((10, 10))
    player.fill((0, 255, 0))
    player_location = player.get_rect()

    moves = [[0, 0], [-2, 0], [0, -2], [2, 0], [0, 2]]

    clock = pygame.time.Clock()

    new_maze()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if not player_scrolling:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if loc_map[row - 1][col] != '#':
                    cur_move = moves[2]
                    player_scrolling = True
                    row -= 1
            elif keys[pygame.K_LEFT]:
                if loc_map[row][col - 1] != '#':
                    cur_move = moves[1]
                    player_scrolling = True
                    col -= 1
            elif keys[pygame.K_RIGHT]:
                if loc_map[row][col + 1] != '#':
                    cur_move = moves[3]
                    player_scrolling = True
                    col += 1
            elif keys[pygame.K_DOWN]:
                if loc_map[row + 1][col] != '#':
                    cur_move = moves[4]
                    player_scrolling = True
                    row += 1

        player_location = player_location.move(cur_move)

        screen.fill(black)
        screen.blits(tiles)
        screen.blit(player, player_location)
        pygame.display.flip()

        if (player_location.left % 10) == 0 and (player_location.top % 10) == 0:
            cur_move = moves[0]
            player_scrolling = False

        if (col * 10 == exit_rect.left) and (row * 10 == exit_rect.top):
            new_maze()

        clock.tick(40)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_maze()
