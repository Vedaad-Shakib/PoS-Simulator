"""This module defines the Player class, which represents a player in the network and contains functionality to make transactions, propose blocks, and validate blocks.
"""

import block
import solver
import transaction
import states
import message

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
        self.seenBlocks      = {}    # map of blockId to block
        self.committedBlocks = set()

        self.preVotes    = {}
        self.votes       = {}

        self.stage = states.States.Consensus.PRE_PRE_VOTE

        self.proposer  = False

    def action(self, heartbeat):
        """Executes the player's actions for heartbeat r"""

        # if start of round, reset node role
        if heartbeat % solver.Solver.N_HEARTBEATS_IN_ROUND == 0:
            self.proposer  = False
            if self.id == self.solver.propSet:
                self.proposer = True

            self.stage = states.States.Consensus.PRE_PRE_VOTE
            
            self.preVotes.clear()
            self.votes.clear()

        # process inbound messages
        for msg, timestamp in self.inbound:
            # don't have access to messages which arrive after the current heartbeat
            if timestamp > heartbeat:
                continue
            
            # if inbound message is transaction, add to local mempool
            if msg.type == message.Message.MessageType.TRANSACTION:
                if msg.value in self.seenTxs:
                    continue
                
                self.mempool.add(msg.value)
                self.seenTxs.add(msg.value)

            # handle pre pre vote
            if self.stage == states.States.Consensus.PRE_PRE_VOTE and msg.type == message.Message.MessageType.BLOCK:
                # message value is block
                if msg.value in self.seenBlocks:
                    continue
                
                self.seenBlocks[hash(msg.value)] = msg.value
                    
                if self.isValid(msg.value):
                    pv = hash(msg.value)
                else:
                    pv = None
                    
                self.outbound.append([message.Message(message.Message.MessageType.PRE_VOTE, pv, self.id), timestamp])
                self.preVotes[pv] = set([self.id])
                self.stage = states.States.Consensus.PRE_VOTE
                # todo: add timeout

            # handle pre vote
            if self.stage == states.States.Consensus.PRE_VOTE and msg.type == message.Message.MessageType.PRE_VOTE:
                # message value is block hash
                if msg.value not in self.preVotes:
                    self.preVotes[msg.value] = set()

                if msg.senderId not in self.preVotes[msg.value]:
                    self.preVotes[msg.value].add(msg.senderId)
                    self.outbound.append([msg, timestamp])

                if len(self.preVotes[msg.value]) >= 2*self.solver.N_PLAYERS/3:
                    self.stage = states.States.Consensus.VOTE
                    self.votes[msg.value] = set([self.id])
                    self.outbound.append([message.Message(message.Message.MessageType.VOTE, msg.value, self.id), timestamp])

            if self.stage == states.States.Consensus.VOTE and msg.type == message.Message.MessageType.VOTE:
                if msg.value not in self.votes:
                    self.votes[msg.value] = set()

                if msg.senderId not in self.votes[msg.value]:
                    self.votes[msg.value].add(msg.senderId)
                    self.outbound.append([msg, timestamp])

                if len(self.votes[msg.value]) >= 2*self.solver.N_PLAYERS/3 and msg.value not in self.committedBlocks:
                    self.committedBlocks.add(msg.value)
                    
                    nBlock = self.seenBlocks[hash(msg.value)].copy()
                    nBlock.next = self.blockchain
                    self.blockchain = nBlock

                    # remove txs from local mempool
                    for tx in nBlock.txs:
                        if tx in self.mempool:
                            self.mempool.remove(tx)

        self.inbound = list(filter(lambda x: x[1] > heartbeat, self.inbound)) # get rid of already-processed messages
        # if proposer and at the start of round, propose block and send prevote
        if heartbeat % solver.Solver.N_HEARTBEATS_IN_ROUND == 0 and self.proposer:
            pBlock = self.proposeBlock()
            self.outbound.append([message.Message(message.Message.MessageType.BLOCK, pBlock, self.id), heartbeat])
            self.outbound.append([message.Message(message.Message.MessageType.PRE_VOTE, hash(pBlock), self.id), heartbeat])
                
        # make transaction with probability p
        if random.random() < self.P_TRANSACTIONS:
            tx = self.makeTransaction()
            self.outbound.append([message.Message(message.Message.MessageType.TRANSACTION, tx, self.id), heartbeat])
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
        

            
