#!/usr/local/bin/python3

""" 
blockchain.py

Group 3
CS60, Spring 2021
Final Project

Update Log:
Initial Write:		GK 05/30/21 05:08PM EDT - Seperated large blockchain program into different modules
Debugging:          NK 05/31/21 11:00PM PDT - Fixed errors 
Update:             GK 06/02/21 04:26PM EDT - Added further functionality
"""
import hashlib          # for encryption
import json             # to format blocks
import datetime         # for blocks' timestamps

import constants 

from block import Block
from transaction import Transaction


class Blockchain:

    def __init__(self):
        self._chain = []
        self._pending_transactions = []
        self.nodes = set()
        self.build_genesis()            # Creates the initial block in chain

    def build_genesis(self):
        genesis_block = Block(0, 0, self._pending_transactions, '0000', '0') # Index = 0
        self._chain.append(genesis_block)
        

    def add_block(self, block):
        if self.block_validity(block, self.last_block):
            self._chain.append(block)
            self._pending_transactions = [] # Empty list of pending transactions now they are in a block

            return True

        return False

    def compute_balance(self, peer_addr):
        #block = self.chain_length
        earned = 0
        spent = 0
        chain = self.full_chain
        for block in chain:
            transactions = block.transactions
            for t in transactions:
                if t.sender_addr == peer_addr:
                    spent += t.amount
                if t.receiver_addr == peer_addr:
                    earned += t.amount
        balance = earned - spent
        return balance

    def validate_trans(self, sender_addr, amount):
        # Prevent stealing by creating negative transactions
        if amount < 0:
            return False
        # Balance in wallet > amount checked on peer side
        return True

    def create_trans(self, sender_addr, sender_priv_key, receiver_addr, amount):
        transaction = Transaction(sender_addr, sender_priv_key, receiver_addr, amount)
        if sender_addr == "deposit":
            self._pending_transactions.append(transaction)

            return transaction, True 

        if receiver_addr == "withdrawal":
            self._pending_transactions.append(transaction)

            return transaction, True

        if self.validate_trans(sender_addr, float(amount)) == True:
            self._pending_transactions.append(transaction)

            return transaction, True
        
        return None, False

    def mine(self):

        prev_block = self.last_block
        new_index = prev_block.index + 1
        prev_hash = prev_block.hash
        nonce = 0

        # Create block
        block = Block(new_index, nonce, self._pending_transactions, 0, prev_hash)

        # Proof of work automatically sets correct nonce and hash for block
        self.proof_of_work(block)


        # Add block to chain
        if self.add_block(block):
            return block

        return None


    def proof_of_work(self, block, difficulty = constants.DIFFICULTY):
        found = False
        n = 0
        while found is False:
            for i in range(constants.MAX_NONCE):   # Max number storable in 32-bit number 
                data = str(block.index)+str(n)+str(self._pending_transactions)+block.prev_hash
                str_obj = json.dumps(data, sort_keys=True).encode()
                new_hash = hashlib.sha256(str_obj).hexdigest()
                if new_hash[:difficulty] == difficulty*'0':
                    # Found valid hash - save hash and nonce to block
                    block.hash = new_hash
                    block.nonce = n
                    found = True
                    break
                n += 1
                # Print just for testing
                # print("New Hash: ", new_hash)
                # print("Block Hash: ", block.hash)
                # print("Current Nonce: ", n)
                # print("Block Nonce: ", block.nonce)
                


    def block_validity(self, block, prev_block, verbose=True):
        i = block.index
        flag = True
        # Check that indices are sequential - no missing blocks
        if block.index != prev_block.index + 1:
            flag = False
            if verbose:
                print(f'Wrong block index at block {i}.')
        # Compare hash of previous block with prev_hash of current block
            if prev_block.hash != block.prev_hash:
                flag = False
            if verbose:
                    print(f'Wrong previous hash at block {i}.')
        # Compare stored hash of block with computed hash of block
            if block.hash != block.hash_block():
                flag = False
                if verbose:
                    print(f'Wrong hash at block {i}.')
        # Compare timestamps to check for backdating
            if prev_block.timestamp >= block.timestamp:
                flag = False
                if verbose:
                    print(f'Backdating at block {i}.')
        return flag
    
    # CHAIN_VALIDITY FUNCTION
    def chain_validity(self, chain_to_validate, verbose = True):
        flag = True
        # Validate genesis block against original
        if self._chain[0].hash_block() != chain_to_validate[0].hash_block():
            flag = False
            if verbose:
                print(f'Genesis block of chain has wrong hash.')

        i = 0
        # Iterate through and validate remainder of chain (non-genesis blocks)
        for i in range(1,len(chain_to_validate)):
            # Run all checks from block validity
            if not self.block_validity(chain_to_validate[i], chain_to_validate[i - 1]):
                flag = False
            # Check for missing or extra blocks by confirming index of block at i is i 
            if chain_to_validate[i].index != i:
                flag = False
                if verbose:
                    print(f'Wrong block index at block {i}.')
        return (flag, i)

    # Recompute Chain starting from a given index
    def recompute_chain_at_index(self, index):
        for i in range(index, len(self.full_chain)):
            prev_block = self.full_chain[i-1]
            curr_block = self.full_chain[i]
            curr_block.index = prev_block.index + 1
            curr_block.prev_hash = prev_block.hash

            self.proof_of_work(self.full_chain[i])

    def replace_chain_simple(self, new_chain):
        # this function assumes the new chain is valid
        # and correct
        self._chain = []
        for i in range(0, len(new_chain)):
            self._chain.append(new_chain[i])
        
    # REPLACE_CHAIN - only replace if new chain is larger than current
    def replace_chain(self, new_chain):
        if len(new_chain) <= len(self._chain):
            return False
        
        # Validate new chain
        if not self.chain_validity(new_chain):
            return False

        # If new chain is longer and valid, add all blocks missing from current chain to current chain
        new_blocks = new_chain[len(self._chain):]
        for block in new_blocks:
            self.add_block(block)   # add_block returns true upon success
        
    def print_chain(self):
        for block in self.full_chain:
            print("Index: " + str(block.index))
            print("Nonce: " + str(block.nonce))
            print("Transactions: ")
            for t in block.transactions:
                print("Sender: " + str(t.sender_addr))
                print("Receiver: " + str(t.receiver_addr))
                print("Amount:" + str(t.amount))
                print("")
            print("Prev hash: " + str(block.prev_hash))
            print("Curr hash: " + str(block.hash))
            print("Timestamp: " + str(block.timestamp))
    
    @property
    def last_block(self):               # Used to get new indices
        return self._chain[-1]

    @property
    def last_transaction(self):         # Returns last transaction in pending transactions
        return self._pending_transactions[-1]
    
    @property                           # Returns all pending transactions
    def pending_transactions(self):
        return self._pending_transactions

    @property                           # Returns blockchain
    def full_chain(self):
        return self._chain

    def get_pending_data(self, pending_trans):
        sender = str(pending_trans.sender_addr)
        recv = str(pending_trans.receiver_addr)
        amt = str(pending_trans.amount)
        return sender, recv, amt

