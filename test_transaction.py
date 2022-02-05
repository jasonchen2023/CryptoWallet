#!/usr/local/bin/python3

""" 
test_transaction.py

Group 3
CS60, Spring 2021
Final Project

Update Log:
Initial Write:		GK 05/31/21 05:42PM EDT - Program to test Transaction functionality

To Run: python -m unittest test_transaction OR python -m unittest -v test_transaction (for verbose)
"""

import unittest
from unittest import TestCase
import json
import string


from blockchain import Blockchain
from block import Block
from transaction import Transaction

class TestTransaction(TestCase):
    def test_create_transaction(self):

        blockchain = Blockchain()

        _, validity = blockchain.create_trans('Mark', 'peer1', 'peer2', 1)

        transaction = blockchain.last_transaction
        print("Transaction: ", str(transaction))
        print("Blockchain: ", str(blockchain._chain))

        # Confirm transacton validity
        self.assertTrue(validity)
        self.assertEqual(transaction.sender_addr, 'Mark')
        self.assertEqual(transaction.sender_priv_key, 'peer1')
        self.assertEqual(transaction.receiver_addr, 'peer2')
        self.assertEqual(transaction.amount, 1)


    def test_negative_transaction(self):
        """
        Confirm that transaction validate function prevents
        stealing via negative transaction amounts
        """
        blockchain = Blockchain()
        transaction, validity = blockchain.create_trans('Mark', 'peer1', 'peer2', -1)
        
        # Print blockchain - does it get added?
        print("Blockchain: ", str(blockchain._chain))

        # Check transaction validity
        self.assertIsNone(transaction)
        self.assertFalse(validity)

if __name__ == '__main__':
    unittest.main()