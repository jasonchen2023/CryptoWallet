#!/usr/local/bin/python3

""" 
test_block.py

Group 3
CS60, Spring 2021
Final Project

Update Log:
Initial Write:		GK 05/31/21 05:51PM EDT - Program to test Block functionality

To Run: python -m unittest test_block OR python -m unittest -v test_block (for verbose)
"""

import unittest
from unittest import TestCase


from blockchain import Blockchain
from block import Block
from transaction import Transaction

class TestBlock(TestCase):
    def test_block_hash(self):

        block = Block(1, 0, [], '0')

        # Recalculate hash of block
        calc_hash = block.hash_block()

        # Confirm that calculated hash equals stored hash
        self.assertEqual(block.hash, calc_hash)


if __name__ == '__main__':
    unittest.main()