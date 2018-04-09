"""This module defines the Player class, which represents a player in the network and contains functionality to make transactions, propose blocks, and validate blocks.
"""

import block
import solver
import transaction

import random
import numpy as np

class Player:
    id = 0 # player id
    
    MEAN_TX_FEE = 0.2  # mean transaction fee
    STD_TX_FEE  = 0.05 # std of transaction fee

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

        self.validator = False # whether the player is currently a validator or proposer
        self.proposer  = False

    def action(self, heartbeat):
        """Executes the player's actions for heartbeat r"""

        t="\t"
        #print(t, self, ":")
        
        # if start of round, reset node role
        if heartbeat % solver.Solver.N_HEARTBEATS_IN_ROUND == 0:
            self.proposer  = False
            self.validator = False
            if self.id in self.solver.propSet:
                self.proposer = True
            if self.id in self.solver.valSet: 
                self.validator = True

            #print(t, "role reassigned:", self.proposer, self.validator)

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
                if self.validator and self not in message.validators:
                    if self.isValid(message):
                        #print(t, self, message.id)
                        message.validators.add(self)
                        
                # if block has more than 2/3 validator signatures, add to local blockchain
                if len(message.validators) >= 2*solver.Solver.N_VALIDATORS/3 and message not in self.committedBlocks:
                    fBlock = block.Block(message.txs, next=message.next, id=message.id, proposer=message.proposer) # create copy of block
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
        if heartbeat % solver.Solver.N_HEARTBEATS_IN_ROUND == 0 and self.proposer:
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

        fee = max(random.gauss(self.MEAN_TX_FEE, self.STD_TX_FEE), 0)
        return transaction.Transaction(self.id, 0, fee)

    def proposeBlock(self):
        """Proposes a Block consisting of multiple random transactions"""
        
        txs = random.sample(self.mempool, min(self.N_TRANSACTIONS, len(self.mempool)))

        return block.Block(txs, proposer=self)
    
    def isValid(self, block):
        """Returns whether a block is valid or not"""

        return True

    def __str__(self):
        return "player %s" % (self.id)

    def __repr__(self):
        return "player %s" % (self.id)
        

            
