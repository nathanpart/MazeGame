from random import randint


class Maze:
    BOTH_WALLS = 0
    HORIZONTAL_WALL = 1
    VERTICAL_WALL = 2
    NO_WALLS = 3

    wall_map = list()
    mapped_cells = set()
    maze_image = list()

    column = 0
    row = 0
    width = 0
    height = 0
    total_cells = 0

    def __init__(self, width=39, height=12):
        self.width = width
        self.height = height
        self.total_cells = self.width * self.height
        self.generate()

    def render(self):
        self.maze_image = list()
        self.maze_image.append("#" * ((self.width * 2) + 1))
        for row in range(0, self.height):
            row_str1 = '#'
            row_str2 = '#'
            for column in range(0, self.width):
                walls = self.wall_map[column][row]
                row_str1 += " #" if walls == self.BOTH_WALLS or walls == self.VERTICAL_WALL else "  "
                row_str2 += "##" if walls == self.BOTH_WALLS or walls == self.HORIZONTAL_WALL else " #"
            self.maze_image.append(row_str1)
            self.maze_image.append(row_str2)

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
        for row in self.maze_image:
            s += row + '\n'
        return s
