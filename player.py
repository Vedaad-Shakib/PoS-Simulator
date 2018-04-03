"""This module defines the Player class, which represents a player in the network and contains functionality to make transactions, propose blocks, and validate blocks.
"""

import block
import transaction

import random

class Player:
    nTransactions = 5 # number of transactions in a block
    id = 0
    
    def __init__(self):
        """Creates a new Player object"""
        
        self.id = Player.id
        Player.id += 1

    def makeTransaction(self):
        """Returns a random transaction"""
        
        return transaction.Transaction(self.id, 1)

    def proposeBlock(self, solver):
        """Proposes a Block consisting of multiple random transactions"""
        
        pickedTx = solver.txs[:self.nTransactions]
        solver.txs = solver.txs[self.nTransactions:]

        return block.Block(pickedTx)

    
    def validate(self, block):
        """Validates a block"""
        
        return block

    def __str__(self):
        return "player %s" % (self.id)

    def __repr__(self):
        return "player %s" % (self.id)
        

            
