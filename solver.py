"""This module defines the Solver class, which takes in a list of players and simulates a proof of stake system for a specified number of rounds.
"""

import block
import player
import transaction

import math
import random
import statistics

class Solver:
    EPS = 1e-6 # epsilon for floating point comparisons
    
    def __init__(self, opts):
        """Initiates the solver class with the list of players and number of rounds"""

        self.players = []                                                 # the list of nodes in the system
        for nPlayers, stake in opts["PLAYERS"]:
            self.players.extend([player.Player(stake) for i in range(nPlayers)])
            
        self.nHeartbeats = opts["N_ROUNDS"]*Solver.N_HEARTBEATS_IN_ROUND # number of total heartbeats
        self.heartbeat   = 0                                              # the heartbeat, or clock, of the system

        # add pointer to solver to players
        for i in self.players:
            i.solver = self
            
        self.connectNetwork()

    def connectNetwork(self):
        """Form the network of players through random assignment of connections"""

        for i in range(len(self.players)):
            others = self.players[:i]+self.players[i+1:]
            self.players[i].connections = random.sample(others, self.N_CONNECTIONS)

    def chooseProposers(self):
        """Choose proposer for next round; chance of being chosen proportional to stake"""

        totalStake = self.calcTotalStake()
        coins = random.sample(list(range(1, totalStake+1)), self.N_PROPOSERS) 

        proposers = []
        
        startCoins = 0 # coin number right before the start of the current player's set of coins
        endCoins = 0 # the player's last coin number
        for i in self.players:
            endCoins += i.stake
            for j in coins:
                if j <= endCoins and j > startCoins:
                    proposers.append(i)
            startCoins = endCoins

        proposers = [i.id for i in proposers]
        
        return proposers

    def chooseValidators(self):
        """Chooses the validators for the next round based on stake they have in the system"""

        totalStake = self.calcTotalStake()
        coins = random.sample(list(range(1, totalStake+1)), self.N_VALIDATORS) 

        validators = []
        
        startCoins = 0 # coin number right before the start of the current player's set of coins
        endCoins = 0 # the player's last coin number
        for i in self.players:
            endCoins += i.stake
            for j in coins:
                if j <= endCoins and j > startCoins:
                    validators.append(i)
            startCoins = endCoins

        validators = [i.id for i in validators]
        
        return validators

    def nextRound(self, heartbeat):
        """Simulates the next round"""

        #print("heartbeat:", heartbeat)
        t="\t"
        
        # if start of round, reset validator, proposer set
        if heartbeat % Solver.N_HEARTBEATS_IN_ROUND == 0:
            self.valSet  = self.chooseValidators() # choose validator set
            self.propSet = self.chooseProposers()  # choose proposer set
            #print(t, "assign new valSet:", self.valSet)
            #print(t, "assign new propSet:", self.propSet)
            #print()
        
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

        # if validators chose the winning block, award 1 token
        for i, j in zip(validators, votes):
            if j == winningBlock:
                i.stake += 1

        # remove txs in winningBlock from tx list
        txs = [i for i in self.txs if i not in winningBlock.txs]
        self.txs = txs

        # add winning block to the beginning of the blockchain
        winningBlock.next = self.blockchain
        self.blockchain = winningBlock"""

    def simulate(self):
        """Simulate the system"""
        
        for i in range(self.nHeartbeats):
            self.nextRound(i)

    def calcPercentStake(self):
        """Calculates the percent stake for each player"""
        
        totalStake = self.calcTotalStake()
        percent = [i.stake/totalStake for i in self.players]

        return percent

    def calcTotalStake(self):
        """Calculates the total stake among all players"""

        return sum([i.stake for i in self.players])
