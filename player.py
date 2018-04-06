"""This module defines the Player class, which represents a player in the network and contains functionality to make transactions, propose blocks, and validate blocks.
"""

import block
import transaction

import random
import numpy as np

class Player:
    N_TRANSACTIONS = 3    # number of transactions included in a block
    P_TRANSACTIONS = 0.1  # probability of making a transaction at heartbeat r
    MEAN_PROP_TIME = 0.01 # mean propagation time
    
    id = 0                # player id
    
    def __init__(self, stake, connections=[]):
        """Creates a new Player object"""

        self.id = Player.id            # the player's id
        Player.id += 1                 

        self.stake = stake             # the number of tokens the player has staked in the system

        self.connections = connections # list of connected players
        self.inbound     = []          # inbound messages from other players in the network at heartbeat r
        self.outbound    = []          # outbounde messages to other players in the network at heartbeat r

        self.blockchain = None  # the current state of the player's blockchain
        self.mempool    = set() # the current list of txs the player knows about
        self.seen       = set() # set of seen txs

    def action(self, heartbeat):
        """Executes the player's actions for heartbeat r"""

        for message, timestamp in self.inbound:
            # don't have access to messages which arrive after the current heartbeat r
            if timestamp > heartbeat:
                continue
            
            # if inbound message is transaction, add to local mempool
            if type(message) == transaction.Transaction:
                self.mempool.add(message)
                if message not in self.seen:
                    self.seen.add(message)
                    self.outbound.append([message, timestamp])

        self.inbound = list(filter(lambda x: x[1] > heartbeat, self.inbound)) # get rid of already-processed messages
                
        # make transaction with probability p
        if random.random() < self.P_TRANSACTIONS:
            tx = self.makeTransaction()
            self.outbound.append([tx, heartbeat])
            self.mempool.add(tx)


        self.sendOutbound()

    def sendOutbound(self):
        """Send all outbound connections to connected nodes"""
        
        for i in self.connections:
            for message, timestamp in self.outbound:
                dt = np.random.exponential(self.MEAN_PROP_TIME) # add propagation time to timestamp
                i.inbound.append([message, timestamp+dt])

        self.outbound.clear()

    def makeTransaction(self):
        """Returns a random transaction"""

        return transaction.Transaction(self.id, 1)

    def proposeBlock(self, txs):
        """Proposes a Block consisting of multiple random transactions"""
        
        pickedTx = random.sample(txs, self.nTransactions)

        return block.Block(pickedTx)

    
    def validate(self, uBlock):
        """Validates a block"""

        return uBlock

    def __str__(self):
        return "player %s" % (self.id)

    def __repr__(self):
        return "player %s" % (self.id)
        

            
