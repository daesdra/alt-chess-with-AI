import copy 
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def location2index(loc: str) -> tuple[int, int]:
    # From a location string, convert letter -> x, number -> y (board indexing starts at 1,1).
    x = ord(loc[0]) - ord('a') + 1
    y = int(loc[1:])

    logging.debug(f"{loc} has been converted to {x, y}.")
    return (x, y)
	
def index2location(x: int, y: int) -> str:
    # From tuple of x, y, convert x -> letter, y -> number.
    letter = chr(x + ord('a') - 1)

    logging.debug(f"{x, y} has been converted to {letter}{y}.")
    return f"{letter}{y}" # Location string. 

class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_

    def can_reach(self, pos_X: int, pos_Y: int, B) -> bool:
        raise NotImplementedError('Subclass should implement this method "can_reach".')

    def can_move_to(self, pos_X: int, pos_Y: int, B) -> bool:
        raise NotImplementedError('Subclass should implement this method "can_move_to".')

    def move_to(self, pos_X: int, pos_Y: int, B):
        raise NotImplementedError('Subclass should implement this method "move_to".')       

Board = tuple[int, list[Piece]]

def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y: 
            logging.debug(f"There is a piece at {pos_X, pos_Y}.")
            return True
        
    logging.debug(f"There is not a piece at {pos_X, pos_Y}.")
    return False

def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            logging.debug(f"Piece at {pos_X, pos_Y}: {piece}.")
            return piece
    return None

