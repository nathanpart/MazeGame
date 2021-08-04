from typing import List

from pygame import Rect
from pygame.surface import Surface

from maze.cats import Cats
from maze.dog import Dog
from maze.game_state import GameState
from maze.mouse import Mouse
from maze.sprites import ItemGroup
from maze.tiles import Tiles
from maze.maze_generate import MazeGenerator, MazeMap, Point


WINDOW_WIDTH = 320
WINDOW_HEIGHT = 320
WINDOW_WIDTH_CENTER = 160
WINDOW_HEIGHT_CENTER = 160

MAZE_WIDTH_PIXELS = 101 * 32
MAZE_HEIGHT_PIXELS = 101 * 32
MAZE_LEFT_MAX = MAZE_WIDTH_PIXELS - WINDOW_WIDTH
MAZE_TOP_MAX = MAZE_HEIGHT_PIXELS - WINDOW_HEIGHT


class Maze(object):
    maze: Surface
    background: Surface
    wall: Surface
    maze_generator: MazeGenerator
    map: MazeMap

    maze_width: int
    maze_height: int

    tiles: Tiles
    background_color = (156, 102, 47)

    mouse: Mouse
    dog: Dog
    cats: Cats
    cheeses: ItemGroup
    bones: ItemGroup
    game_state: GameState

    rect = Rect(0, 0, 320, 320)
    last_rect: Rect

    def __init__(self, game_state: GameState, mouse: Mouse, cats: Cats, dog: Dog):
        self.maze_width = 101
        self.maze_height = 101

        maze = Surface((self.maze_width * 32, self.maze_height * 32))
        maze.fill(self.background_color)

        self.tiles = Tiles()
        self.wall = self.tiles.wall
        self.background = self.tiles.ground

        self.maze_generator = MazeGenerator(self.maze_width, self.maze_height)
        self.mouse = mouse
        self.cats = cats
        self.dog = dog
        self.game_state = game_state
        self.cheeses = ItemGroup(self.game_state, "eat_cheese", 50, self.map, self.tiles.cheese)
        self.bones = ItemGroup(self.game_state, "collect_bone", 10, self.map, self.tiles.bone)

    def new_maze(self):
        # Generate new maze and render it into the maze surface
        self.maze_generator.generate()
        self.map = self.maze_generator.maze_image

        for row in range(0, self.maze_height):
            for column in range(0, self.maze_width):
                rect = Rect(column * 32, row * 32, 32, 32)
                if self.map.is_wall(column, row) == '#':
                    self.maze.blit(self.wall, rect)
                else:
                    self.maze.blit(self.background, rect)

        # Put player in the upper left corner
        exclude_list: List[Point] = [Point(1, 1)]
        self.mouse.mouse_reset()

        # Add the cheeses, bones, and cats
        self.cheeses.new_game(exclude_list)
        self.bones.new_game(exclude_list)
        self.cats.reset(exclude_list)

    def update(self) -> bool:
        if self.mouse.sprite is None:
            return False  # Out of lives - so game is over
        if self.cheeses.is_empty:
            self.new_maze()  # Level completed

        self.cheeses.update()
        self.bones.update()
        self.dog.update()
        self.cats.update()
        self.mouse.update()
        return True

    def draw(self, surface: Surface, dest_rect: Rect):
        self.cheeses.draw(self.maze)
        self.bones.draw(self.maze)
        self.dog.draw(self.maze)
        self.cats.draw(self.maze)
        self.mouse.draw(self.maze)

        dog_location = self.dog.get_location()
        mouse_location = self.mouse.get_location()

        critter_location = (dog_location if dog_location is not None else
                            (mouse_location if mouse_location is not None else self.last_rect))

        rect = self.rect.copy()
        if critter_location == self.last_rect:
            rect = self.last_rect
        else:
            x = critter_location.centerx - WINDOW_WIDTH_CENTER
            x = max(x, 0)
            x = min(x, MAZE_LEFT_MAX)

            y = critter_location.centery - WINDOW_HEIGHT_CENTER
            y = max(y, 0)
            y = min(y, MAZE_TOP_MAX)

            rect.left = x
            rect.top = y
            self.last_rect = rect

        surface.blit(self.maze, dest_rect, rect)
