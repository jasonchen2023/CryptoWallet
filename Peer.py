# Group3: 404 Error
# 
# CS60, Group Project
# 
# To compile and run Peer.py:
#   Peer.py [peer_port] [peer_name] [tracker_port]
# 
# NOTE:
# 
# Messages may be printed out of order (bc printing from multiple threads)
# 


import atexit
import sys
import socket
import pickle
import threading

import constants
from block import Block
from transaction import Transaction
from blockchain import Blockchain
from Helper_classes import displayText
import time


# tracks a neighbors name, and socket
class Neighbor:
    def __init__(self, name, connection_socket, n_thread):
        self.name = name
        self.connection_socket = connection_socket
        self.thread = n_thread


# thread to receive packets from neighbors
class neighborThread(threading.Thread):

    def __init__(self, peer, neighbor_socket):
        threading.Thread.__init__(self)
        self.peer = peer
        self.neighbor_socket = neighbor_socket
        self.keep_running = True

    def run(self):
        while self.keep_running:
            try:
                self.neighbor_socket.settimeout(10)

                try:
                    message = pickle.loads(self.neighbor_socket.recv(4096))
                    self.neighbor_socket.settimeout(None)

                    # receive blockchain update from peer
                    if message["type"] == "blockchain":
                        print("received blockchain from: ", message["name"])

                        blockchain = message["blockchain"]
                        for block in blockchain._chain:
                            print("block index: ", block.index)
                        # displayText("blockchain: ", message["blockchain"])

                        print("replacing chain")
                        self.peer.blockchain.replace_chain_simple(blockchain._chain)

                        self.peer.blockchain.print_chain()

                        self.peer.tally_dict = {}


       

                    # receive block from peer
                    
                    elif message["type"] == "block":
                        print("received block from: ", message["name"])

                        # print("block index: ", message["block"].index)

                        # try to add new block to BC
                        new_block = message["block"]
                        self.peer.blockchain.full_chain.append(new_block)
                        (valid, ind) = self.peer.blockchain.chain_validity(
                            self.peer.blockchain.full_chain)
                        

                        # self.peer.blockchain.print_chain()
                        
                        if (valid):
                            print("block valid, added to BC")

                            b = False
                            total = 0
                            for t in new_block.transactions:
                                
                                if (t.receiver_addr == self.peer.name):
                                    b = True
                                    total += t.amount
                                    
                            
                            if b:
                                
                                self.peer.balance += total      
                                print("Received " + str(total) + " from " + message["name"] + ". Your balance is: " + str(self.peer.balance))


                        else:
                            print("block invalid, recomputing BC")
                            self.peer.blockchain.recompute_chain_at_index(ind)

                            # BC good, may need to broadcast to neighbors


                            # broadcast request for last block from all peers in network

                            self.peer.broadcast(pickle.dumps({
                                "type": "last block request",
                                "name": self.peer.name
                            }))
                    
                    # send hash last block to peer
                    elif message["type"] == "last block request":

                        new_message = pickle.dumps({
                            "type": "last block tally",
                            "name": self.peer.name,
                            "block": self.peer.blockchain.last_block.hash
                        })
                        self.peer.send_to_peer(message["name"], new_message)

                    # receive hash of last block
                    elif message["type"] == "last block tally":

                        # enter the block hash into dictionary
                        if (message["block"] not in self.peer.tally_dict):
 
                            self.peer.tally_dict["block"] = []
                        
                        self.peer.tally_dict["block"].append(message["name"])   # dictionary with last block has as key and list of peers as value

                        
                        # once 
                        self.peer.neighbor_count += 1

                        if (self.peer.neighbor_count == len(self.peer.neighbor_dict.keys())):
                            
                            majority_peer = self.peer.return_peer_in_majority()
                            new_message = pickle.dumps({
                                "type": "send blockchain",
                                "name": self.peer.name
                            })
                        
                            self.peer.send_to_peer(message["name"], new_message)
                        

                    elif message["type"] == "send blockchain":
                        self.peer.send_to_peer(message["name"], pickle.dumps({
                            "type": "blockchain",
                            "name": self.peer.name,
                            "blockchain": self.peer.blockchain
                        }))
 

                      
                except EOFError as error:
                    break
            
            except socket.timeout as e:

                pass

    def stop_thread(self):
        self.keep_running = False

        # do something with the packet


