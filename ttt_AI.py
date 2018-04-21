#! /usr/bin/python3

# Import the socket module
import socket
# Import command line arguments
from sys import argv
from database.memory import ShortMemory
from database.memory import LongMemory


class TTTClient:
    """TTTClient deals with networking and communication with the TTTServer."""

    def __init__(self):
        """Initializes the client and create a client socket."""
        # Create a TCP/IP socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, address, port_number):
        """Keeps repeating connecting to the server and returns True if
        connected successfully."""
        while True:
            try:
                print("Connecting to the game server...")
                # Connection time out 10 seconds
                self.client_socket.settimeout(10)
                # Connect to the specified host and port
                self.client_socket.connect((address, int(port_number)))
                # Return True if connected successfully
                return True
            except:
                # Caught an error
                print("There is an error when trying to connect to " +
                      str(address) + "::" + str(port_number))
                self.__connect_failed__()
        return False

    def __connect_failed__(self):
        """(Private) This function will be called when the attempt to connect
        failed. This function might be overridden by the GUI program."""
        # Ask the user what to do with the error
        choice = input("[A]bort, [C]hange address and port, or [R]etry?")
        if (choice.lower() == "a"):
            exit()
        elif (choice.lower() == "c"):
            address = input("Please enter the address:")
            port_number = input("Please enter the port:")

    def s_send(self, command_type, msg):
        """Sends a message to the server with an agreed command type token
        to ensure the message is delivered safely."""
        # A 1 byte command_type character is put at the front of the message
        # as a communication convention
        try:
            self.client_socket.send((command_type + msg).encode())
        except:
            # If any error occurred, the connection might be lost
            self.__connection_lost()

    def s_recv(self, size, expected_type):
        """Receives a packet with specified size from the server and check
        its integrity by comparing its command type token with the expected
        one."""
        try:
            msg = self.client_socket.recv(size).decode()
            # If received a quit signal from the server
            if (msg[0] == "Q"):
                why_quit = ""
                try:
                    # Try receiving the whole reason why quit
                    why_quit = self.client_socket.recv(1024).decode()
                except:
                    pass
                # Print the resaon
                print(msg[1:] + why_quit)
                # Throw an error
                raise Exception
            # If received an echo signal from the server
            elif (msg[0] == "E"):
                # Echo the message back to the server
                self.s_send("e", msg[1:])
                # Recursively retrive the desired message
                return self.s_recv(size, expected_type)
            # If the command type token is not the expected type
            elif (msg[0] != expected_type):
                print("The received command type \"" + msg[0] + "\" does not " +
                      "match the expected type \"" + expected_type + "\".")
                # Connection lost
                self.__connection_lost()
            # If received an integer from the server
            elif (msg[0] == "I"):
                # Return the integer
                return int(msg[1:])
            # In other case
            else:
                # Return the message
                return msg[1:]
            # Simply return the raw message if anything unexpected happended
            # because it shouldn't matter any more
            return msg
        except:
            # If any error occurred, the connection might be lost
            self.__connection_lost()
        return None

    def __connection_lost(self):
        """(Private) This function will be called when the connection is lost."""
        print("Error: connection lost.")
        try:
            # Try and send a message back to the server to notify connection lost
            self.client_socket.send("q".encode())
        except:
            pass
        # Raise an error to finish
        raise Exception

    def close(self):
        """Shut down the socket and close it"""
        # Shut down the socket to prevent further sends/receives
        self.client_socket.shutdown(socket.SHUT_RDWR)
        # Close the socket
        self.client_socket.close()


