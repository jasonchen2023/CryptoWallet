#!/usr/local/bin/python3

""" 
blockchain.py
Group 3
CS60, Spring 2021
Final Project
Update Log:
Initial Write:		GK 05/31/21 02:38PM EDT - First attempt at crypto wallet
Update 1:           GK 06/01/21 03:35PM EDT - Edits and Debugging
Requirements: pycrypto package
"""
import hashlib                      # for SHA256 encryption
import binascii                     # to convert address
import Crypto
from Crypto import Random           
from Crypto.PublicKey import RSA    # for private key encryption
from Crypto.Signature import PKCS1_v1_5

import constants

from transaction import Transaction
from block import Block
from blockchain import Blockchain


class Wallet(object):
    """
    A wallet needs a private/public key pair. We will use the public key as
    the sender's address.
    """
    def __init__(self):
        random = Random.new().read
        self.private_key = RSA.generate(1024, random)
        self.public_key = self.private_key.publickey()
        self.signer = PKCS1_v1_5.new(self.private_key)
        self.balance = 100

    @property
    def address(self):
        """
        For simplicity, we are making the address the public key
        """
        addr = binascii.hexlify(self.public_key.exportKey(format='DER')).decode('ascii')
        return addr

    def sign(self, msg):
        h = hashlib.sha256(msg)
        s = binascii.hexlify(self.signer.sign(h)).decode('ascii')
        return s

    def verify_signature(self, wallet_addr, msg, signature):
        pub_key = RSA.importKey(binascii.unhexlify(wallet_addr))
        verifier = PKCS1_v1_5.new(pub_key)
        h = hashlib.sha256(msg)
        result = verifier.verify(h, binascii.unhexlify(signature))
        return result

    def getKeys(self):
        return self.private_key, self.public_key

    def deposit(self, transaction):
        if transaction.receiver_addr == self.address:
            self.balance += transaction.amount

    def withdraw(self, transaction):
        if transaction.sender_addr == self.address:
            self.balance -= transaction.amount