<h1> <img src="https://i.imgur.com/4MOXfCU.png"
  width="90"
  height="90"
  style="float:left;">

# README.md
**CS60, 21S
Final Project
Peer-to-Peer Blockchain with Crypto Wallet Application**


**Group 3 - Error 404
Jason Chen, Grace King, Norman Kuang, Rehoboth Okorie**




## Overview

The assignment for this final project was to build a simplified peer-to-peer blockchain and an application to demonstrate its functionality. The goal of the project was for us to gain hands-on experience implementing a basic blockchain and testing it with a demo application.

The peer-to-peer network contains 1 tracker and can support at least 3 peers, all on the Thayer Babylon servers. The tracker maintains a list of peers, which is updated as peers join or leave the network. Additionally every peer is informed of updates to this list.

The blockchain has been implemented so that each peer can maintain a copy of the blockchain, mine to create a valid block, broadcast mined blocks to other peers, and verify and add a block to its local blockchain. The blockchain has also been designed to be resilient to invalid transactions, handle forks, and deal with modifications made to blocks. 

To demonstrate the peer-to-peer blockchain functionality, a cryptocurrency wallet application was implemented for the currency "Dartmouth Extra Credit Points", seen below.

<img src="https://i.imgur.com/4MOXfCU.png" width=200 align=right>



Additional features were implemented including:

* Application GUI - note, due to challenges, the GUI did not achieve functionality
* Multiple transactions inside a block
* Public/Private keys
* Signed transactions for extra security
* RSA encryption

## Program Structure

### Blockchain API

The blockchain API was divided into four files to run the program and 5 files for testing.

Program Files: 
* blockchain.py
* block.py
* transaction.py
* constants.py

Test Files:
* script.py
* test_block.py
* test_blockchain.py
* test_transaction.py
  
Test outputs can be found in the ```test_outputs``` folder.

### Peer-to-Peer Network

The peer-to-peer network was divided into 3 files to run the program was tested using the command line interface

Program Files: 
* Peer.py
* Tracker.py
* Helper_classes.py

### Demo Applicaiton: Cryptocurrency Wallet

The cryptocurrency wallet application was divided into one file to create the wallet.

Program Files: 
* wallet.py


## Code Compilation

To compile and run Peer.py:
- python3 Peer.py [peer_port] [peer_name] [tracker_port]

To compile and run Tracker.py:
- python3 Tracker.py [tracker_port]



### Dependencies

* Works with Python 3


For a full list of dependencies, including versions, please see ```requirements.txt```.
To install dependencies run ```pip install -r requirements.txt``` in the terminal


### Installation

1. Clone the [Github Repository](https://https://github.com/cs60-spring-2021/project-group3)
``` git clone https://github.com/cs60-spring-2021/project-group3.git```
2. Install dependencies
```pip install -r requirements.txt```
3. Run Tracker
4. Run Peers


## Code Usage

### Program Usage

To compile and run Peer.py:
- python3 Peer.py [peer_port] [peer_name] [tracker_port]

To compile and run Tracker.py:
- python3 Tracker.py [tracker_port]


## Assumptions

Please note that this program was created for educational purposes only. It is by no means intended to be used in a real scenario. The cryptocurrency in this program has no monetary value, except perhaps for extra credit points in a Dartmouth Computer Science course :yum: :crossed_fingers:.

## License

These Python programs create a peer-to-peer blockchain with a crypto wallet application built on top of it. 

MIT License

Copyright (c) 2021 Jason Chen, Grace King, Norman Kuang, Rehoboth Okorie

See ```license.txt``` for more information


## Acknowledgements

Thank you to Professor Xia Zhou, Qijia Shao, and Ho Man Colman Leung for their instruction, help, guidance, advice, and support throughout this project and the whole term. 

## References

The following resources were referenced in the building of this project:
[1]: https://github.com/bajcmartinez/blockchainpy
[2]: https://www.youtube.com/watch?v=x-P-nmhiO-
[3]: https://github.com/dvf/blockchain
[4]: https://github.com/adilmoujahid/blockchain-python-tutorial
[5]: http://adilmoujahid.com/posts/2018/03/intro-blockchain-bitcoin-python/
[6]: https://github.com/julienr/ipynb_playground/blob/master/bitcoin/dumbcoin/dumbcoin.ipynb
[7]: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
[8]: https://towardsdatascience.com/building-a-minimal-blockchain-in-python-4f2e9934101d
[9]: https://livecodestream.dev/post/from-zero-to-blockchain-in-python-part-1/
[10]: https://medium.com/swlh/introduction-to-blockchain-with-implementation-in-python-c12f8478a3c4
[11]: https://www.youtube.com/watch?v=_160oMzblY8
[12]: https://www.youtube.com/watch?v=xIDL_akeras
