from functools import total_ordering
from random import randint, randrange
from typing import List, Optional

WEST = 0
NORTH = 1
EAST = 2
SOUTH = 3


@total_ordering
class Point:
    """
    Data structure for storing location in the maze
    """
    col: int
    row: int

    def __init__(self, col: int, row: int):
        """
        Create a point instance at

        :param col: The location's column coordinate
        :param row: The location's row coordinate
        """
        self.col = col
        self.row = row

    def here(self, col: int, row: int) -> bool:
        """
        Returns true this point is at the position specified in the parameters

        :param col: column of the location to check
        :param row: row of the location to check
        :return: True if the value in the point is at the location (col, row), else False
        """
        return self.col == col and self.row == row

    def __eq__(self, other):
        return self.col == other.col and self.row == other.row

    def __gt__(self, other):
        return (self.row == other.row and self.col > other.col) or self.row > other.row


class MazeMap:
    """
    Hold the map information of a generated maze. Stored as a python's equivalent of a 2-dimensional array
    (List of Lists) as a list of Column data.  This gives the ability to for the normal x,y index order
    """
    width: int
    height: int
    map: List[List[str]]

    def __init__(self, width: int, height: int):
        """
        Initialize the maze map structure

        :param width: width of the maze
        :param height: hegith of the maze
        """
        self.map = [['.' for _ in range(0, height)] for _ in range(0, width)]

        for x in range(0, width):
            if x == 0 or x == (width - 1):
                for y in range(0, height):
                    self.map[x][y] = '#'
                    continue
            self.map[x][0] = '#'
            self.map[x][height - 1] = '#'
        self.width = width
        self.height = height

    def is_wall(self, col: int, row: int) -> bool:
        """
        Determine is the location is a wall or passage way
        :param col: column of the maze location
        :param row: row of the maze location
        :return: True if the location is a wall, or False if the location is a passage way
        """
        return self.map[col][row] == '#'

    def passages(self, col: int, row: int, cur_dir: Optional[int] = None) -> List[int]:
        """
        Returns  a list of passages available to move from current location

        :param col: Column of the current location
        :param row: Row of the current location
        :param cur_dir: Direction of current direction of travel or None
        :return: List of directions of available passages
        """
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

    def right_hand_rule(self, location: Point, current_direction: int) -> int:
        avail_dirs = self.passages(location.col, location.row)
        if current_direction == EAST:
            if SOUTH in avail_dirs:
                return SOUTH
            if EAST in avail_dirs:
                return EAST
            if NORTH in avail_dirs:
                return NORTH
            return WEST
        elif current_direction == SOUTH:
            if WEST in avail_dirs:
                return WEST
            if SOUTH in avail_dirs:
                return SOUTH
            if EAST in avail_dirs:
                return EAST
            return NORTH
        elif current_direction == WEST:
            if NORTH in avail_dirs:
                return NORTH
            if WEST in avail_dirs:
                return WEST
            if SOUTH in avail_dirs:
                return SOUTH
            return EAST
        else:
            if EAST in avail_dirs:
                return EAST
            if NORTH in avail_dirs:
                return NORTH
            if WEST in avail_dirs:
                return WEST
            return SOUTH

    def get_rand_cell(self) -> Point:
        """
        Get a random location in the maze that is not a wall

        :return: Point containing the random location
        """
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
    _width = 0
    _height = 0
    total_cells = 0

    @property
    def width(self):
        return (self._width * 2) + 1

    @width.setter
    def width(self, w):
        self._width = (w - 1) // 2

    @property
    def height(self):
        return (self._height * 2) + 1

    @height.setter
    def height(self, h):
        self._height = (h - 1) // 2

    def __init__(self, width=79, height=13):
        """
        Initialize a new maze generator

        :param width: Width of the mazes to be generated
        :param height: Height of the mazes to be generated
        """
        if width % 2 == 0 or height % 2 == 0:
            raise ValueError("The width and height parameters need to be odd.")

        self.maze_image = MazeMap(width, height)
        self.width = width
        self.height = height
        self.total_cells = self._width * self._height

    def _render(self):
        """
        Render the maze that generated into a MazeMap
        """
        for row in range(0, self._height):
            for column in range(0, self._width):
                walls = self.wall_map[column][row]
                v_wall = '#' if walls == self.BOTH_WALLS or walls == self.VERTICAL_WALL else ' '
                h_wall = '#' if walls == self.BOTH_WALLS or walls == self.HORIZONTAL_WALL else ' '
                self.maze_image.map[(column * 2) + 1][(row * 2) + 1] = ' '
                self.maze_image.map[(column * 2) + 2][(row * 2) + 1] = v_wall
                self.maze_image.map[(column * 2) + 1][(row * 2) + 2] = h_wall
                self.maze_image.map[(column * 2) + 2][(row * 2) + 2] = '#'

    def _generate(self):
        """
        Generate the maze by determining walls and passages
        """
        wall_map = list()
        for column in range(0, self._width):
            wall_map.append(list())
            for row in range(0, self._height):
                wall_map[column].append(self.BOTH_WALLS)
        self.wall_map = wall_map

        self.mapped_cells = set()

        self.column = randint(1, self._width - 1)
        self.row = 0
        total = 1
        self.mapped_cells.add((self.column, self.row))

        while total < self.total_cells:
            new_cell_dir = self._pick_cell()
            if new_cell_dir == "left":
                assert self._is_left_open()
                self.column -= 1
                self.wall_map[self.column][self.row] = self.HORIZONTAL_WALL
            elif new_cell_dir == 'up':
                assert self._is_above_open()
                self.row -= 1
                self.wall_map[self.column][self.row] = self.VERTICAL_WALL
            elif new_cell_dir == 'right':
                assert self._is_right_open()
                if self.wall_map[self.column][self.row] == self.BOTH_WALLS:
                    self.wall_map[self.column][self.row] = self.HORIZONTAL_WALL
                else:
                    self.wall_map[self.column][self.row] = self.NO_WALLS
                self.column += 1
            elif new_cell_dir == 'down':
                assert self._is_below_open()
                if self.wall_map[self.column][self.row] == self.BOTH_WALLS:
                    self.wall_map[self.column][self.row] = self.VERTICAL_WALL
                else:
                    self.wall_map[self.column][self.row] = self.NO_WALLS
                self.row += 1
            else:
                assert new_cell_dir == "advance"
                assert not (self._is_below_open() or self._is_right_open() or
                            (self._is_above_open() or self._is_left_open()))
                do_once = True
                while (self.column, self.row) not in self.mapped_cells or do_once:
                    do_once = False
                    self.column += 1
                    if self.column == self._width:
                        self.column = 0
                        self.row += 1
                        if self.row == self._height:
                            self.row = 0

            if new_cell_dir != "advance":
                total += 1
                self.mapped_cells.add((self.column, self.row))
        return

    def _pick_cell(self):
        """
        Pick a available surrounding cell and move to it marking the passage to it as a passage
        """
        if self._is_left_open():
            if self._is_above_open():
                if self._is_right_open():
                    return ['left', 'up', 'right'][randint(0, 2)]
                elif self._is_below_open():
                    return ['left', 'up', 'down'][randint(0, 2)]
                else:
                    return ['left', 'up'][randint(0, 1)]
            else:
                if self._is_right_open():
                    if self._is_below_open():
                        return ['left', 'right', 'down'][randint(0, 2)]
                    else:
                        return ['left', 'right'][randint(0, 1)]
                else:
                    if self._is_below_open():
                        return ['left', 'down'][randint(0, 1)]
                    else:
                        return 'left'
        else:
            if self._is_above_open():
                if self._is_right_open():
                    if self._is_below_open():
                        return ['up', 'right', 'down'][randint(0, 2)]
                    else:
                        return ['up', 'right'][randint(0, 1)]
                else:
                    if self._is_below_open():
                        return ['up', 'down'][randint(0, 1)]
                    else:
                        return 'up'
            else:
                if self._is_right_open():
                    if self._is_below_open():
                        return ['right', 'down'][randint(0, 1)]
                    else:
                        return 'right'
                else:
                    if self._is_below_open():
                        return 'down'
                    else:
                        return 'advance'

    def _is_left_open(self):
        """
        Is the cell to the left available to be added to the maze?

        :return: True is available, or False
        """
        return (self.column > 0) and (self.column - 1, self.row) not in self.mapped_cells

    def _is_above_open(self):
        """
        Is the cell above available to be added to the maze?

        :return: True is available, or False
        """
        return (self.row > 0) and (self.column, self.row - 1) not in self.mapped_cells

    def _is_right_open(self):
        """
        Is the cell to the right available to be added to the maze?

        :return: True is available, or False
        """
        return (self.column + 1 < self._width) and ((self.column + 1, self.row) not in self.mapped_cells)

    def _is_below_open(self):
        """
        Is the cell below available to be added to the maze?

        :return: True is available, or False
        """
        return (self.row + 1 < self._height) and ((self.column, self.row + 1) not in self.mapped_cells)

    def get_maze(self) -> MazeMap:
        """
        Get a new random generated maze

        :return: MazeMap of the generated maze
        """
        self._generate()
        self._render()
        return self.maze_image

    def __str__(self):
        """
        Dump the maze into a string
        """
        s = ''

        for row in range(0, len(self.maze_image.map[0])):
            for col in range(0, len(self.maze_image.map)):
                s += self.maze_image.map[col][row]
            s += '\n'
        return s