# Currently taking input from stdin, but should be implemented in GUI form
class inputThread(threading.Thread):

    def __init__(self, peer):
        threading.Thread.__init__(self)
        self.peer = peer

    def run(self):


        print("Your balance is " + str(self.peer.balance))

        while True:

            if (self.peer.valid_identity == True):

                time.sleep(1.5)
                request = input("What is your request? deposit / transfer / withdrawal / mine / exit: ")

                while (request != "deposit" and request != "transfer" and request != "withdrawal" and request != "exit" and request != "mine"):
                    request = input("Invalid request Please enter deposit / transfer / withdrawal / mine / exit: ")

                # mine block
                if (request == "mine"):

                    block = self.peer.blockchain.mine()
                    self.peer.broadcast(pickle.dumps({
                        "type": "block",
                        "name": self.peer.name,
                        "block": self.peer.blockchain.last_block,

                    }))

                    print("Block mined and broadcasted ")
                    # testing that block was added
                    #self.peer.blockchain.print_chain()

                # deposit money
                if (request == "deposit"):
                    amt = input("How much would you like to deposit? ")

                    if not entry_valid(amt):
                        continue

                    amt = float(amt)

                    self.peer.blockchain.create_trans("deposit", "private key", self.peer.name, amt)


                    self.peer.balance += amt

                    print("Your balance is now: " + str(self.peer.balance))
                    # print("To add additional transactions, request 'transfer'. Else, to send request 'mine'.")
                    print("To process transaction, enter 'mine'.")
                

                # withdraw money
                if (request == "withdrawal"):

                    amt = input("How much would you like to withdraw? ")

                    
                    if not entry_valid(amt):
                        continue

                    amt = float(amt)

                    while amt > self.peer.balance:
                        amt = float(input("ERROR: Your balance is " + str(self.peer.balance) + ". Please re-enter amount:  "))
        
                        continue

                    self.peer.blockchain.create_trans("withdrawal", "private key", self.peer.name, amt)

                    self.peer.balance -= amt

                    print("Your balance is now: " + str(self.peer.balance))     
                    # print("To add additional transactions, request 'transfer'. Else, to send request 'mine'.")
                    print("To process transaction, enter 'mine'.")


                # transfer money
                elif (request == "transfer"):

                    check = input("Please enter: [recipient] [amount] ")
                    
                    check = check.split()
                    if (len(check) != 2):
                        print("invalid entry")
                        continue

                    recipient = check[0]


                    if not entry_valid(check[1]):
                        continue

                    amt = float(check[1])

                    # recipient not in network
                    while (recipient not in self.peer.neighbor_dict.keys()):
                        recipient = input("Recipient not in network. Please enter a different recipient: ")

                    # transfer amount greater than deposit
                    while (amt > self.peer.balance):
                        amt = float(input("Cannot transfer " + str(amt) + ". Your balance is " + str(self.peer.balance) + ". Enter a smaller amount: " )    )

                        if not entry_valid(amt):
                            continue

                    self.peer.blockchain.create_trans(self.peer.name, "private key", recipient, amt)

                    self.peer.balance -= amt


                    print("Your balance is now: " + str(self.peer.balance))


                    print("To process transaction, enter 'mine'.")
                
                
                # peer exiting
                elif (request == "exit"):

                    self.peer.send_to_tracker("remove")
                    print("Input thread exited")
            
                    exit()
                        
                    
             



# thread for processing messages sent by the tracker or neighbors (peers)
class trackerThread(threading.Thread):

    def __init__(self, peer):
        threading.Thread.__init__(self)
        self.peer = peer

        # helper function to execute the threads

    def run(self):

        self.peer.join_network()

        while True:

            message = pickle.loads(self.peer.tracker_socket.recv(1024))

            # must change name or port
            if (message["type"] == "change"):

                # name invalid
                if (message["field"] == "name"):
     
                    self.peer.name = input("Enter a different name: ")
                    self.peer.join_network()

                # port invalid
                elif (message["field"] == "port"):

                    port_num = input("Enter a different port number: ")

                    while not is_digit(port_num):
                        port_num = input("Port number must be a number: ")
                    self.peer.peer_port = int(port_num)
                    self.peer.join_network()


            # successfully joined
            elif (message["type"] == "joined"):
                self.peer.valid_identity = True

            # add a newly joined peer
            elif (message["type"] == "add"):

                neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                neighbor_socket.connect(('127.0.0.1', int(message["port"])))  # message one = port number of peer

                new_message = pickle.dumps({
                    "type": "add",
                    "name": self.peer.name,
                    "blockchain": self.peer.blockchain
                })
                neighbor_socket.send(new_message)
                self.peer.add_peer(message["name"], neighbor_socket)

            # remove a peer from the dict
            elif (message["type"] == "remove"):

                # exit out of this thread if we are requesting to be removed
                if (message["name"] == self.peer.name):

                    self.peer.t_thread_exited = True

                    print("Tracker thread exited")
                    exit()
                    # break

                # another peer leaving
                neighbor = self.peer.neighbor_dict.get(message["name"], None)
                if neighbor:
                    neighbor.thread.stop_thread()
                    self.peer.neighbor_dict[message["name"]].connection_socket.close()
                    self.peer.neighbor_dict.pop(message["name"])

                    print(message["name"], " removed")

                    print("In network:")
                    for peer in self.peer.neighbor_dict.keys():
                        print(peer)


