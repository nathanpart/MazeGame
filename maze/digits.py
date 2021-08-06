from typing import List

from pygame.rect import Rect
from pygame.surface import Surface

from maze.config import BACKGROUND_COLOR, DIGIT_WIDTH
from maze.tiles import Tiles, DC_BLUE, DC_YELLOW

BYTE_WIDTH = 3 * DIGIT_WIDTH
WORD_WIDTH = 5 * DIGIT_WIDTH


class Digits:
    is_byte: bool
    digits: Surface
    digit_rects: List[Rect]
    _value: int
    value_list: List[int]
    display: Surface

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value if value >= 0 else 0
        self._value &= 0xFF if self.is_byte else 0xFFFF
        self.value_list = [int(x) for x in list(str(self._value))]

    def __init__(self, tiles: Tiles, color: int, value: int = 0, is_byte: bool = False):
        if DC_BLUE > color > DC_YELLOW:
            raise ValueError("%d is not a valid color index." % color)
        self.digits = tiles.digits[color]
        self.digit_rects = tiles.digit_rects
        self.is_byte = is_byte
        self.value = value

        size = BYTE_WIDTH if self.is_byte else WORD_WIDTH, 32
        self.display = Surface(size)

    def draw(self, surface: Surface, dest_rect: Rect):
        self.display.fill(BACKGROUND_COLOR)

        for idx, digit in enumerate(self.value_list):
            digit_location = 16 * idx
            self.display.blit(self.digits, Rect(digit_location, 0, 16, 32), self.digit_rects[digit])

        surface.blit(self.display, dest_rect)

    # Make ourselves behave like an int
    def __add__(self, other):
        if isinstance(other, Digits):
            return self.value + other.value
        else:
            return self.value + other

    def __sub__(self, other):
        if isinstance(other, Digits):
            return self.value - other.value
        else:
            return self.value - other

    def __mul__(self, other):
        if isinstance(other, Digits):
            return self.value * other.value
        else:
            return self.value * other

    def __truediv__(self, other):
        if isinstance(other, Digits):
            return self.value / other.value
        else:
            return self.value / other

    def __floordiv__(self, other):
        if isinstance(other, Digits):
            return self.value // other.value
        else:
            return self.value // other

    def __mod__(self, other):
        if isinstance(other, Digits):
            return self.value % other.value
        else:
            return self.value % other

    def __divmod__(self, other):
        if isinstance(other, Digits):
            return divmod(self.value, other.value)
        else:
            return divmod(self.value, other)

    def __pow__(self, other):
        if isinstance(other, Digits):
            return self.value ** other.value
        else:
            return self.value ** other

    def __lshift__(self, other):
        if isinstance(other, Digits):
            return self.value << other.value
        else:
            return self.value << other

    def __rshift__(self, other):
        if isinstance(other, Digits):
            return self.value >> other.value
        else:
            return self.value >> other

    def __and__(self, other):
        if isinstance(other, Digits):
            return self.value & other.value
        else:
            return self.value & other

    def __xor__(self, other):
        if isinstance(other, Digits):
            return self.value ^ other.value
        else:
            return self.value ^ other

    def __or__(self, other):
        if isinstance(other, Digits):
            return self.value | other.value
        else:
            return self.value | other

    def __radd__(self, other):
        if isinstance(other, Digits):
            return other.value + self.value
        else:
            return other + self.value

    def __rsub__(self, other):
        if isinstance(other, Digits):
            return other.value - self.value
        else:
            return other - self.value

    def __rmul__(self, other):
        if isinstance(other, Digits):
            return other.value * self.value
        else:
            return other * self.value

    def __rtruediv__(self, other):
        if isinstance(other, Digits):
            return other.value / self.value
        else:
            return other / self.value

    def __rfloordiv__(self, other):
        if isinstance(other, Digits):
            return other.value // self.value
        else:
            return other // self.value

    def __rmod__(self, other):
        if isinstance(other, Digits):
            return other.value % self.value
        else:
            return other % self.value

    def __rdivmod__(self, other):
        if isinstance(other, Digits):
            return divmod(other.value, self.value)
        else:
            return divmod(other, self.value)

    def __rpow__(self, other):
        if isinstance(other, Digits):
            return other.value ** self.value
        else:
            return other ** self.value

    def __rlshift__(self, other):
        if isinstance(other, Digits):
            return other.value << self.value
        else:
            return other << self.value

    def __rrshift__(self, other):
        if isinstance(other, Digits):
            return other.value >> self.value
        else:
            return other >> self.value

    def __rand__(self, other):
        if isinstance(other, Digits):
            return other.value & self.value
        else:
            return other & self.value

    def __rxor__(self, other):
        if isinstance(other, Digits):
            return other.value ^ self.value
        else:
            return other ^ self.value

    def __ror__(self, other):
        if isinstance(other, Digits):
            return other.value | self.value
        else:
            return other | self.value

    def __iadd__(self, other):
        if isinstance(other, Digits):
            self.value += other.value
        else:
            self.value += other
        return self

    def __isub__(self, other):
        if isinstance(other, Digits):
            self.value -= other.value
        else:
            self.value -= other
        return self

    def __imul__(self, other):
        if isinstance(other, Digits):
            self.value *= other.value
        else:
            self.value *= other
        return self

    def __itruediv__(self, other):
        if isinstance(other, Digits):
            self.value /= other.value
        else:
            self.value /= other
        return self

    def __ifloordiv__(self, other):
        if isinstance(other, Digits):
            self.value //= other.value
        else:
            self.value //= other
        return self

    def __imod__(self, other):
        if isinstance(other, Digits):
            self.value %= other.value
        else:
            self.value %= other
        return self

    def __ipow__(self, other):
        if isinstance(other, Digits):
            self.value **= other.value
        else:
            self.value **= other
        return self

    def __ilshift__(self, other):
        if isinstance(other, Digits):
            self.value <<= other.value
        else:
            self.value <<= other
        return self

    def __irshift__(self, other):
        if isinstance(other, Digits):
            self.value >>= other.value
        else:
            self.value >>= other
        return self

    def __iand__(self, other):
        if isinstance(other, Digits):
            self.value &= other.value
        else:
            self.value &= other
        return self

    def __ixor__(self, other):
        if isinstance(other, Digits):
            self.value ^= other.value
        else:
            self.value ^= other
        return self

    def __ior__(self, other):
        if isinstance(other, Digits):
            self.value |= other.value
        else:
            self.value |= other
        return self

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    def __abs__(self):
        return abs(self.value)

    def __invert__(self):
        return ~self.value

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __le__(self, other):
        if isinstance(other, Digits):
            return self.value <= other.value
        else:
            return self.value <= other

    def __lt__(self, other):
        if isinstance(other, Digits):
            return self.value < other.value
        else:
            return self.value < other

    def __ge__(self, other):
        if isinstance(other, Digits):
            return self.value >= other.value
        else:
            return self.value >= other

    def __gt__(self, other):
        if isinstance(other, Digits):
            return self.value > other.value
        else:
            return self.value > other

    def __eq__(self, other):
        if isinstance(other, Digits):
            return self.value == other.value
        else:
            return self.value == other

    def __ne__(self, other):
        if isinstance(other, Digits):
            return self.value != other.value
        else:
            return self.value != other

    def __bool__(self):
        return self.value != 0
