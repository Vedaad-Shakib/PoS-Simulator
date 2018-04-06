"""This module defines a Block class, which represents a block on the blockchain.
"""

class Block:
    id = 0
    
    def __init__(self, txs, next=None, id=-1):
        """Creates a new Block object given a list of transactions txs"""

        if id == -1:
            self.id = Block.id
            Block.id += 1
        else:
            self.id = id
        
        self.next = next # next block in blockchain
        self.txs = txs   # list of transactions

        self.validators = set() # set of validators signing the block

    def __eq__(self, other):
        """Equality for Block objects is defined as having the same transactions"""

        if other == None:
            return False
        
        selfIds = [i.id for i in self.txs]
        otherIds = [i.id for i in other.txs]

        return set(selfIds) == set(otherIds)

    def __hash__(self):
        """Hash for reasonz !"""

        return self.id

    def __str__(self):
        if self.next == None:
            return "block %s: "%(self.id)+", ".join([str(i) for i in self.txs])+\
                   "validators: %s"%(list(self.validators))
        return "block %s: "%(self.id)+", ".join([str(i) for i in self.txs])+"\n"+str(self.next)        

    def __repr__(self):
        if self.next == None:
            return "block %s: "%(self.id)+", ".join([str(i) for i in self.txs])+\
                   "validators: %s"%(list(self.validators))
        return "block %s: "%(self.id)+", ".join([str(i) for i in self.txs])+"\n"+repr(self.next)



        