class Peer:

    def __init__(self, name, peer_port, tracker_port):
        self.name = name
        self.valid_identity = False
        self.tracker_port = tracker_port
        self.peer_port = peer_port
        self.tracker_socket = self.create_tracker_socket()
        # self.server_socket = self.createSocket()
        self.neighbor_dict = {}
        self.blockchain = Blockchain()
        self.t_thread_exited = False
        self.tally_dict = {}
        self.neighbor_count = 0
        self.balance = 100

        # thread to receive messages from tracker
        t_thread = trackerThread(self)
        t_thread.start()

        # take commands from stdin (will be implemented in GUI)
        input_thread = inputThread(self)
        input_thread.start()

        while (self.valid_identity == False):
            pass

        self.server_socket = self.createSocket()
        self.server_socket.listen()
        

        # listen and accept connection requests from other peers (when first setting up network)
        while True:

            try:
            
                self.server_socket.settimeout(10)

                neighbor_socket, addr = self.server_socket.accept()
                message = pickle.loads(neighbor_socket.recv(4096))

                if (message["type"] == "add"):
                    self.add_peer(message["name"], neighbor_socket)

                    # replace current blockchain with neighbor's
                    blockchain = message["blockchain"]
                    self.blockchain.replace_chain_simple(blockchain._chain)
            
            except socket.timeout as e:
            
                # break if we are leaving the network
                if (self.t_thread_exited == True):
                    break
 

        # close all neighbor connection sockets and threads
        for nbr in self.neighbor_dict.values():
            nbr.connection_socket.close()
            nbr.thread.stop_thread()

        # self.tracker_socket.close()
        self.server_socket.close()


    # creates the socket to communicate with tracker
    def create_tracker_socket(self):
        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.connect(('127.0.0.1', self.tracker_port))  # tup[0] = neighbor port
        return tracker_socket

    # creates the socket for server
    def createSocket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', self.peer_port))
        return server_socket

    # adds a peer to the network
    def add_peer(self, name, neighbor_socket):

        n_thread = neighborThread(self, neighbor_socket)
        n_thread.start()

        neighbor = Neighbor(name, neighbor_socket, n_thread)
        self.neighbor_dict[name] = neighbor

        print(name + " joined network")

    # send our port number and name to the tracker
    def join_network(self):
        global PORT
        info = pickle.dumps({
            "type": "add",
            "port": self.peer_port,
            "name": self.name
        })
        self.tracker_socket.send(info)

    # send a message to the tracker
    def send_to_tracker(self, message):

        # format the message
        self.tracker_socket.send(
            pickle.dumps({
            "type": "remove",
            "name": self.name,
            "message": message
        }))



    # send a packet to peer
    def send_to_peer(self, peer, packet):
        peer_socket = self.neighbor_dict[peer].connection_socket
        peer_socket.send(packet)


    # broadcast a packet to peers
    def broadcast(self, packet):
        for peer in self.neighbor_dict.values():
            peer_socket = peer.connection_socket
            peer_socket.send(packet)

    # return a peer with majority last_hash
    def return_peer_in_majority(self):
        maximum = 0
        majority = None
        for last_hash in self.tally_dict.keys():
            if len(self.tally_dict[last_hash]) > maximum:
                maximum = len(self.tally_dict[last_hash])
                majority = last_hash

        print("last hash: ", majority)
        print(self.tally_dict)
        return (self.tally_dict[last_hash][0])




# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
def is_digit(input_str):
    return input_str.strip().isdigit()

def is_float(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

# returns whether entry is a number that's greater than 0
def entry_valid(amt):

    if not is_float(amt):
        print("Error: not a number ")
        return False

    amt = float(amt)
    if (amt < 0):
        print("Error: Deposit amount negative ")
        return False

    return True


if (is_digit(sys.argv[1]) and is_digit(sys.argv[3])):
    peer_port = int(sys.argv[1])  # Port to listen on (non-privileged ports are > 1023)
    NAME = sys.argv[2]
    TRACKER_PORT = int(sys.argv[3])
    Peer(NAME, peer_port, TRACKER_PORT)

else:
    print("port number must be a number")
