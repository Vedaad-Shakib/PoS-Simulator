"""This module defines the Solver class, which takes in a list of players and simulates a proof of stake system for a specified number of rounds.
"""

import block
import player
import transaction

import random
import statistics

class Solver:
    nValidators = 5 # number of validators
    EPS = 1e-6      # epsilon for floating point comparisons
    
    def __init__(self, players, nRounds):
        """Initiates the solver class with the list of players and number of rounds"""
        
        self.players = players # list of nodes in the system
        self.nRounds = nRounds # number of "rounds" the system is simulated for
        self.blockchain = None # the global blockchain
        self.txs = []          # the transaction pool

        totalStake = sum([i.stake for i in players])

        assert totalStake-1 < self.EPS or 1-totalStake < self.EPS, "total stake is %s but needs to equal 1" % (totalStake)

    def nextRound(self):
        """Simulates the next round by sequentially collecting transactions, running the 
           proposal and validation processes, and adding the block to the blockchain"""
        
        # collect transactions from all the players
        for i in self.players:
            self.txs.append(i.makeTransaction())

        # choose proposer
        proposer = random.choice(self.players)
        proposedBlock = proposer.proposeBlock(self.txs)
        
        # choose validator
        validators = random.sample(self.players, self.nValidators)
        votes = [i.validate(proposedBlock) for i in validators]

        winningBlock = max(votes, key=votes.count) # O(n^2), could be optimized

        # remove txs in winningBlock from tx list
        txs = [i for i in self.txs if i not in winningBlock.txs]
        self.txs = txs

        # add winning block to the beginning of the blockchain
        winningBlock.next = self.blockchain
        self.blockchain = winningBlock

    def simulate(self):
        """Simulate the system"""
        
        for _ in range(self.nRounds):
            self.nextRound()
            

if __name__ == "__main__":
    players = [player.Player(0.1) for i in range(10)]
    solver = Solver(players, 3)

    solver.simulate()
    print(solver.blockchain)
    print(solver.txs)
        
