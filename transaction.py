#!/usr/local/bin/python3

""" 
transaction.py

Group 3
CS60, Spring 2021
Final Project

Update Log:
Initial Write:		GK 05/30/21 04:53PM EDT - Seperated large blockchain program into different modules 
"""
import datetime         # for blocks' timestamps



class Transaction:
    def __init__(self, sender_addr, sender_priv_key, receiver_addr, amount):
        self.sender_addr = sender_addr
        self.sender_priv_key = sender_priv_key
        self.receiver_addr = receiver_addr
        self.amount = amount
        self.timestamp = str(datetime.datetime.now())

@property
def get_sender(self):
    return str(self.sender_addr)

@property
def get_recv(self):
    return str(self.reciever_addr)

@property
def get_amount(self):
    return str(self.amount)

@property
def get_data(self):
    sender = self.get_sender
    recv = self.get_recv
    amt = self.get_amount

    return sender, recv, amt