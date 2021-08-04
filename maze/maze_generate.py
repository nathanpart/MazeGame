from functools import total_ordering
from random import randint, randrange
from typing import List, Optional

WEST = 0
NORTH = 1
EAST = 2
SOUTH = 3


@total_ordering
class Point:
    col: int
    row: int

    def __init__(self, col: int, row: int):
        self.col = col
        self.row = row

    def here(self, col: int, row: int) -> bool:
        return self.col == col and self.row == row

    def __eq__(self, other):
        return self.col == other.col and self.row == other.row

    def __gt__(self, other):
        return (self.row == other.row and self.col > other.col) or self.row > other.row


class MazeMap:
    width: int
    height: int
    map: List[List[str]]

    def __init__(self, width: int, height: int):
        self.map = [['.' for _ in range(0, height + 1)] for _ in range(0, width + 1)]

        for x in range(0, width + 1):
            if x == 0 or x == width:
                for y in range(0, height + 1):
                    self.map[x][y] = '#'
                    continue
            self.map[x][0] = '#'
            self.map[x][height] = '#'
        self.width = width
        self.height = height

    def is_wall(self, col: int, row: int) -> bool:
        return self.map[col][row] == '#'

    def passages(self, col: int, row: int, cur_dir: Optional[int] = None) -> List[int]:
        pass_list = list()
        if col - 1 != 0 and not self.is_wall(col - 1, row):
            if cur_dir is None or cur_dir != EAST:
                pass_list.append(WEST)
        if row - 1 != 0 and not self.is_wall(col, row - 1):
            if cur_dir is None or cur_dir != SOUTH:
                pass_list.append(NORTH)
        if col + 1 < self.width and not self.is_wall(col + 1, row):
            if cur_dir is None or cur_dir != WEST:
                pass_list.append(EAST)
        if row + 1 < self.height and not self.is_wall(col, row + 1):
            if cur_dir is None or cur_dir != NORTH:
                pass_list.append(SOUTH)

        # Allow double back if it is the way we came from is the only possible direction
        if len(pass_list) == 0:
            return self.passages(col, row)

        return pass_list

    def get_rand_cell(self) -> Point:
        point = Point(0, 0)
        while self.map[point.col][point.row] == '#':
            point.col = randrange(1, self.width)
            point.row = randrange(1, self.height)
        return point

    def __str__(self) -> str:
        s = ''
        for row in range(0, len(self.map[0])):
            for col in range(0, len(self.map)):
                s += self.map[col][row]
            s += "\n"
        return super().__str__()


