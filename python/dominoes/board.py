import numpy as np

from collections import Iterable
from random import randrange
from itertools import combinations_with_replacement, imap

class DominoError(Exception): pass

class Tile(object):
    """\
    A domino tile.
    """

    def __init__(self, *sides):
        if len(sides) == 1 and isinstance(sides[0], Iterable):
            sides = sides[0]
        print sides
        if len(sides) != 2:
            raise DominoError("A tile can only have 2 sides")
        self.sides = map(int, sides)
        self.weight = sum(self.sides)

    def __eq__(self, rhs):
        if isinstance(rhs, self.__class__):
            rsides = rhs.sides
        elif isinstance(rhs, Iterable) and len(rhs) == 2:
            rsides = rhs
        else:
            raise DominoError("Cannot compare against a non-Tile object")
        return len(set(self.sides).symmetric_difference(rsides)) == 0

    def __lt__(self, rhs):
        if isinstance(rhs, self.__class__):
            return self.weight < rhs.weight
        return self.weight < int(rhs)

    def __add__(self, rhs):
        if isinstance(rhs, self.__class__):
            return self.weight + rhs.weight
        return self.weight + int(rhs)

    def __radd__(self, lhs):
        return self.__add__(lhs)

    def __sub__(self, rhs):
        if isinstance(rhs, self.__class__):
            return self.weight - rhs.weight
        return self.weight - int(rhs)

    def __rsub__(self, lhs):
        if isinstance(lhs, self.__class__):
            return lhs.weight - self.weight
        return int(lhs) - self.weight

    def __contains__(self, side):
        return int(side) in self.sides

    def __repr__(self):
        return "Tile<[{}, {}]>".format(*self.sides)

    def __getitem__(self, idx):
        return self.sides[idx]

    def __setitem__(self, idx, side):
        self.sides[idx] = side

    def __iter__(self):
        return self.sides

    def intersection(self, tile):
        return set(self.sides).intersection(tile.sides)

class Tiles(list):
    """\
    A collection for domino tiles.
    """

    def __init__(self, *tiles, **opts):
        tiles = imap(Tile, tiles)
        if 'auto' in opts and opts['auto']:
            tiles = imap(Tile, combinations_with_replacement(range(0, 7) ,2))
        super(Tiles, self).__init__(tiles)

    def pop_randomly(self, n):
        """Remove random ~n-Tiles form the current set."""
        res = Tiles()
        while n > 0 and len(self) > 0:
            res.append(
                    self.pop(randrange(0, len(self)))
                    )
            n -= 1
        return res

    def matching(self, tile):
        """Return tiles that have a side matching another on the provided tile."""
        return self.__class__(*[x for x in self if x.intersection(tile)])

class Player(Tiles):
    """\
    An object to represent a domino player.
    """

    def __init__(self, *tiles, **opts):
        super(Player, self).__init__(*tiles, **opts)

class Game(object):
    """\
    A dominoes game mixin to provide basic game functions.
    """

    def __init__(self, nplayers=4):
        if 2 < nplayers > 4:
            raise DominoError("Cannot play with less than 2 or more than 4 players")
        self.nplayers = nplayers
        self.odd = True if players % 2 else False
        self._turns = ['player_{}'.format(x) for x in range(0, nplayers)]
        self.new()

    def new(self):
        self.tiles = Tiles(auto=True)
        self.board = Tiles()
        self.stock = Tiles()
        self.players = [Player() for x in range(0, self.nplayers)]
        self.isinprogress = False

    def deal(self):
        if self.isinprogress:
            raise DominoError("Cannot deal twice in a game")
        self.isinprogress = True

        if self.odd: # Remove the null tile if odd number of players
            self.tiles.remove([0, 0])

        shares = len(self.tiles) / self.nplayers
        for player in self.players:
            player.extend(self.tiles.pop_randomly(shares))
        self.stock.extend(self.tiles.pop_randomly(len(self.tiles)))

    def turn(self):
        pass

