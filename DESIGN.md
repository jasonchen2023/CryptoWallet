<h1> <img src="https://i.imgur.com/4MOXfCU.png"
  width="90"
  height="90"
  style="float:left;">

# DESIGN.md

**CS60, 21S
Final Project
Peer-to-Peer Blockchain with Cryptocurrency Wallet Application**

**Group 3 - Error 404
Jason Chen, Grace King, Norman Kuang, Rehoboth Okorie**

## Introduction

### High Level Summary

This document describes the design and implementation of the blockchain API, peer-to-peer network protocol, and cryptocurrency wallet application demonstration for our CS60 21S final project. The fundamental building components of the blockchain are blocks, which are linked together like a linked list to form the "block chain". Details of how this is implemented can be found in the **Blockchain API** section, below. Peer-to-peer (P2P) is a decentralized network in which peers cam communicate with each other without a central authority. Details of the P2P protocol implemented for this project can be found in the **P2P Network Protocol** below. To demonstrate successful implementation of blockchain, a demo application of a cryptocurrency wallet was implemented. Details of the design for the cryptocurrency wallet and the application's GUI can be seen below in the section **Demo Application: Cryptocurrency Walet**.

### Technologies Used

This project was written using Python 3, ==**[[FILL IN REST OF TECHNOLOGIES USED]]**==

## Blockchain API

The fundamental building components of the blockchain are blocks, which are linked together like a linked list to form the “blockchain”. In addition, because we are building a crypto wallet as our application, there is a third building component - transactions - which are included in blocks.

The blockchain API design contains three classes:

1. **Transaction** - the Transaction object that make up the data stored in blocks (stored in block.transactions class variable) that comprise the blockchain
   program
2. **Block** - the Block object that are linked to form the blockchain, and associated functions
3. **Blockchain** - the Blockchain that stores the chain of blocks, pending transactions and contains the majority of the functions that control the

### Transaction Class

The transaction class contains 4 objects:

1. **sender_addr** - the address of the peer sending the transaction
2. **sender_priv_key** - the private key of the sending peer, which is used to ==**FILL THIS IN GRACE**==
3. **receiver_addr** - theaddress of the peer receiving the transaction
4. **amount** - the amount of currency being sent in the transaction
5. **timestamp** - the date and time (in UTC) that the transaction was created in the format: YYYY-MM-DD HH:MM:SS.μS
   - Example: 2021-05-31 15:38:58.931800

The transactions are timestamped always in Coordinated Universal Time (UTC) to maintain consistencies across all users regardless of location.

### Transaction Functions

#### init

```python
def __init__(self, sender_addr, sender_priv_key, receiver_addr, amount):
        self.sender_addr = sender_addr
        self.sender_priv_key = sender_priv_key
        self.receiver_addr = receiver_addr
        self.amount = amount
        self.timestamp = str(datetime.datetime.now())
```

### Block Class

The block class contains 6 objects:

1. **index** - an integer that serves as the block ID and its index in the chain
2. **nonce** - a positive integer that forces the hash of the block to begin with a certain number of 0 bits, also known as the difficulty; if the nonce does not force the block to begin with the specified number of 0 bits, then the block and its transactions are invalid
3. **transactions** - an array containing all the pending transactions at the time the block was created
4. **hash** - the hash of the block
5. **prev_hash** - the hash of the previous block
6. **timestamp** - the date and time (in UTC) that the block was created in the format: YYYY-MM-DD HH:MM:SS.μS
   - Example: 2021-05-31 15:38:58.931800

### Block Functions

#### init

```python
def __init__(self, index, nonce, transactions, hash, prev_hash):
    self.index = index
    self.nonce = nonce
    self.transactions = transactions
    self.prev_hash = prev_hash or (constants.DIFFICULTY *'0')
    self.hash = self.hash_block()
    self.timestamp = str(datetime.datetime.now())

```

#### hash_block

The `hash_block` function takes the nonce, transactions, and previous hash data from the block and uses it to compute the hash of the block.
Inputs: None
Outputs: block hash in hex form

#### num_transactions

The `num_transactions` property returns the length of the transactions list stored in the block.
Inputs: None
Outputs: number of transactions stored in the block

#### block_transactions

The `block_transactions` property returns the transactions list stored in the block.
Inputs: None
Outputs: a list containing the transactions stored in the block

### Blockchain Class

The blockchain class contains 3 4objects:

1. **chain** - an array that each block is added to; the blockchain
2. **pending_transactions** - an array of all transactions that have not yet been added to a block
3. **nodes** - gives the chain the ability to store multiple nodes
4. **build_genesis** - creates the initial block in the chain

### Blockchain Functions

The Blockchain class contains the following functions:

- init
- build_genesis
- add_block
- create_trans
- mine
- validate_proof_of_work
- proof_of_work
- block_validity
- chain_validity
- replace_chain
- last_block
- last_transaction
- pending_transactions
- full_chain

