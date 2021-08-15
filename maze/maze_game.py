import sys
from typing import Tuple, Optional, List

import pygame
from pygame import Rect, Color
from pygame.surface import Surface
from pygame.time import Clock

from maze.cats import Cats
from maze.config import BOARD_WIDTH, BOARD_HEIGHT, MAZE_WIDTH, MAZE_HEIGHT, BACKGROUND_COLOR, HEAD_WIDTH, HEAD_HEIGHT
from maze.critters import CritterGroup
from maze.dog import DogBlew, Dog
from maze.game_state import GameState
from maze.items import ItemGroup
from maze.maze import Maze
from maze.maze_generate import MazeGenerator, MazeMap, Point
from maze.mouse import TheMouse, Mouse
from maze.tiles import Tiles


class MazeGame:
    play_game: bool
    maze: Maze
    mouse: Optional[Mouse]
    dog: Optional[Dog]
    cats: Optional[Cats]
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
    is_dog: bool
    clear_tiles: List[Rect]

    def __init__(self):
        pygame.init()

        self.is_dog = False
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(BACKGROUND_COLOR)
        self.clock = Clock()

        self.tiles = Tiles()

        self.generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        self.maze = Maze(self.tiles)

        self.mouse_tile, *self.mouse_recs = self.tiles.mice
        self.game_state = GameState(self.tiles)

        self.clear_tiles = list()
        self.mouse = None
        self.cats = None
        self.dog = None
        self.cheese = None
        self.bones = None

        self.level = 0

    def title_screen(self):
        pass

    def new_level(self):
        self.level += 1
        self.map = self.generator.get_maze()
        self.maze.new_maze(self.map)

        if self.mouse is None:
            self.mouse = Mouse(self.map, self.tiles.mice, TheMouse)
        else:
            self.mouse.critter_reset(self.map)

        if self.cheese is None:
            self.cheese = ItemGroup(self.game_state, self.map, self.tiles.cheese, 1, 0)
        if self.bones is None:
            self.bones = ItemGroup(self.game_state, self.map, self.tiles.bone, 5, 1)
        if self.cats is None:
            self.cats = Cats(self.tiles, self.map, self.mouse)

        exclude_list = [Point(1, 1)]
        self.cheese.new_game(exclude_list, 50)
        self.bones.new_game(exclude_list, 6 + (4 * self.level))
        self.cats.reset(exclude_list, 5 + (5 * self.level))
        self.level = 0

    def title_loop(self):
        return True

    def game_over_loop(self):
        pass

    def game_loop(self):
        self.new_level()
        self.game_state.new_game()
        dog_counter = 0
        flash_counter = 0
        self.play_game = True
        while self.play_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if self.is_dog:
                dog_counter -= 1
                if dog_counter <= 0:
                    self.mouse.exit_dog(*self.dog.deactivate())

            keys = pygame.key.get_pressed()
            if self.is_dog:
                if keys[pygame.K_UP]:
                    self.mouse.move_up(self.map)
                elif keys[pygame.K_LEFT]:
                    self.mouse.move_left(self.map)
                elif keys[pygame.K_RIGHT]:
                    self.mouse.move_right(self.map)
                elif keys[pygame.K_DOWN]:
                    self.mouse.move_down(self.map)
            else:
                if keys[pygame.K_UP]:
                    self.mouse.move_up(self.map)
                elif keys[pygame.K_LEFT]:
                    self.mouse.move_left(self.map)
                elif keys[pygame.K_RIGHT]:
                    self.mouse.move_right(self.map)
                elif keys[pygame.K_DOWN]:
                    self.mouse.move_down(self.map)
                elif keys[pygame.K_SPACE]:
                    if self.game_state.bones > 0:
                        self.activate_dog()

            # Update mouse - returns False if mouse got ate

            self.update()
            self.screen.fill(BACKGROUND_COLOR)
            self.clear_critter_tiles()
            self.draw()

            pygame.display.flip()
            self.clock.tick(40)

            if len(self.cheese) == 0:
                self.new_level()
                self.game_state.bones.value = 0

    def update(self):
        self.clear_tiles.clear()
        if self.is_dog:
            try:
                self.dog.update(self.clear_tiles)
            except DogBlew:
                # Pop the dog - switch back to mouse and lose a life
                self.is_dog = False
                self.mouse.sprite.kill()
        else:
            if not self.mouse.update(self.clear_tiles):
                if self.next_mouse():
                    self.mouse.critter_reset(self.map)
                else:
                    self.play_game = False  # Game Over
        self.cheese.update(self.mouse.sprite)
        self.bones.update(self.mouse.sprite)
        self.cats.update(self.clear_tiles)

    def clear_critter_tiles(self):
        for tile in self.clear_tiles:
            self.maze.surface.blit(self.tiles.ground, tile)

    def draw(self):
        self.cheese.draw(self.maze.surface)
        self.bones.draw(self.maze.surface)
        self.mouse.draw(self.maze.surface)
        self.cats.draw(self.maze.surface)
        self.maze.draw(self.screen, Rect(0, 32, 32, 32), self.mouse.get_location())
        self.game_state.draw(self.screen, Rect(0, 0, HEAD_WIDTH, HEAD_HEIGHT))

    def maze_run(self):
        while self.title_loop():
            self.game_loop()
            self.game_over_loop()

    def next_mouse(self):
        self.game_state.lives -= 1
        return self.game_state.lives > 0

    def activate_dog(self):
        pass
