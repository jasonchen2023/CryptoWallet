#!/usr/local/bin/python3

"""
constants.py
"""

DIFFICULTY = 4                  # Equal to the number of zeros that lead the hash, aka how difficult to mine
MAX_NONCE = 2**32               # Maximum number that can be stored in a 32-bit number
TARGET = 2 ** (256-DIFFICULTY)  # Nonce must be less than the target to be accepted

REWARD = 20                     # Mining reward


