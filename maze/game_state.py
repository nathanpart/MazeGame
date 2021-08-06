from pygame import Surface
from pygame.rect import Rect

from maze.config import HEAD_WIDTH, HEAD_HEIGHT, DIGIT_WIDTH, BACKGROUND_COLOR
from maze.digits import Digits, BYTE_WIDTH, WORD_WIDTH
from maze.maze_generate import NORTH
from maze.tiles import Tiles, DC_CYAN, DC_YELLOW, DC_WHITE

LIVES_POS = HEAD_WIDTH - (4 * DIGIT_WIDTH)
BONES_POS = HEAD_WIDTH - (11 * DIGIT_WIDTH)
SCORE_POS = DIGIT_WIDTH

LIVES_ICON_POS = HEAD_WIDTH - (6 * DIGIT_WIDTH)
BONES_ICON_POS = HEAD_WIDTH - (13 * DIGIT_WIDTH)


class GameState(object):
    lives: Digits
    bones: Digits
    score: Digits

    lives_icon: Surface
    bones_icon: Surface

    display: Surface
    lives_rect = Rect(LIVES_POS, 0, BYTE_WIDTH, 32)
    bones_rect = Rect(BONES_POS, 0, BYTE_WIDTH, 32)
    score_rect = Rect(SCORE_POS, 0, WORD_WIDTH, 32)

    lives_icon_rect = Rect(LIVES_ICON_POS, 0, 32, 32)
    bones_icon_rect = Rect(BONES_ICON_POS, 0, 32, 32)

    def __init__(self, tiles: Tiles):
        self.score = Digits(tiles, DC_CYAN)
        self.lives = Digits(tiles, DC_YELLOW, is_byte=True)
        self.bones = Digits(tiles, DC_WHITE, is_byte=True)

        self.display = Surface((HEAD_WIDTH, HEAD_HEIGHT))

        mice, *mice_rects = tiles.mice
        self.lives_icon = mice.subsurface(mice_rects[NORTH])
        self.bones_icon = tiles.bone

    def new_game(self):
        self.score.value = 0
        self.lives.value = 3
        self.bones.value = 0

    def eat_cheese(self):
        self.score += 1

    def collect_bone(self):
        self.bones += 1
        self.score += 5

    def cat_got_ate(self):
        self.score += 10

    def deployed_dog(self) -> bool:
        if self.bones == 0:
            return False
        self.bones -= 1
        return True

    def next_life(self) -> bool:
        if self.lives == 0:
            return False
        self.lives -= 1
        return True

    def draw(self, surface: Surface, dest_rect: Rect):
        self.display.fill(BACKGROUND_COLOR)
        self.score.draw(self.display, self.score_rect)
        self.display.blit(self.bones_icon, self.bones_icon_rect)
        self.bones.draw(self.display, self.bones_rect)
        self.display.blit(self.lives_icon, self.lives_icon_rect)
        self.lives.draw(self.display, self.lives_rect)

        surface.blit(self.display, dest_rect)