#### init

```python
def __init__(self):
    self._chain = []
    self._pending_transactions = []
    self.nodes = set()
    self.build_genesis()            # Creates the initial block in chain

```

#### build_genesis

The `build_genesis` automatically generates the first block in the blockchain when the chain is created. The genesis block hsa a index of 0, nonce of 0, and an empty list of transactions.
Inputs: None
Outputs: None, appends created genesis block to chain

#### add_block

The `add_block` appends the given block to the blockchain and empties the pending transactions class variable of the blockchain.
Inputs: block
Outputs: True if block is successfully added, else False
Called In: `mine`, `replace_chain`

#### compute_balance

The `compute_balance` iterates through the blockchain, and through every transaction stored in each block, calculating the amount of money a peer has sent and recieved in order to compute the balance in the peer's wallet
Inputs: peer_addr - the address of the peer, in this case the peer's public key
Outputs: balance
Called In: `validate_trans`

#### validate_trans

The `validate_trans` checks the validity of a created transaction before it is added to pending transactions by: 1) confirming that the amount specified in the transaction is not negative in order to prevent peers stealing from one another, 2) confirming that the peer has enough currency in their wallet to make the transaction
Inputs: sender_addr, amount
Outputs: False if either condition fails, else true
Called In: `create_trans`

#### create_trans

The `create_trans` creates a new transaction object, and after confirming its validity appends it to pending transactions
Inputs: sender_addr, sender_priv_key, receiver_addr, amount
Outputs: transaction, True if success, else None, False

#### mine

The `mine` creates a new block object and populates it with the proper variables including calling the proof of work function to set the correct nonce and hash and the add block function to append the block to the chain.
Inputs: None
Outputs: block if success, else None

#### proof_of_work

The `proof_of_work` iterates through potential nonces (starting from zero) until either the correct hash is found or it reaches the MAX_NONCE (the maximum number storable in a 32 bit number). For every nonce tested, the hash is computed and then checked to see if it has the proper number of leading 0s, which correspond to the difficulty (defaulted to 4, aka 0000). Upon successfully finding a valid hash, the function saves the nonce and hash values to the block.
Inputs: block, (optional) difficulty
Outputs: None, saves nonce and hash to block
Called In: `mine`

#### block_validity

The `block_validity` checks the validity of the block by: 1) confirming sequential indices to insure no missing or out of order blocks, 2) comparing the prev_hash of the current block to the hash of the previous block, 3) comparing the stored hash of the block with the computed hash of the block, 4) checking the timestamp to ensure no backdating.
Inputs: block, prev_block, (optional) verbose - if True prints errors that arise
Outputs: True or False depending on the test results
Called In: `chain_validity`

#### chain_validity

The `chain_validity` checks the validity of the whole blockchain by 1) comparing the genesis blocks, 2) iterating through the remainder of the chain calling the block_validity function and additionally checking that the index stored in the block matches the index used in the for loop
Inputs: chain_to_validate, (optional) verbose - if True prints errors that
Outputs: True or False depending on test results, and the index of the block that has an error if applicable
Called In: `replace_chain`

#### replace_chain

The `replace_chain` compares the chain to an inputed chain. If the new chain is longer (implies forking has occured) the chain is validated. If the new chain is longer and valid, all the blocks missing from the peer's chain are added from the compared chain
Inputs: new_chain
Outputs: True if chain is replaced, else False

#### last_block

The `last_block` property returns the last block of the chain.

#### last_transaction

The `last_transaction` property returns the last transaction in the pending transactions.

#### pending_transactions

The `pending_transactions` property returns the pending transactions list stored in the blockchain.

#### full_chain

The `full_chain` property returns the entire chain of blocks stored in the blockchain.

## P2P Network Protocol

### Psuedocode for major components

#### Peer.py

- Create a peer object
- Start a thread that receives messages from the tracker
  - Send the tracker its name and port number to be officially added
  - Receive and process requests from the tracker
- Continuously listen for incoming connection requests from other peers
  - When connection is established, create two threads: one to send messages to the peer and one to receive messages from the peer

#### Tracker.py

- Create a tracker object
- Continuously listen for incoming connection requests from newly joining peers
  - Once connection is established, start a new thread to communicate with the peer
    - Receive an initial message from peer containing the peer's name and port number
    - Broadcast message to all other peers in network to add this newly joined peer
    - Create a `peer` object (a helper object) to track information regarding the peer, and the object into a dictionary containing all peers in network

### APIs

#### Peer

```c

    def add_peer(self, name, neighbor_socket):  # add a peer to the network
    def join_network(self): # join the network
    def send_to_tracker(self, message): # send a message to the tracker
    def send_to_peer(self, peer, packet):   # send a message to the peer
    def broadcast(self, packet):    # broadcast a packet to all the peers
    def return_peer_in_majority(self):  # return a peer with the majority blockchain
```

