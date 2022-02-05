#!/usr/local/bin/python3

""" 
script.py
Group 3
CS60, Spring 2021
Final Project
Update Log:
Initial Write:		NK 05/31/21 11:00PM PDT - Testing script for Blockchain API
"""
import hashlib          # for encryption
import json             # to format blocks
import datetime         # for blocks' timestamps

import constants
from block import Block
from blockchain import Blockchain
from transaction import Transaction
from wallet import Wallet

print("======================================================================")
print("Test Run at: ", datetime.datetime.now())
print("======================================================================")
# BLOCK CLASS
bc = Blockchain()
print("-----BLOCK 0-----")
print("Index: " + str(bc.last_block.index))
print("Nonce: " + str(bc.last_block.nonce))
print("Transactions: " + str(bc.last_block.transactions))
print("Prev hash: " + str(bc.last_block.prev_hash))
print("Curr hash: " + str(bc.last_block.hash))
print("Timestamp: " + str(bc.last_block.timestamp))
bc.create_trans('Roxanne', 'peer1', 'Willy', 5)
bc.create_trans('Brian', 'peer1', 'Margyu', 15)
bc.mine()
print("-----BLOCK 1 MINED-----")
print("Index: " + str(bc.last_block.index))
print("Nonce: " + str(bc.last_block.nonce))
print("Transactions: ")
for transaction in bc.last_block.transactions:
    print("\tSender:" + str(transaction.sender_addr))
    print("\tReceiver:" + str(transaction.receiver_addr))
    print("\tAmt:" + str(transaction.amount))
print("Prev hash: " + str(bc.last_block.prev_hash))
print("Curr hash: " + str(bc.last_block.hash))
print("Timestamp: " + str(bc.last_block.timestamp))
bc.mine()
print("-----BLOCK 2 MINED-----")
print("Index: " + str(bc.last_block.index))
print("Nonce: " + str(bc.last_block.nonce))
print("Transactions: " + str(bc.last_block.transactions))
print("Prev hash: " + str(bc.last_block.prev_hash))
print("Curr hash: " + str(bc.last_block.hash))
print("Timestamp: " + str(bc.last_block.timestamp))
bc.mine()
print("-----BLOCK 3 MINED-----")
print("Index: " + str(bc.last_block.index))
print("Nonce: " + str(bc.last_block.nonce))
print("Transactions: " + str(bc.last_block.transactions))
print("Prev hash: " + str(bc.last_block.prev_hash))
print("Curr hash: " + str(bc.last_block.hash))
print("Timestamp: " + str(bc.last_block.timestamp))
bc.mine()
print("-----BLOCK 4 MINED-----")
print("Index: " + str(bc.last_block.index))
print("Nonce: " + str(bc.last_block.nonce))
print("Transactions: " + str(bc.last_block.transactions))
print("Prev hash: " + str(bc.last_block.prev_hash))
print("Curr hash: " + str(bc.last_block.hash))
print("Timestamp: " + str(bc.last_block.timestamp))
print("")
print("-----BLOCKCHAIN-----")
print("Blockchain: ", bc._chain)
print("======================================================================")
print("\n\n\n\n\n")