"""This module defines the Solver class, which takes in a list of players and simulates a proof of stake system for a specified number of rounds.
"""

import block
import player
import transaction

import math
import random
import statistics

class Solver:
    N_VALIDATORS = 5  # number of validators
    N_CONNECTIONS = 2 # number of connections for each players
                      # TODO: make gaussian RV centered around 4
    EPS = 1e-6        # epsilon for floating point comparisons
    
    def __init__(self, players, nRounds):
        """Initiates the solver class with the list of players and number of rounds"""
        
        self.players   = players # list of nodes in the system
        self.nRounds   = nRounds # number of "rounds" the system is simulated for
        self.heartbeat = 0       # the heartbeat, or clock, of the system

        self.connectNetwork()

    def connectNetwork(self):
        """Form the network of players through random assignment of connections"""

        for i in range(len(self.players)):
            others = self.players[:i]+self.players[i+1:]
            self.players[i].connections = random.sample(others, self.N_CONNECTIONS)

    def chooseValidators(self):
        """Chooses the validators for the next round based on stake they have in the system"""

        totalStake = self.calcTotalStake()
        coins = [random.randint(1, int(totalStake)) for i in range(self.N_VALIDATORS)]

        validators = []
        
        startCoins = 0 # coin number right before the start of the current player's set of coins
        endCoins = 0 # the player's last coin number
        for i in self.players:
            endCoins += i.stake
            for j in coins:
                if j <= endCoins and j > startCoins:
                    validators.append(i)
            startCoins = endCoins

        return validators
        

    def nextRound(self, heartbeat):
        """Simulates the next round"""

        for i in self.players:
            i.action(heartbeat)
        
        """# collect transactions from all the players
        for i in self.players:
            tx = i.makeTransaction()
            if tx:
                self.txs.append(i.makeTransaction())

        # choose proposer
        proposer = random.choice(self.players)
        proposedBlock = proposer.proposeBlock(self.txs)
        
        # choose validator
        validators = self.chooseValidators()
        votes = [i.validate(proposedBlock) for i in validators]

        winningBlock = max(votes, key=votes.count) # O(n^2), could be optimized

        # if validators chose the winning block, award alpha*totalStake token
        for i, j in zip(validators, votes):
            if j == winningBlock:
                i.stake += 0.01 * self.calcTotalStake()

        # remove txs in winningBlock from tx list
        txs = [i for i in self.txs if i not in winningBlock.txs]
        self.txs = txs

        # add winning block to the beginning of the blockchain
        winningBlock.next = self.blockchain
        self.blockchain = winningBlock"""

    def simulate(self):
        """Simulate the system"""
        
        for i in range(self.nRounds):
            self.nextRound(i)

    def calcPercentStake(self):
        """Calculates the percent stake for each player"""
        
        totalStake = self.calcTotalStake()
        percent = [i.stake/totalStake for i in self.players]

        return percent

    def calcTotalStake(self):
        """Calculates the total stake among all players"""

        return sum([i.stake for i in self.players])
