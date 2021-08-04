from pygame import Color, Surface
from pygame.font import Font
from pygame.sprite import Sprite, Group


class Score(Sprite):
    """ to keep track of the score.
    """
    score: int
    last_score: int
    background: Color

    def __init__(self, background: Color):
        Sprite.__init__(self)
        self.font = Font(None, 20)
        self.font.set_italic(1)
        self.color = Color("white")
        self.background = background
        self.score = 0
        self.last_score = -1
        self.update()

    def update(self):
        """ We only update the score in update() when it has changed.
        """
        if self.score != self.last_score:
            self.last_score = self.score
            msg = "Score: %d" % self.score
            self.image = self.font.render(msg, 0, self.color, self.background)
            self.rect = self.image.get_rect().move(10, 6)


class Items(Sprite):
    count: int
    last_count: int
    background: Color
    font: Font

    def __init__(self, background: Color, tile: Surface):
        super(Items, self).__init__()
        self.count = 0
        self.last_count = -1
        self.image = Surface((64, 32))
        self.rect = self.image.get_rect()
        self.image.fill(background)
        self.image.blit(tile, (0, 0))

        self.background = background
        self.color = Color("white")
        self.font = Font(None, 20)
        self.font.set_italic(1)
        self.update()

    def update(self, *args, **kwargs) -> None:
        if self.count != self.last_count:
            self.last_count = self.count
            msg = "%d" % self.count
            msg_surface = self.font.render(msg, 0, self.color, self.background)
            msg_rect = msg_surface.get_rect().move(38, 6)
            self.image.blit(msg_surface, msg_rect)


class GameState(object):
    lives: Items
    bones: Items
    score: Score
    heading_group: Group

    def __init__(self, background: Color, mouse_tile: Surface, bone_tile: Surface):
        self.score = Score(background)
        self.lives = Items(background, mouse_tile)
        self.bones = Items(background, bone_tile)
        self.heading_group = Group(self.score, self.lives, self.bones)

    def new_game(self):
        self.score.score = 0
        self.lives.count = 3
        self.bones.count = 0

    def eat_cheese(self):
        self.score.score += 1

    def collect_bone(self):
        self.bones.count += 1
        self.score.score += 5

    def cat_got_ate(self):
        self.score.score += 10

    def deployed_dog(self) -> bool:
        if self.bones.count == 0:
            return False
        self.bones.count -= 1
        return True

    def next_life(self) -> bool:
        if self.lives.count == 0:
            return False
        self.lives.count -= 1
        return True

    def update(self):
        self.heading_group.update()

    def draw(self, surface: Surface):
        self.heading_group.draw(surface)
