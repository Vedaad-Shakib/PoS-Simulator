import block
import player
import solver
import transaction

import random

def test_blockEquals():
    t = [transaction.Transaction(i, i+1) for i in range(10)]

    a = block.Block(t[:3])
    b = block.Block([t[2], t[1], t[0]])
    c = block.Block(t[-3:])

    assert a == b
    assert a != c
    assert b != c

if __name__ == "__main__":
    blockTestEquals()
