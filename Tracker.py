# Group3: 404 Error
# 
# CS60, Group Project
# 
# To compile and run Tracker.py:
#   Tracker.py [tracker_port]

import threading
import pickle
import time
import socket
import sys

# track information of each peer
class Peer:
    def __init__(self, port, name, connection_socket):
        self.port = port
        self.name = name
        self.connection_socket = connection_socket

# thread for taking input and sending message to server
class newThread(threading.Thread): 
    def __init__(self, connection_socket, tracker): 
        threading.Thread.__init__(self) 
        self.connection_socket = connection_socket
        self.peer_dict = tracker.peer_dict
  
        # helper function to execute the threads
    def run(self): 
        # obtain peer port number of newly joined peer
        peer_info = pickle.loads(self.connection_socket.recv(1024))
        peer_port = peer_info["port"]
        peer_name = peer_info["name"]    # name

        # ensure name is unique
        while peer_info["name"] in self.peer_dict:
            
            message = pickle.dumps({
                "type": "change",
                "field": "name",
                "message": "{} is taken".format(peer_info["name"])
            })
            # message = message.encode()
            self.connection_socket.send(message)
            peer_info = pickle.loads(self.connection_socket.recv(1024))

        # ensure port number not taken
        while not (self.port_unique(peer_info["port"])):
            print(peer_info["port"])
            message = pickle.dumps({
                "type": "change",
                "field": "port",
                "message": "{} is taken".format(peer_info["port"])
            })

            self.connection_socket.send(message)
            peer_info = pickle.loads(self.connection_socket.recv(1024))
            
        peer_port = peer_info["port"]
        peer_name = peer_info["name"]    # name
        peer = Peer(peer_port, peer_name, self.connection_socket)   # new peer object

        self.connection_socket.send(pickle.dumps({
            "type": "joined",
            "port": peer_port,
            "name": peer_name
        }))

        # tell peers in the network to add this peer
        if (len(self.peer_dict) > 0):
            message = pickle.dumps({
                "type": "add",
                "port": peer_port,
                "name": peer_name
            })
            # message = message.encode()
            self.broadcast(message)

        self.peer_dict[peer_name] = peer  # add this peer to list of peers

        print("In network: ")
        for peer in self.peer_dict:
            print(peer)

        # receive messages from the peer
        while True:
            message = pickle.loads(self.connection_socket.recv(1024))

            # request from a peer to be removed from network
            if (message["type"] == "remove"):
                new_message = pickle.dumps({
                    "type": "remove",
                    "name": message["name"]
                })

                # tell all other peers in network to remove the peer
                for peer in self.peer_dict.values(): 
                    peer.connection_socket.send(new_message)

                self.peer_dict[message["name"]].connection_socket.close()
                self.peer_dict.pop(message["name"]) # remove the peer from the dictionary

                print(self.peer_dict)
                break

    # broadcast to peers
    def broadcast(self, packet):
        for peer in self.peer_dict.values():
            time.sleep(0.2)
            peer.connection_socket.send(packet)

    def port_unique(self, port):
        for peers in self.peer_dict.values():
            if port == peers.port:
                return False
        return True

class Tracker:
    def __init__(self, host, port):
        self.socket = createSocket(host, port)
        self.peer_dict = {}   # keep track of peer objects

        self.socket.listen(1)
        print("The server is ready to receive")

        while True:
            connection_socket, addr = self.socket.accept()
            thread = newThread(connection_socket, self)
            thread.start()  
        self.socket.close()

# creates the socket for server
def createSocket(host, port):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((host, port))
    return serverSocket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = int(sys.argv[1])       # Port to listen on (non-privileged ports are > 1023)

tracker = Tracker(HOST, PORT)
