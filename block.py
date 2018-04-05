"""This module defines a Block class, which represents a block on the blockchain.
"""

class Block:
    id = 0
    
    def __init__(self, txs, next=None):
        """Creates a new Block object given a list of transactions txs"""

        self.id = Block.id
        Block.id += 1
        
        self.next = next
        self.txs = txs

    def __eq__(self, other):
        """Equality for Block objects is defined as having the same transactions"""
        
        selfIds = [i.id for i in self.txs]
        otherIds = [i.id for i in other.txs]

        return set(selfIds) == set(otherIds)

    def __str__(self):
        if self.next == None:
            return "block %s: "%(self.id)+", ".join([str(i) for i in self.txs])
        return "block %s: "%(self.id)+", ".join([str(i) for i in self.txs])+"\n"+str(self.next)        

    def __repr__(self):
        if self.next == None:
            return "block %s: "%(self.id)+", ".join([str(i) for i in self.txs])
        return "block %s: "%(self.id)+", ".join([str(i) for i in self.txs])+"\n"+repr(self.next)



        