class AiPlayer(TTTClient):
    """TTTClientGame deals with the game logic on the client side."""
    board_content = []
    command = ""
    ## play_as = 'X' or 'O'
    play_as = ''
    command = ""
    agent_move = -1
    agent_last_move = -1
    opp_move = -1
    opp_last_move = -1

    def __init__(self):
        """Initializes the client game object."""
        TTTClient.__init__(self)
        self.shortMemory = ShortMemory()
        self.longMemory = LongMemory()

    def start_game(self):
        """Starts the game and gets basic game information from the server."""
        # Receive the player's ID from the server
        self.player_id = int(self.s_recv(128, "A"))
        # Confirm the ID has been received
        self.s_send("c", "1")

        # Tell the user that connection has been established
        self.__connected__()

        # Receive the assigned role from the server
        self.role = str(self.s_recv(2, "R"))
        # Confirm the assigned role has been received
        self.s_send("c", "2")

        # Receive the mactched player's ID from the server
        self.match_id = int(self.s_recv(128, "I"))
        # Confirm the mactched player's ID has been received
        self.s_send("c", "3")

        print(("You are now matched with player " + str(self.match_id)
               + "\nYou are the \"" + self.role + "\""))

        # Call the __game_started() function, which might be implemented by
        # the GUI program to interact with the user interface.
        self.__game_started__()
        # Start the main loop
        self.__main_loop()

    def __connected__(self):
        """(Private) This function is called when the client is successfully
        connected to the server. This might be overridden by the GUI program."""
        # Welcome the user
        print("Welcome to Tic Tac Toe online, player " + str(self.player_id)
              + "\nPlease wait for another player to join the game...")

    def __game_started__(self):
        """(Private) This function is called when the game is getting started."""
        # This is a virtual function
        # The actual implementation is in the subclass (the GUI program)
        return

    def __main_loop(self):
        """The main game loop."""
        while True:
            # Get the board content from the server
            self.board_content = self.s_recv(10, "B")
            # Get the command from the server
            self.command = self.s_recv(2, "C")
            # Update the board

            self.__update_board__()
            if (self.command == "Y"):
                # If it's this player's turn to move
                self.make_move(self.board_content)
            elif (self.command == "N"):
                # If the player needs to just wait
                self.__player_wait__()
                # Get the move the other player made from the server
                move = self.s_recv(2, "I")
                self.__opponent_move_made__(move)
            elif (self.command == "D"):
                # If the result is a draw
                print("It's a draw.")
                break
            elif (self.command == "W"):
                # If this player wins
                print("You WIN!")
                # Draw winning path
                self.__draw_winning_path__(self.s_recv(4, "P"))
                # Break the loop and finish
                break
            elif (self.command == "L"):
                # If this player loses
                print("You lose.")
                # Draw winning path
                self.__draw_winning_path__(self.s_recv(4, "P"))
                # Break the loop and finish
                break
            else:
                # If the server sends back anything unrecognizable
                # Simply print it
                print("Error: unknown message was sent from the server")
                # And finish
                break

    def __update_board__(self):
        """(Private) Updates the board. This function might be overridden by
        the GUI program."""
        if (self.command == "Y"):
            # If it's this player's turn to move, print out the current
            # board with " " converted to the corresponding position number

            print("Current board:\n" + AiPlayer.format_board(
                self.show_board_pos()))
        else:
            # Print out the current board
            print("Current board:\n" + AiPlayer.format_board(
                self.board_content))

    def __player_wait__(self):
        """(Private) Lets the user know it's waiting for the other player to
        make a move. This function might be overridden by the GUI program."""
        print("Waiting for the other player to make a move...")

    def __opponent_move_made__(self, move):
        """(Private) Shows the user the move that the other player has taken.
        This function might be overridden by the GUI program."""
        print("Your opponent took up number " + str(move));

        # Saves the oppenent's last move before overwriting
        self.opp_last_move = self.opp_move

        # Updates to the current move
        self.opp_move = self.opp_move - 1

    def __draw_winning_path__(self, winning_path):
        """(Private) Shows to the user the path that has caused the game to
        win or lose. This function might be overridden by the GUI program."""
        # Generate a new human readable path string
        readable_path = ""
        for c in winning_path:
            readable_path += str(int(c) + 1) + ", "

        print("The path is: " + readable_path[:-2])

    def show_board_pos(self):
        """(Static) Converts the empty positions " " (a space) in the board
        string to its corresponding position index number."""
        new_s = list("123456789")
        for i in range(0, 8):
            if (self.board_content[i] != " "):
                new_s[i] = self.board_content[i]
        return "".join(new_s)

    def format_board(s):
        """(Static) Formats the grid board."""

        # If the length of the string is not 9
        if (len(s) != 9):
            # Then print out an error message
            print("Error: there should be 9 symbols.")
            # Throw an error
            raise Exception

        # Draw the grid board
        # print("|1|2|3|")
        # print("|4|5|6|")
        # print("|7|8|9|")
        return ("|" + s[0] + "|" + s[1] + "|" + s[2] + "|\n"
                + "|" + s[3] + "|" + s[4] + "|" + s[5] + "|\n"
                + "|" + s[6] + "|" + s[7] + "|" + s[8] + "|\n")

    def make_move(self, position):
        """(Private) Lets the user input the move and sends it back to the
        server. This function might be overridden by the GUI program."""
        while True:
            # Prompt the user to enter a position
            try:
                position = int(input('Please enter the position (1~9):'))
                print(self.opponent_pos())
            except:
                print("Invalid input.")
                continue

            # Ensure user-input data is valid
            if (position >= 1 and position <= 9):
                # If the position is between 1 and 9
                if (self.board_content[position - 1] != " "):
                    # If the position is already been taken,
                    # Print out a warning
                    print("That position has already been taken." +
                          "Please choose another one.")
                else:
                    # Save the previous move
                    self.agent_last_move = self.agent_move

                    # Update the current move
                    self.agent_move = position - 1

                    # If the user input is valid, break the loop
                    if not self.shortMemory.save(board_before=self.board_content, move=position, role=self.role, is_new=True):
                        print("Database Error")
                    break
            else:
                print("Please enter a value between 1 and 9 that" +
                      "corresponds to the position on the grid board.")
        # Loop until the user enters a valid value

        # Send the position back to the server
        self.s_send("i", str(position))

    def opponent_pos(self):
        opponent = []
        agentSymbol = self.agent_role()
        if agentSymbol == 'X':
            oppSymbol = 'O'
        else:
            oppSymbol = 'X'
        for i in self.board_content:
            if i == oppSymbol:
                opponent.append(i)

        return opponent

    def agent_pos(self):
        agent = []
        agentsymbol = self.agent_role()
        for i in self.board_content:
            if i == agentsymbol:
                agent.append(i)

        return agent

    def is_game_over():
        if self.is_won() or self.is_draw()
            self.shortMemory.save(board_before=self.board_content, move=position, role=self.role, is_new=True)
            return True
        else
            return False

    def is_draw(self):
        Full = True
        for i in range(0,8):
            if board[i] == " ":
               Full = False

        if Full == True:
            print "It is draw."
            return True
        else
            return False

    def is_won(board_content,position):
        if  (board_content[0] == agent_move and board_content[1] == agent_move and board_content[2 ] == agent_move) or
            (board_content[3] == agent_move and board_content[4] == agent_move and board_content[5] == agent_move) or
            (board_content[6] == agent_move and board_content[7] == agent_move and board_content[8] == agent_move) or
            (board_content[0] == agent_move and board_content[3] == agent_move and board_content[6] == agent_move) or
            (board_content[1] == agent_move and board_content[4] == agent_move and board_content[7] == agent_move) or
            (board_content[2] == agent_move and board_content[5] == agent_move and board_content[8] == agent_move) or
            (board_content[0] == agent_move and board_content[4] == agent_move and board_content[8] == agent_move) or
            (board_content[2] == agent_move and board_content[4] == agent_move and board_content[6] == agent_move):
            print ("you have won!")
            return True
        else
            return False

    def agent_role(self):
        if self.role == 'X':
            return 'X'
        elif self.role == 'O':
            return 'O'

    def opponent_role(self):
        if self.role == 'X':
            return 'O'
        elif self.role == 'O':
            return 'X'

    def opponent_last_move(self):
        return self.opp_last_move

    def agent_last_move(self):
        return self.agent_last_move

    def all_avaiable_pos(self):
        return False

    def position_score(position):
        return 100


# Define the main program
def main():
    # If there are more than 3 arguments
    if (len(argv) >= 3):
        # Set the address to argument 1, and port number to argument 2
        address = argv[1]
        port_number = argv[2]
    else:
        # Ask the user to input the address and port number
        address = input("Please enter the address:")
        port_number = input("Please enter the port:")

    # Initialize the agent object
    agent = AiPlayer()
    # Connect to the server
    agent.connect(address, port_number)
    try:
        # Start the game
        agent.start_game()
    except:
        print(("Game finished unexpectedly!"))
    finally:
        # Close the agent
        agent.close()


if __name__ == "__main__":
    # If this script is running as a standalone program,
    # start the main program.
    main()
