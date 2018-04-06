"""This module defines the Transaction class, which represents a transaction made between two players.
"""

class Transaction:
    id = 0
    
    def __init__(self, senderId, recipId):
        """Creates a new Transaction object, given senderId and recipId"""
        
        self.senderId = senderId
        self.recipId = recipId
        
        self.id = Transaction.id
        Transaction.id += 1

    def __eq__(self, other):
        """Define equality for Transaction objects"""

        if other == None:
            return False
        
        return self.id == other.id

    def __str__(self):
        return "transaction %s" % (self.id)

    def __repr__(self):
        return "transaction %s" % (self.id)

    def __hash__(self):
        """Define hash to make Transaction hashable"""
        
        return self.id
