import pytest

class Movement(object):
    def simple_move(self):
        x = 'test'
        assert 'test' in x

mov = Movement()
mov.simple_move()