"""This file runs the solver for any arbitrary user-defined test case.
"""

import block
import player
import solver
import transaction

import math
import random
import statistics

players = [player.Player(1) for i in range(100)]
solver = solver.Solver(players, 40)

"""for i in solver.players:
    print(i, ":", i.connections)"""
        
solver.simulate()

print(solver.players[0])
print(solver.players[0].blockchain)

