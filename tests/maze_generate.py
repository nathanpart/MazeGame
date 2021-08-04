import unittest

from maze.maze_generate import MazeGenerator, MazeMap


class MyTestCase(unittest.TestCase):

    def test_maze_map(self):
        maze = MazeMap(10, 5)
        self.assertEqual(10, len(maze.map))
        self.assertEqual(5, len(maze.map[0]))

    def test_something(self):
        maze_image = MazeGenerator()

        self.assertEqual(True, isinstance(maze_image.maze_image, MazeMap))  # add assertion here


if __name__ == '__main__':
    unittest.main()
