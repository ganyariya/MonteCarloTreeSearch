from __future__ import annotations
from random import choice
from monte_carlo_tree_search.istate import IState
from typing import List, Optional, Final

LENGTH: Final[int] = 3
HEIGHT: Final[int] = 3
WIDTH: Final[int] = 3


class State(IState):
    def __init__(self, pieces: Optional[List[int]] = None, enemy_pieces: Optional[List[int]] = None):
        self.pieces: Optional[List[int]] = pieces if pieces is not None else [0] * (HEIGHT * WIDTH)
        self.enemy_pieces: Optional[List[int]] = enemy_pieces if enemy_pieces is not None else [0] * (HEIGHT * WIDTH)

    def next(self, action: int) -> State:
        pieces = self.pieces.copy()
        pieces[action] = 1
        return State(self.enemy_pieces, pieces)

    def legal_actions(self) -> List[int]:
        return [i for i in range(HEIGHT * WIDTH) if self.pieces[i] == 0 and self.enemy_pieces[i] == 0]

    def random_action(self) -> int:
        return choice(self.legal_actions())

    @staticmethod
    def pieces_count(pieces: List[int]) -> int:
        return pieces.count(1)

    def is_lose(self) -> bool:
        dy = [0, 1, 1, -1]
        dx = [1, 0, 1, -1]

        for y in range(HEIGHT):
            for x in range(WIDTH):
                for k in range(4):
                    lose = True
                    ny, nx = y, x
                    for i in range(LENGTH):
                        if ny < 0 or ny >= HEIGHT or nx < 0 or nx >= WIDTH:
                            lose = False
                            break
                        if self.enemy_pieces[ny * WIDTH + nx] == 0:
                            lose = False
                            break
                        ny += dy[k]
                        nx += dx[k]
                    if lose:
                        return True

        return False

    def is_draw(self) -> bool:
        return self.pieces_count(self.pieces) + self.pieces_count(self.enemy_pieces) == HEIGHT * WIDTH

    def is_done(self) -> bool:
        return self.is_lose() or self.is_draw()

    def is_first_player(self) -> bool:
        return self.pieces_count(self.pieces) == self.pieces_count(self.enemy_pieces)

    def __str__(self) -> str:
        ox = ('o', 'x') if self.is_first_player() else ('x', 'o')
        ret = ""
        for i in range(HEIGHT * WIDTH):
            if self.pieces[i] == 1:
                ret += ox[0]
            elif self.enemy_pieces[i] == 1:
                ret += ox[1]
            else:
                ret += '-'
            if i % WIDTH == WIDTH - 1:
                ret += '\n'
        return ret
