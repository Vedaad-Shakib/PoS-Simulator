"""This module defines the Player class, which represents a player in the network and contains functionality to make transactions, propose blocks, and validate blocks.
"""

import block
import solver
import transaction

import random
import numpy as np

class Player:
    N_TRANSACTIONS = 3    # number of transactions included in a block
    P_TRANSACTIONS = 0.1  # probability of making a transaction at heartbeat r
    MEAN_PROP_TIME = 0.1    # mean propagation time

    id = 0                # player id

    # defines node state constants (none, validator, proposer)
    class ROLES:
        NONE      = 0
        VALIDATOR = 1
        PROPOSER  = 2
    
    def __init__(self, stake):
        """Creates a new Player object"""

        self.id = Player.id # the player's id
        Player.id += 1                 

        self.stake = stake  # the number of tokens the player has staked in the system
        
        self.connections = [] # list of connected players
        self.inbound     = [] # inbound messages from other players in the network at heartbeat r
        self.outbound    = [] # outbound messages to other players in the network at heartbeat r

        self.blockchain      = None  # the current state of the player's blockchain
        self.mempool         = set() # the current list of txs the player knows about
        self.seenTxs         = set() # set of seen txs
        self.seenBlocks      = {}    # map of seen blocks to nValidators
        self.committedBlocks = set() # set of blocks already added to blockchain (prevent duplicates)

        self.role = self.ROLES.NONE

    def action(self, heartbeat):
        """Executes the player's actions for heartbeat r"""

        #t="\t"
        #print(t, self, ":")
        
        # if start of round, reset node role
        if heartbeat % solver.Solver.N_HEARTBEATS_IN_ROUND == 0:
            if self.id in self.solver.propSet:
                self.role = self.ROLES.PROPOSER
            elif self.id in self.solver.valSet: # bug? propSet may have overlap with valSet, in which case player would only be proposer, not validator
                self.role = self.ROLES.VALIDATOR
            else:
                self.role = self.ROLES.NONE

            #print(t, "role reassigned:", self.role)

        #print(t, "mempool:", self.mempool)
        #print(t, "inbound:", self.inbound)
        #print(t, "blockchain:", self.blockchain)

        # process inbound messages
        for message, timestamp in self.inbound:
            # don't have access to messages which arrive after the current heartbeat
            # don't want to process already-seen messages
            if timestamp > heartbeat:
                continue
            
            # if inbound message is transaction, add to local mempool
            if type(message) == transaction.Transaction:
                if message in self.seenTxs:
                    continue
                
                self.mempool.add(message)
                self.seenTxs.add(message)

            if type(message) == block.Block:
                # if block has been seen and not updated since seen
                if message in self.seenBlocks and self.seenBlocks[message] == len(message.validators):
                    continue
                
                # if validator, sign block
                if self.role == self.ROLES.VALIDATOR:
                    if self.isValid(message):
                        message.validators.add(self.id)
                        
                # if block has more than 2/3 validator signatures, add to local blockchain
                if len(message.validators) >= 2*solver.Solver.N_VALIDATORS/3 and message not in self.committedBlocks:
                    fBlock = block.Block(message.txs, next=message.next, id=message.id) # create copy of block
                    fBlock.validators = message.validators.copy() # copy validators
                    fBlock.next = self.blockchain
                    self.blockchain = fBlock

                    self.committedBlocks.add(message)

                    # remove txs from local mempool
                    for tx in fBlock.txs:
                        if tx in self.mempool:
                            self.mempool.remove(tx)
                    # optimization: if common blockchain among all players, add to global blockchain to save mem
                    
                self.seenBlocks[message] = len(message.validators)

            # add to seen messages and outbound for propagation via gossip protocol
            self.outbound.append([message, timestamp])

        self.inbound = list(filter(lambda x: x[1] > heartbeat, self.inbound)) # get rid of already-processed messages
        # if proposer and at the start of round, propose block
        if heartbeat % solver.Solver.N_HEARTBEATS_IN_ROUND == 0 and self.role == self.ROLES.PROPOSER:
            pBlock = self.proposeBlock()
            self.seenBlocks[pBlock] = 0
            self.outbound.append([pBlock, heartbeat])
                
        # make transaction with probability p
        if random.random() < self.P_TRANSACTIONS:
            tx = self.makeTransaction()
            self.outbound.append([tx, heartbeat])
            self.mempool.add(tx)

        #print(t, "mempool:", self.mempool)
        #print(t, "outbound:", self.outbound)
        #print(t, "blockchain:", self.blockchain)
        #print()
        
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

    def proposeBlock(self):
        """Proposes a Block consisting of multiple random transactions"""
        
        txs = random.sample(self.mempool, min(self.N_TRANSACTIONS, len(self.mempool)))

        return block.Block(txs)
    
    def isValid(self, block):
        """Returns whether a block is valid or not"""

        return True

    def __str__(self):
        return "player %s" % (self.id)

    def __repr__(self):
        return "player %s" % (self.id)
        

            