### Data Structures

#### Peer

- dictionary to track `neighbor` objects. Key is name of the neighbor and value is the neighbor object
- neighbor object - tracks the name, connection socket, and thread for the peer
- dictionary to track the number of occurances for each last hash sent by peers

#### Tracker

- dictionary to track `peer` objects. The peer objects contain the name of the peer, its port number, and connection socket

### Protocol

Messages sent from peer-to-peer and peer-to-tracker will be formatted in a dictionary.

Each message will have a "type" key in the dictionary to denote the purpose of the message. Some "types" include:

- `block` to send a block
- `blockchain` to send a blockchain
- `add` to add a peer
- `remove` to remove a peer
- `change` to change name or port number
- `joined` to denote succesful joining

Each message will also have a `name` key in the dictionary to track the sender of the message.

Each dictionary may have more keys and values depending on the type of message. For example, if the type is "blockchain", there will be a key and value to store the blockchain of the peer. If the type is "remove", there will be a key and value to track the name of the peer that should be removed.

### Blockchain synchronization between peers

There are three possible scenarios in which the peer blockchains can be desynchronized:

- A new peer joins the network.
- Two blocks are mined at the same time by two different peers. (Forking)
- Corruption of one peer's blockchain, either modifying nonce/hash/transactions/index.

Scenario 1: When a new peer joins the network, it will request a copy of the current blockchain from another peer. Theoretically, all of the peers will have the same copy of the same blockchain; if they don't, then scenarios 2 and 3 will detect the inconsistency and synchronize the blockchains before sending an updated copy to the new peer.

Scenario 2: When two blocks are mined at the same time by two different peers, these blocks will contain the exact same index and timestamp. Thus, when the neighboring peers add these blocks to their chain, the first add will be successfully (regardless which block it adds first) while the addition of the second block signifies an invalid chain. In this case, the blockchain adds the block anyway while correcting the indices such that they are sequential.

When a peer detects invalidity, it will attempt to update its blockchain to a copy of the network's majority. This is done by requesting all of its neighboring peers to broadcast their last block; we can tally up the various chains in the network by looking at the hash of each peer's final block. Equivalent blockchains will have equivalent hashes in the last block. Once a majority has been determined, if the peer observed invalidity, it will request a copy of the blockchain from any one of the majority chain holders. In the event of mining two blocks at the same time, all peers will observe invalidity.

Scenario 3: This scenario is dealt with similar to scenario 2, except this time only one chain is invalid instead of all. Once all of the neighbor peers broadcast their chain, the peer can then request a blockchain from one of the majority peers that have the correct blockchain.

## Demo Application - Cryptocurrency Wallet

A Cryptocurrency wallet is a safe avenue where users can store their digital assets and funds. It can be used to send and receive money easily and help to possess full control over crypto holdings. The wallet keeps track of each peers balance of ExtraCreditPoint coins.

### Wallet Features

- RSA generated public and private key pair for secure transactions
  - The public key stored in your wallet will be used to receive the funds and can be searched for in the distributed ledger
  - The private key stored in your wallet is used to sign transactions and prove that the user owns the associated public key. It is also used to match the public address the currency to unlock and utilize funds
- Signing of transactions and validation of signatures for additional security
- Initial balance of 100 coins

### Wallet Functions

The Wallet class contains the following functions:

- init
- address
- sign
- verify_signature
- getKeys
- deposit
- withdraw

#### init

```python
def __init__(self):
    random = Random.new().read
    self.private_key = RSA.generate(1024, random)
    self.public_key = self.private_key.publickey()
    self.signer = PKCS1_v1_5.new(self.private_key)
    self.balance = 100
```

#### address

The `address` property returns the address of the wallet, which for simplicity is the public key.

#### sign

The `sign` function takes a message, encrypts it using SHA-256, saves the result to the signer property of the Wallet class, converts it to hex form, decodes it in ASCII, and returns the ASCII decode.
Inputs: message
Outputs: ASCII signature string

#### verify_signature

The `verify_signature` function uses the public key of the wallet and a message to verify the signature, adding to the security of the wallet and transactions.
Inputs: wallet_addr (same as peer_addr/public key of wallet), message, signature
Outputs: True or False

#### getKeys

The `sign` function returns the keys of the wallet and is used for the GUI.
Inputs: None
Outputs: private_key, public_key

#### deposit

The `deposit` function adds currency to the wallet if the inputted transaction's receiver address is the address of the wallet.
Inputs: transaction
Outputs: None, adds amount in transaction to balance of wallet

#### withdraw

The `withdraw` function subtracts currency from the wallet if the inputted transaction's sender address is the address of the wallet.
Inputs: transaction
Outputs: None, subtracts amount in transaction from balance of wallet

### GUI

==**KC FILL THIS IN**==
