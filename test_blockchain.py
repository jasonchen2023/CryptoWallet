#!/usr/local/bin/python3

""" 
test_blockchain.py

Group 3
CS60, Spring 2021
Final Project

Update Log:
Initial Write:		GK 05/31/21 03:23PM EDT - Program to test Blockchain functionality

To Run: python -m unittest test_blockchain OR python -m unittest -v test_blockchain (for verbose)
"""

import unittest
from unittest import TestCase
import copy
import json 
import string

import constants 

from blockchain import Blockchain
from block import Block
from transaction import Transaction


class TestBlockchain(TestCase):
    ## [[REMOVED MINING REWARD]]
    # def test_mine_empty_transaction_block(self):

    #     # Pretty sure address is wrong
    #     mine_addr = 'peer1'

    #     blockchain = Blockchain()
    #     block = blockchain.mine(mine_addr)

    #     # Check that block created
    #     self.assertIsNotNone(block)

    #     # Check that block was added to chain
    #     self.assertEqual(blockchain.last_block.hash, block.hash)

    #     # Check that block only has 1 transaction - the mining reward
    #     self.assertEqual(len(block.transactions), 1)

    #     reward_trans = block.transactions[0]

    #     # Check parameters of reward_trans - no sender, gives # coins defined in constants
    #     self.assertEqual(reward_trans.sender, '0')
    #     self.assertEqual(reward_trans.recipient, mine_addr)
    #     self.assertEqual(reward_trans.amount, 25)

    #     print("Blockchain: ", blockchain._chain)

    def test_mine_simple_transaction_block(self):
        mine_addr = 'peer2'

        blockchain = Blockchain()
        blockchain.create_trans('peer1', 'peer3', 1)
        blockchain.create_trans('peer2', 'peer1', 10)
        self.assertEqual(len(blockchain._pending_transactions), 2)

        block = blockchain.mine(mine_addr)


        # Check that block was created (could be mined)
        self.assertIsNotNone(block)

        # Check if block was added to chain
        self.assertEqual(blockchain.last_block.hash, block.hash)

        # Check that pending transactions was emptied
        self.assertEqual(0, len(blockchain._pending_transactions))

        # Check that block contains all transactions
        self.assertEqual(3, len(block.transactions))

        reward_trans = block.transactions[-1]

        # Verify correct reward transaction
        self.assertEqual('0', reward_trans.sender)
        self.assertEqual(mine_addr, reward_trans.recipient)
        self.assertEqual(25, reward_trans.amount)

        print("Blockchain: ", str(blockchain._chain))

    def test_empty_chain_validation(self):
        addr = 'peer1'
        blockchain = Blockchain()
        block = blockchain.mine(addr)

        self.assertTrue(blockchain.validate_chain(blockchain.full_chain))
        print("Blockchain: ", str(blockchain._chain))

    def test_corrupted_chain_validation(self):
        addr = 'peer1'
        blockchain = Blockchain()
        last_block = blockchain.mine(addr)

        # Check that the block could be mined
        self.assertIsNotNone(last_block)

        chain = blockchain.full_chain

        # Corrupt a block
        chain.append(Block(1, 1, [], last_block.hash))

        self.assertFalse(blockchain.validate_chain(blockchain.full_chain))
        print("Blockchain: ", str(blockchain._chain))

    def test_replace_chain(self):
        """
        Test to confirm this chain is replaced for a longer chain.
        This is how we handle when 2 peers mine the same block and
        the chain forks.
        """
        addr = 'peer4'

        blockchain1 = Blockchain()
        blockchain1.mine(addr)

        blockchain2 = copy.deepcopy(blockchain1)
        blockchain2.mine(addr)

        # Confirm that chain1 has 2 blocks, chain2 has 3
        self.assertEqual(2, len(blockchain1.full_chain))
        self.assertEqual(3, len(blockchain2.full_chain))

        # Print both chains
        print("Before replacement:")
        print("Blockchain1: ", str(blockchain1._chain))
        print("Blockchain2: ", str(blockchain2._chain))

        # Replace shorter chain with longer
        blockchain1.replace_chain(blockchain2.full_chain)

        # Confirm that both chains have 3 blocks, and are equal
        self.assertEqual(3, len(blockchain1.full_chain))
        self.assertEqual(3, len(blockchain2.full_chain))
        self.assertEqual(blockchain1.last_block.hash, blockchain2.last_block.hash)

        # Print both chains
        print("After replacement:")
        print("Blockchain1: ", str(blockchain1._chain))
        print("Blockchain2: ", str(blockchain2._chain))

    def test_replace_chain_original(self):
        addr = 'peer5'

        blockchain1 = Blockchain()
        blockchain1.mine(addr)

        blockchain2 = copy.deepcopy(blockchain1)

        blockchain1.mine(addr)

         # Confirm that chain1 has 3 blocks, chain2 has 2
        self.assertEqual(3, len(blockchain1.full_chain))
        self.assertEqual(2, len(blockchain2.full_chain))

        # Print both chains
        print("Before replacement:")
        print("Blockchain1: ", str(blockchain1._chain))
        print("Blockchain2: ", str(blockchain2._chain))

        # Attempt to replace chain - should not work
        blockchain1.replace_chain(blockchain2.full_chain)

        # Confirm that both chains hace not changed and are not equal
        self.assertEqual(3, len(blockchain1.full_chain))
        self.assertEqual(2, len(blockchain2.full_chain))
        self.assertNotEqual(blockchain1.last_block.hash, blockchain2.last_block.hash)
        
        # Print both chains - should be the same
        print("After replacement:")
        print("Blockchain1: ", str(blockchain1._chain))
        print("Blockchain2: ", str(blockchain2._chain))

if __name__ == '__main__':
    unittest.main()


