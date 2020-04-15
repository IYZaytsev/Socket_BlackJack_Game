import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))
client_socket.setblocking(False)

while True:
    try:
        #This is the lobby loop, user can break out of it by entering 1 which starts the game for all users connected.
        while True:
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            print(message)
            # if game has started moves onto game loop
            if("Game has started..." in message):
                break
            
            #waiting for user input
            user_ans = input()
            if(user_ans == "1"):
                client_socket.send(f"{len(user_ans):<{HEADER_LENGTH}}".encode('utf-8') + user_ans.encode('utf-8'))
        #This is the lobby loop, user can break out of it by entering 1 which starts the game for all users connected.
        while True: 
            print("in game loop")
            break

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: {}'.format(str(e)))
        sys.exit()