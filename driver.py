"""This file runs the solver for any arbitrary user-defined test case. Meant to be programmed on top of."""

import block
import player
import solver
import transaction

import math
import random
import statistics

def drive(opts):
    """Drive execution of the program. opts: dictionary of options.
       Ex: opts = {"PLAYERS": [(100, 1)], # list of tuples; [(number of players, stake per player)]
            "N_VALIDATORS": 5,            # number of validators in the system
            "N_PROPOSERS": 1,             # number of proposers in the system
            "N_CONNECTIONS": 8,           # number of connections per player
            "N_HEARTBEATS_IN_ROUND": 5,   # number of heartbeats (dt) in a round
            "N_ROUNDS": 5,                # number of rounds of proposal/validation/commit
            "N_TRANSACTIONS": 3,          # number of transactions per block
            "P_TRANSACTIONS": 0.1,        # probability of transaction per player per heartbeat
            "MEAN_PROP_TIME": 0.1         # mean propagation time of messages (exponential distribution)
           }"""

    solver.Solver.N_VALIDATORS          = opts["N_VALIDATORS"]
    solver.Solver.N_PROPOSERS           = opts["N_PROPOSERS"]
    solver.Solver.N_CONNECTIONS         = opts["N_CONNECTIONS"]
    solver.Solver.N_HEARTBEATS_IN_ROUND = opts["N_HEARTBEATS_IN_ROUND"]
    solver.Solver.N_ROUNDS              = opts["N_ROUNDS"]

    player.Player.N_TRANSACTIONS = opts["N_TRANSACTIONS"]
    player.Player.P_TRANSACTIONS = opts["P_TRANSACTIONS"]
    player.Player.MEAN_PROP_TIME = opts["MEAN_PROP_TIME"]

    random.seed(opts["SEED"])

    print("====simulating for %s rounds, %s heartbeats per round====\n"%(opts["N_ROUNDS"], opts["N_HEARTBEATS_IN_ROUND"]))

    sol = solver.Solver(opts)
    
    sol.simulate()

    for i in sol.players:
        print(i)
        print("\t"+str(i.blockchain).replace("\n", "\n\t"))
        print()


    print(sol.blockchain)
