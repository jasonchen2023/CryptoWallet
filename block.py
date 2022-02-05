#!/usr/local/bin/python3

""" 
block.py

Group 3
CS60, Spring 2021
Final Project

Update Log:
Initial Write:		GK 05/30/21 04:45PM EDT - Seperated large blockchain program into different modules 
Debugging:          NK 05/31/21 11:00PM PDT - Fixed errors
"""
import hashlib          # for encryption
import json             # to format blocks
import datetime         # for blocks' timestamps

import constants 


# BLOCK CLASS

class Block:
    def __init__(self, index, nonce, transactions, hash, prev_hash):
        self.index = index
        self.nonce = nonce 
        self.transactions = transactions
        self.prev_hash = prev_hash or (constants.DIFFICULTY *'0')
        self.hash = self.hash_block()
        self.timestamp = str(datetime.datetime.now())

    def hash_block(self):
        data = str(self.nonce)+str(self.transactions)+self.prev_hash
        string_obj = json.dumps(data, sort_keys=True)
        block_string = string_obj.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash

    @property
    def num_transactions(self):
        return len(self.transactions)

    @property
    def block_transactions(self):
        return self.transactions

