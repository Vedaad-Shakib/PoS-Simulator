"""This module defines the Player class, which represents a player in the network and contains functionality to make transactions, propose blocks, and validate blocks.
"""

import block
import transaction

import random

class Player:
    nTransactions = 5 # number of transactions in a block
    id = 0
    
    def __init__(self, stake):
        """Creates a new Player object"""
        
        self.id = Player.id
        Player.id += 1

        self.stake = stake

    def makeTransaction(self):
        """Returns a random transaction"""
        
        return transaction.Transaction(self.id, 1)

    def proposeBlock(self, txs):
        """Proposes a Block consisting of multiple random transactions"""
        
        pickedTx = txs[:self.nTransactions]

        return block.Block(pickedTx)

    
    def validate(self, uBlock):
        """Validates a block"""

        if random.random() < 0.3:
            return uBlock
        return block.Block([])

    def __str__(self):
        return "player %s" % (self.id)

    def __repr__(self):
        return "player %s" % (self.id)
        

            
