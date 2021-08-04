
# Size of the maze
MAZE_WIDTH = 101
MAZE_HEIGHT = 101

# Size of a tile
TILE_WIDTH = 32
TILE_HEIGHT = 32

# Size of the game play area
PLAY_WIDTH = 10 * TILE_WIDTH
PLAY_HEIGHT = 10 * TILE_HEIGHT

# Size of the score/state area
HEAD_WIDTH = 10 * TILE_WIDTH
HEAD_HEIGHT = TILE_HEIGHT

# Size of the game window
BOARD_WIDTH = PLAY_WIDTH
BOARD_HEIGHT = PLAY_HEIGHT + HEAD_HEIGHT

SURFACE_WIDTH = TILE_WIDTH * MAZE_WIDTH
SURFACE_HEIGHT = TILE_HEIGHT * MAZE_HEIGHT

WINDOW_RIGHT_MAX = SURFACE_WIDTH - TILE_WIDTH
WINDOW_BOTTOM_MAX = SURFACE_HEIGHT - TILE_HEIGHT
WIDTH_CENTER = SURFACE_WIDTH // 2
HEIGHT_CENTER = SURFACE_HEIGHT // 2


BACKGROUND_COLOR = (156, 102, 47)