class Bishop(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        super().__init__(pos_X, pos_Y, side_)
        if side_ :
            logging.debug(f"A white bishop has been created at {pos_X, pos_Y}.")
        else:
            logging.debug(f"A black bishop has been created at {pos_X, pos_Y}.")
	
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        # Bishop movement capabilities (diagonal movement only).
        dx = abs(self.pos_x - pos_X)
        dy = abs(self.pos_y - pos_Y)

        # Check if movement is within bishop's movement capabilities. 
        if dx != dy:
            logging.debug(f"Bishop cannot reach ({pos_X}, {pos_Y}) from ({self.pos_x}, {self.pos_y}) - not a diagonal movement.")
            return False      

        # Check if movement is on the board. 
        if not (1 <= pos_X <= B[0] and 1 <= pos_Y <= B[0]):
            logging.debug(f"Bishop cannot reach ({pos_X}, {pos_Y}) - out of board bounds.")
            return False        

        # Check if there is another piece in the way of the final destination. 
            # Determine the direction of the bishop's movement.
        x_step = 1 if pos_X > self.pos_x else -1
        y_step = 1 if pos_Y > self.pos_y else -1
            # Check that each square in the path to the final destination is clear. 
        x, y = self.pos_x + x_step, self.pos_y + y_step

        while x != pos_X or y != pos_Y: # While the bishop is not yet at the final destination,   
            if is_piece_at(x, y, B):
                logging.debug(f"Bishop blocked at ({x}, {y}) while moving to ({pos_X}, {pos_Y}).")
                return False
            x += x_step # check the next square in the path. 
            y += y_step 
        
        # Check that the final destination is either empty or not of the same side. 
        if is_piece_at(pos_X, pos_Y, B):
            target_piece = piece_at(pos_X, pos_Y, B)
            if target_piece.side == self.side:
                logging.debug(f"Bishop blocked by own piece at ({pos_X}, {pos_Y}).")
                return False
            logging.debug(f"Bishop can capture {target_piece} at ({pos_X}, {pos_Y}).")

        logging.debug(f"Bishop at ({self.pos_x}, {self.pos_y}) can reach ({pos_X}, {pos_Y}).")
        return True # The bishop can reach the destination.  

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        # Do not allow a bishop to move to its current position.
        if self.pos_x == pos_X and self.pos_y == pos_Y:
            logging.debug(
                f"{self.__class__.__name__} at ({self.pos_x}, {self.pos_y}) cannot move to its current position.")
            return False

        # Backup the piece list. 
        B = copy.deepcopy(B)

        # Firstly, check if the bishop cannot reach (per can_reach method).
        if not self.can_reach(pos_X, pos_Y, B):
            logging.debug(f"Bishop cannot reach ({pos_X}, {pos_Y}).")
            return False
        
        # Secondly, check if the result of the move is a capture,
        # if yes, find the piece captured using piece_at.
        captured_piece = None
        if is_piece_at(pos_X, pos_Y, B):
            captured_piece = piece_at(pos_X, pos_Y, B)
            if captured_piece.side == self.side:
                logging.debug(f"Bishop cannot capture own piece at ({pos_X}, {pos_Y}).")
                return False # Cannot capture a piece of the same side.

        # Store the original position.
        original_pos_x, original_pos_y = self.pos_x, self.pos_y
        self.pos_x, self.pos_y = pos_X, pos_Y
        
        # Handle a capture, if any.
        if captured_piece: 
            B = (B[0], [p for p in B[1] if p != captured_piece])

        # Check for check.
        if is_check(self.side, B):
            # Restore the original position of the board.
            self.pos_x, self.pos_y = original_pos_x, original_pos_y
            return False
        
        # Restore the original position of the board.
        self.pos_x, self.pos_y = original_pos_x, original_pos_y

        logging.debug(f"Bishop at ({self.pos_x}, {self.pos_y}) can move to ({pos_X}, {pos_Y}).")
        return True # The bishop can move to the new location.

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        # Check if the bishop can move to the new location.
        if not self.can_move_to(pos_X, pos_Y, B):
            logging.debug(f"Bishop cannot move to ({pos_X}, {pos_Y}).")
            return B
        
        # Remove the captured piece, if any. 
        captured_piece = None
        if is_piece_at(pos_X, pos_Y, B): # There is an enemy piece (do not have to specify if self or not because can_reach check already does this).
            captured_piece = piece_at(pos_X, pos_Y, B)
            B[1].remove(captured_piece)
            logging.debug(f"The bishop has captured {captured_piece} at {pos_X, pos_Y}. The piece is {captured_piece}.")

        # Move the bishop to the new position. 
        self.pos_x = pos_X
        self.pos_y = pos_Y 
        logging.debug(f"You have moved your bishop to: {pos_X, pos_Y}.")

        return B # return the new board

class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        super().__init__(pos_X, pos_Y, side_)
        if side_:
            logging.debug(f"A white king has been created at {pos_X, pos_Y}.")
        else:
            logging.debug(f"A black king has been created at {pos_X, pos_Y}.")

    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        # King's movement capabilities (1 tile at a time, in any direction).
        dx = abs(self.pos_x - pos_X)
        dy = abs(self.pos_y - pos_Y)

        # Check if the movement is within the king's movement capabilities.
        if dx > 1 or dy > 1:
            logging.debug(f"King cannot reach ({pos_X}, {pos_Y}) from ({self.pos_x}, {self.pos_y}) - not a valid king movement type.")
            return False

        # Check if movement is on the board. 
        if not (1 <= pos_X <= B[0] and 1 <= pos_Y <= B[0]):
            logging.debug(f"King cannot reach ({pos_X}, {pos_Y}) - out of board bounds.")
            return False 
        
        # Check that the final destination is either empty or not of the same side. 
        if is_piece_at(pos_X, pos_Y, B):
            target_piece = piece_at(pos_X, pos_Y, B)
            if target_piece.side == self.side:
                logging.debug(f"King blocked by own piece at ({pos_X}, {pos_Y}).")
                return False
            logging.debug(f"King can capture {target_piece} at ({pos_X}, {pos_Y}).")

        logging.debug(f"Bishop at ({self.pos_x}, {self.pos_y}) can reach ({pos_X}, {pos_Y}).")
        return True # The king can reach the destination.

    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        # Do not allow a king to move to its current position.
        if self.pos_x == pos_X and self.pos_y == pos_Y:
            logging.debug(
                f"{self.__class__.__name__} at ({self.pos_x}, {self.pos_y}) cannot move to its current position.")
            return False
        
        # Backup the pieces list.
        B = copy.deepcopy(B)
            
        # Firstly, check if the king cannot reach (per can_reach method).
        if not self.can_reach(pos_X, pos_Y, B):
            logging.debug(f"King cannot reach ({pos_X}, {pos_Y}).")
            return False

        # King can not move next to a king. 
        for piece in B[1]:
            if isinstance(piece, King) and piece.side != self.side:
                if abs(piece.pos_x - pos_X) <= 1 and abs(piece.pos_y - pos_Y) <= 1:
                    logging.debug(f"King cannot move next to an enemy king.")
                    return False
                
        # Store the original position. 
        original_pos_x, original_pos_y = self.pos_x, self.pos_y
        self.pos_x, self.pos_y = pos_X, pos_Y

        # Handle a capture, if any. 
        captured_piece = None
        if is_piece_at(pos_X, pos_Y, B): # There is an enemy piece. 
            captured_piece = piece_at(pos_X, pos_Y, B)
            B[1].remove(captured_piece)

        # Finally, check if the new configuration puts one's own king in check,
        # if yes, king in check, return False because invalid move.
        if is_check(self.side, B):
            # Restore the original position if it causes a check.
            self.pos_x, self.pos_y = original_pos_x, original_pos_y
            return False

        # Restore original position after the simulation.
        self.pos_x, self.pos_y = original_pos_x, original_pos_y

        logging.debug(f"King at ({self.pos_x}, {self.pos_y}) can move to ({pos_X}, {pos_Y}).")
        return True # The king can move to the new location.

    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        # Check if the king can move to the new location.
        if not self.can_move_to(pos_X, pos_Y, B):
            logging.debug(f"King cannot move to ({pos_X}, {pos_Y}).")
            return B
        
        # Remove the captured piece, if any. 
        captured_piece = None
        if is_piece_at(pos_X, pos_Y, B): # There is an enemy piece. 
            captured_piece = piece_at(pos_X, pos_Y, B)
            B[1].remove(captured_piece) 
            logging.debug(f"The king has captured a piece at {pos_X, pos_Y}. The piece is {captured_piece}")

        # Move the king to the new location.
        self.pos_x = pos_X
        self.pos_y = pos_Y
        logging.debug(f"You have moved your king to: {pos_X, pos_Y}.")

        return B # return the new board        

def is_check(side: bool, B: Board) -> bool:
    # Step 1, find the King's position. 
    for piece in B[1]:
        if piece.side == side and isinstance(piece, King):
            king_location = (piece.pos_x, piece.pos_y)
            logging.debug(f"King located at: {king_location}.")
            break

    if not king_location:
        raise ValueError("Could not find a king on the board. Check configuration text file.")

    # Step 2, check if any enemy piece can reach the King's position.
    for piece in B[1]:
        if piece.side != side:
            if piece.can_move_to(king_location[0], king_location[1], B):
                logging.debug(
                    f"{piece.__class__.__name__} at {(piece.pos_x, piece.pos_y)} threatens the King at {king_location}")
                return True
            else:
                logging.debug(
                    f"{piece.__class__.__name__} at: {(piece.pos_x, piece.pos_y)} does not threaten the King at {king_location}")

    logging.debug("Board state is not in check for either side.")
    return False # No threats to the King. 

def is_checkmate(side: bool, B: Board) -> bool:
    # Step 1, check if the King is in check; if not, return False.
    if not is_check(side, B):
        return False

    all_squares = [(x, y) for x in range(1, B[0] + 1) for y in range(1, B[0] + 1)]

    # Step 2, check for possible moves to get out of check. 
    for piece in B[1]: # For pieces in the piece list, 
        if piece.side == side: # if the piece is on the same side of the king,
            for x, y in all_squares: # check all squares on the board.
                # Backup the pieces list before simulating the move.
                original_pieces = B[1][:]

                if piece.can_move_to(x, y, B): # If (same side) piece can move to a square,
                    # temporarily move the piece and check if the move results in check.
                    hypothetical_board = (B[0], original_pieces) # Create a new board with the original pieces.
                    hypothetical_piece = piece_at(piece.pos_x, piece.pos_y, hypothetical_board)

                    # Move the piece on the hypothetical board. 
                    hypothetical_piece.move_to(x, y, hypothetical_board)

                    logging.debug(f"Testing {piece.__class__.__name__} moving to ({x}, {y}).")
                    if not is_check(side, hypothetical_board):
                        logging.debug(
                            f"Escape found! {piece.__class__.__name__} to ({x}, {y}) prevents checkmate.")
                        return False  # Escape found, so it's not checkmate.
    
    print(f"Checkmate! The {side} King is in checkmate.")
    return True # checkmate

def is_stalemate(side: bool, B: Board) -> bool:
    # Step 1, check if the king is in check; return false if king in check.
    if is_check(side, B):
        return False
    
    all_squares = [(x, y) for x in range(1, B[0] + 1) for y in range(1, B[0] + 1)]

    # Step 2, Check if any piece has a valid move.
    for piece in B[1]: # Check all pieces.
        if piece.side == side:
            for x, y in all_squares: # Check all squares on the board.
                    if piece.can_move_to(x, y, B):
                        # Simulate move without calling move_to.
                        B_copy = copy.deepcopy(B)

                        # Find the matching piece in the copied board (same side).
                        simulated_piece = next(p for p in B_copy[1] if
                                               p.pos_x == piece.pos_x and p.pos_y == piece.pos_y and p.side == side)

                        # Simulate capturing opponent's piece at the destination.
                        captured_piece = piece_at(x, y, B_copy)
                        if captured_piece and captured_piece.side != side:
                            B_copy[1].remove(captured_piece)

                        # Move the simulated piece.
                        simulated_piece.pos_x, simulated_piece.pos_y = x, y

                        # Check if the king is still in check after the simulated move.
                        if not is_check(side, B_copy):
                            logging.debug(
                                f"A valid move exists for {piece.__class__.__name__} at ({piece.pos_x}, {piece.pos_y}) "
                                f"to ({x}, {y}). Not stalemate.")
                            return False  # A valid move exists.
                        
    # If no piece can move: it's a stalemate.
    print(f"Stalemate! The {side} King is not in check and no pieces can move.")
    return True 

def read_board(filename: str) -> Board:
    try: 
        with open(filename, 'r') as f:
            S = int(f.readline().strip())
            white_pieces = f.readline().strip().split(', ')
            black_pieces = f.readline().strip().split(', ')
        
        logging.debug(f"Board parameters: {S}")
        logging.debug(f"White pieces: {white_pieces}")
        logging.debug(f"Black pieces: {black_pieces}")

        pieces = []

        for piece_str in white_pieces: 
            if piece_str:
                type_str = piece_str[0] # First character is the type (ex, "K" for King, "B" Bishop),
                loc = piece_str[1:] # the rest of the string is the location (ex, "b5").
                x, y = location2index(loc)
                if type_str == "K":
                    pieces.append(King(x, y, True))
                elif type_str == "B":
                    pieces.append(Bishop(x, y, True))

        for piece_str in black_pieces:
            if piece_str:
                type_str = piece_str[0]
                loc = piece_str[1:]
                x, y = location2index(loc)
                if type_str == "K":
                    pieces.append(King(x, y, False))
                elif type_str == "B":
                    pieces.append(Bishop(x, y, False))

        Board = (S, pieces)
        return Board
    except: 
        raise IOError("This is not a valid file.")

def save_board(filename: str, B: Board) -> None:
    with open(filename, 'w') as f:
        f.write(f"{B[0]}\n")
        white_pieces = []
        black_pieces = []
        for piece in B[1]: 
            loc = index2location(piece.pos_x, piece.pos_y)
            piece_char = "K" if isinstance(piece, King) else "B"
            piece_str = f"{piece_char}{loc}" 
            if piece.side:
                white_pieces.append(piece_str)
            else: 
                black_pieces.append(piece_str)
        f.write(", ".join(white_pieces) + "\n")
        f.write(", ".join(black_pieces) + "\n")

def find_black_move(B: Board) -> tuple[Piece, int, int]:
    all_moves = [] # To store all possible moves before choosing the best one.
    checkmate_found = False
    check_found = False 

    # Check for checkmate.
    for piece in [p for p in B[1] if not p.side]: 
        if checkmate_found:
            break

        for x in range(1, B[0] + 1):
            for y in range(1, B[0] + 1):
                if piece.can_move_to(x, y, B):
                    orig_x, orig_y = piece.pos_x, piece.pos_y
                    # Simulate the move. 
                    hypothetical_board = (B[0, copy.deepcopy(B[1])])
                    hypothetical_piece = next(p for p in hypothetical_board[1] if
                                            p.pos_x == piece.pos_x and p.pos_y == piece.pos_y and isinstance(p,
                                                                                                            piece.__class__))

                    # find a captured piece. 
                    captured_piece = piece_at(x, y, hypothetical_board)
                    hypothetical_piece.pos_x, hypothetical_piece.pos_y = x, y

                    # Check for checkmate.
                    if is_checkmate(False, hypothetical_board):
                        move_type = 'checkmate'
                        checkmate_found = True
                        all_moves.append((orig_x, orig_y, x, y, move_type, captured_piece))
                        break  # Stop further simulations for this piece.
                
                    # Check for check.
                    elif is_check(False, hypothetical_board):
                        move_type = 'check'
                        check_found = True
                        all_moves.append((orig_x, orig_y, x, y, move_type, captured_piece))
                        continue
                    
                    # Check for capture.
                    elif captured_piece and captured_piece.side != piece.side:
                        move_type = 'capture'
                        all_moves.append((orig_x, orig_y, x, y, move_type, captured_piece))

                    # Valid move.
                    else:
                        move_type = 'valid'
                        all_moves.append((orig_x, orig_y, x, y, move_type, captured_piece))

    # Prioritize better moves. 
    if all_moves: 
        move_priority = {'checkmate': 4, 'check': 3, 'capture': 2, 'valid': 1}
        best_move = max(all_moves, key=lambda move: move_priority[move[4]])

        orig_x, orig_y, x, y, move_type, captured_piece = best_move
        logging.debug(f"The best move is: {orig_x, orig_y} to {x, y}. Move type: {move_type}.")

        # Locate the actual piece at the original position.
        piece = next(p for p in B[1] if p.pos_x == orig_x and p.pos_y == orig_y)
        
        # Apply the move.
        return piece, x, y 

    return None

def conf2unicode(B: Board) -> str: 
    unicode_board = "" # Empty string to store the unicode board.
    for y in range(B[0], 0, - 1): # Run a loop from 1 to the size of the board.
        row = []
        for x in range(1, B[0] + 1):
            piece = next((p for p in B[1] if p.pos_x == x and p.pos_y == y), None)
            if piece: 
                if isinstance(piece, Bishop):
                    row.append("♗" if piece.side else "♝")
                elif isinstance(piece, King):
                    row.append("♔" if piece.side else "♚")
        # Default board display if no piece.
            else:
                row.append(" ")
        # Join all rows together. 
        unicode_board += "".join(row) + "\n"
    return unicode_board

def main() -> None:   
    B = None
    start = None
    finish = None

    filename = input("File name for initial configuration: ")

    if filename == "QUIT":
        quit()
    elif filename != "QUIT":
        while True: 
            try:
                B = read_board(filename)
                break
            except IOError:
                filename = input("This is not a valid file. File name for initial configuration: ")
    if B:       
        logging.debug(conf2unicode(B)) # Print the board in unicode format.

    while True: # Game running.
        # White's turn:
        white_input = input("Next move of White: ").strip()
        if white_input == "QUIT":
            save_file = input("File name for final configuration: ")
            save_board(save_file, B)
            print("The game configuration saved.")
            break
        
        elif white_input != "QUIT":
            try:
                # Format: (start position, end position) ex: (b5, c6)
                # len 4, ex: a1b1
                if len(white_input) == 4:
                    start = white_input[:2]
                    finish = white_input[2:]
                #len 5, format: a10b1 
                elif len(white_input) == 5:
                    if white_input[1].isdigit() and white_input[2].isdigit():
                        start = white_input[:3]
                        finish = white_input[4:]
                #len 5, format: a1b10
                    else:
                        start = white_input[:2]
                        finish = white_input[3:]
                #len 6, ex: a10b10
                elif len(white_input) == 6:
                    start = white_input[:3]
                    finish = white_input[4:]

                # convert to (x,y) coordinates:
                start_x, start_y = location2index(start)
                finish_x, finish_y = location2index(finish)

                # find the piece at the starting position:
                piece = piece_at(start_x, start_y, B)

                if not piece: # There is no piece here.
                    print(f"There is no piece at {start_x, start_y}. Try again.") # debug 
                    raise Exception
                
                # If there is a piece,
                # validate that it can move to the destination. 
                if piece.can_move_to(finish_x, finish_y, B):
                    B = piece.move_to(finish_x, finish_y, B)
                    print(f"The configuration after White's move is:\n{conf2unicode(B)}")
                else:
                    print("This is not a valid move. Try again.")
                    continue
            except Exception: 
                print("Invalid input. Try again.")
                continue 

        if is_checkmate(False, B):
            print("Checkmate! White wins.")
            break

        elif is_stalemate(False, B):
            print("Stalemate! The game is a draw.")
            break

        # Black's turn:
        print("Next move of Black is ", end="")
        black_piece, black_x, black_y = find_black_move(B)
        print(f"{index2location(black_x, black_y)}")
        
        # Apply Black's move to the board.
        B = black_piece.move_to(black_x, black_y, B)
        print(f"The configuration after Black's move is:\n{conf2unicode(B)}")

        # Check for checkmate or stalemate after Black's move.
        if is_checkmate(True, B):
            print("Game over. Black wins.")
            quit() 

        elif is_stalemate(True, B):
            print("Game over. Stalemate.")
            quit()

if __name__ == '__main__': 
   main()