class MazeGenerator:
    BOTH_WALLS = 0
    HORIZONTAL_WALL = 1
    VERTICAL_WALL = 2
    NO_WALLS = 3

    wall_map = list()
    mapped_cells = set()

    maze_image: MazeMap

    column = 0
    row = 0
    width = 0
    height = 0
    total_cells = 0

    def __init__(self, width=79, height=13):
        if width % 2 == 0 or height % 2 == 0:
            raise ValueError("The width and height parameters need to be odd.")

        self.maze_image = MazeMap(width - 1, height - 1)
        self.width = (width - 1) // 2
        self.height = (height - 1) // 2
        self.total_cells = self.width * self.height
        self.generate()

    def render(self):
        for row in range(0, self.height):
            for column in range(0, self.width):
                walls = self.wall_map[column][row]
                v_wall = '#' if walls == self.BOTH_WALLS or walls == self.VERTICAL_WALL else ' '
                h_wall = '#' if walls == self.BOTH_WALLS or walls == self.HORIZONTAL_WALL else ' '
                self.maze_image.map[(column * 2) + 1][(row * 2) + 1] = ' '
                self.maze_image.map[(column * 2) + 2][(row * 2) + 1] = v_wall
                self.maze_image.map[(column * 2) + 1][(row * 2) + 2] = h_wall
                self.maze_image.map[(column * 2) + 2][(row * 2) + 2] = '#'

    def generate(self):
        wall_map = list()
        for column in range(0, self.width):
            wall_map.append(list())
            for row in range(0, self.height):
                wall_map[column].append(self.BOTH_WALLS)
        self.wall_map = wall_map

        self.mapped_cells = set()

        self.column = randint(1, self.width - 1)
        self.row = 0
        total = 1
        self.mapped_cells.add((self.column, self.row))

        while total < self.total_cells:
            new_cell_dir = self.pick_cell()
            if new_cell_dir == "left":
                assert self.is_left_open()
                self.column -= 1
                self.wall_map[self.column][self.row] = self.HORIZONTAL_WALL
            elif new_cell_dir == 'up':
                assert self.is_above_open()
                self.row -= 1
                self.wall_map[self.column][self.row] = self.VERTICAL_WALL
            elif new_cell_dir == 'right':
                assert self.is_right_open()
                if self.wall_map[self.column][self.row] == self.BOTH_WALLS:
                    self.wall_map[self.column][self.row] = self.HORIZONTAL_WALL
                else:
                    self.wall_map[self.column][self.row] = self.NO_WALLS
                self.column += 1
            elif new_cell_dir == 'down':
                assert self.is_below_open()
                if self.wall_map[self.column][self.row] == self.BOTH_WALLS:
                    self.wall_map[self.column][self.row] = self.VERTICAL_WALL
                else:
                    self.wall_map[self.column][self.row] = self.NO_WALLS
                self.row += 1
            else:
                assert new_cell_dir == "advance"
                assert not (self.is_below_open() or self.is_right_open() or self.is_above_open() or self.is_left_open())
                do_once = True
                while (self.column, self.row) not in self.mapped_cells or do_once:
                    do_once = False
                    self.column += 1
                    if self.column == self.width:
                        self.column = 0
                        self.row += 1
                        if self.row == self.height:
                            self.row = 0

            if new_cell_dir != "advance":
                total += 1
                self.mapped_cells.add((self.column, self.row))

        self.render()
        return

    def pick_cell(self):
        if self.is_left_open():
            if self.is_above_open():
                if self.is_right_open():
                    return ['left', 'up', 'right'][randint(0, 2)]
                elif self.is_below_open():
                    return ['left', 'up', 'down'][randint(0, 2)]
                else:
                    return ['left', 'up'][randint(0, 1)]
            else:
                if self.is_right_open():
                    if self.is_below_open():
                        return ['left', 'right', 'down'][randint(0, 2)]
                    else:
                        return ['left', 'right'][randint(0, 1)]
                else:
                    if self.is_below_open():
                        return ['left', 'down'][randint(0, 1)]
                    else:
                        return 'left'
        else:
            if self.is_above_open():
                if self.is_right_open():
                    if self.is_below_open():
                        return ['up', 'right', 'down'][randint(0, 2)]
                    else:
                        return ['up', 'right'][randint(0, 1)]
                else:
                    if self.is_below_open():
                        return ['up', 'down'][randint(0, 1)]
                    else:
                        return 'up'
            else:
                if self.is_right_open():
                    if self.is_below_open():
                        return ['right', 'down'][randint(0, 1)]
                    else:
                        return 'right'
                else:
                    if self.is_below_open():
                        return 'down'
                    else:
                        return 'advance'

    def is_left_open(self):
        return (self.column > 0) and (self.column - 1, self.row) not in self.mapped_cells

    def is_above_open(self):
        return (self.row > 0) and (self.column, self.row - 1) not in self.mapped_cells

    def is_right_open(self):
        return (self.column + 1 < self.width) and ((self.column + 1, self.row) not in self.mapped_cells)

    def is_below_open(self):
        return (self.row + 1 < self.height) and ((self.column, self.row + 1) not in self.mapped_cells)

    def __str__(self):
        s = ''

        for row in range(0, len(self.maze_image.map[0])):
            for col in range(0, len(self.maze_image.map)):
                s += self.maze_image.map[col][row]
            s += '\n'
        return s
