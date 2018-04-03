"""This module defines the Solver class, which takes in a list of players and simulates a proof of stake system for a specified number of rounds.
"""

import block
import player
import transaction

import random
import statistics

class Solver:
    nValidators = 1
    
    def __init__(self, players, nRounds):
        """Initiates the solver class with the list of players and number of rounds"""
        
        self.players = players # list of nodes in the system
        self.nRounds = nRounds # number of "rounds" the system is simulated for
        self.blockchain = None # the global blockchain
        self.txs = []          # the transaction pool

    def nextRound(self):
        """Simulates the next round by sequentially collecting transactions, running the 
           proposal and validation processes, and adding the block to the blockchain"""
        
        # collect transactions from all the players
        for i in self.players:
            self.txs.append(i.makeTransaction())

        # choose proposer
        proposer = random.choice(self.players)
        proposedBlock = proposer.proposeBlock(self)
        
        # choose validator
        validators = random.choices(self.players, k=self.nValidators)
        votes = [i.validate(proposedBlock) for i in validators]

        winningBlock = statistics.mode(votes)

        # add winning block to the beginning of the blockchain
        winningBlock.next = self.blockchain
        self.blockchain = winningBlock
        

    def simulate(self):
        """Simulate the system"""
        
        for _ in range(self.nRounds):
            self.nextRound()
            

if __name__ == "__main__":
    players = [player.Player() for i in range(10)]
    solver = Solver(players, 2)

    solver.simulate()
    print(solver.blockchain)
    print(solver.txs)
        
