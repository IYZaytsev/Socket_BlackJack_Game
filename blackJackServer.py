import socket
import select
import random

#Creating a TCP socket
#AF_INET means IPV4
#SOCK_STREAM means TCP
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#SO_REUSEADDR  is being set to 1(true), if program is restarted TCP socket we created can be used again
#without waiting for a for the socket to be fully closed. 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#binding socket and listening for connections
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}
number_of_usr = 0;
waitingForGameToStart = True
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return client_socket.recv(message_length).decode('utf-8')

    except:
        return False


#Waiting for players to join lobby and to start game 
while waitingForGameToStart:
    #checking to see whats up with all sockets, every iteration. Keeping a list 
    #of all sockets that have connected and server_socket is first in that list 
    read_sockets, _, _ = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        # server_socket is being connected to, new user
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            #adding client socket to list of users   
            sockets_list.append(client_socket)
            print("User Joined !")
            #Giving player a number and storing it in a clients dictionary
            number_of_usr += 1
            clients[client_socket] = number_of_usr

            message = f"Welcome player {number_of_usr} to blackjack server, waiting for players to connect...(press 1 to start game)"
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
        # Some user has requested to start a game with the current lobby
        else:
            message = receive_message(notified_socket)
            if(message == "1"):
                print(f"player{clients[notified_socket]} wants to start game")
                game_start_notify = f"Game has started... (started by player{clients[notified_socket]})"
                #notifying all other clients that game has be initiated
                for client_socket in clients:
                    client_socket.send(f"{len(game_start_notify):<{HEADER_LENGTH}}".encode('utf-8') + game_start_notify.encode('utf-8'))
            # After all clients have been notified, breakout out of while loop to start the game loop.
            waitingForGameToStart = False

# This is the start of the game loop
# Creating a card deck of 13 cards of each suite
facecards_pip = {10: "Jack", 11: "Queen", 12: "King", 13: "Ace"}
while True:
    currentCards = {}
    messageString = ""
    # Dealing each player two cards and then sending out the results 
    for currentTurn in range(1, len(sockets_list)):
        currentCards[currentTurn] = []

    for currentTurn in range(1, len(sockets_list)):  
        currentCards[currentTurn].append(random.randrange(1,14))
        currentCards[currentTurn].append(random.randrange(1,14))

    for currentTurn in range(1, len(sockets_list)):
        card1_value = currentCards[currentTurn][0]
        card2_value = currentCards[currentTurn][1]
        card1 = facecards_pip.get(card1_value, card1_value) 
        card2 = facecards_pip.get(card2_value, card2_value) 
        print(f"cards are {card1} and {card2} \n")
    break