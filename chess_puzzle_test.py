import pytest
from chess_puzzle import *

# location2index tests:
def test_location2index1(): # preprovided test from original code
    assert location2index("e2") == (5,2)

def test_location2index2(): # once converted, letter and number both == len(1)
    assert location2index("a1") == (1,1)

def test_location2index3(): # once converted, letter == len(2), number == len(1)
    assert location2index("j1") == (10,1)

def test_location2index4(): # once converted, letter == len(1), number both == len(2)
    assert location2index("a15") == (1,15)

def test_location2index5(): # once converted, letter and number both == len(2)
    assert location2index("m12") == (13,12)

# index2location tests:
def test_index2location1(): # preprovided test from original code
    assert index2location(5,2) == "e2"

def test_index2location2(): # convert x and y values, both == len(1), to a letter and number
    assert index2location(1,1) == "a1"

def test_index2location3(): # convert x and y values, to a letter and number: letter == len(2), number == len(1)
    assert index2location(10,1) == "j1"

def test_index2location4(): # convert x and y values, to a letter and number: letter == len(1), number both == len(2)
    assert index2location(1, 15) == "a15"

def test_index2location5(): # convert x and y values, to a letter and number: letter and number both == len(2)
    assert index2location(13, 12) == "m12"

wb1 = Bishop(2,5,True)
wb2 = Bishop(4,4,True)
wb3 = Bishop(3,1,True)
wb4 = Bishop(5,5,True)
wb5 = Bishop(4,1,True)
wb6 = Bishop(5, 6, True) # added bishop
wb7 = Bishop(3, 1, True) # added bishop
wb8 = Bishop(3, 2, True) # added bishop
wb9 = Bishop(4, 2, True) # added bishop

wk1 = King(3,5,True)
wk1a = King(2,5,True)
wk1b = King(2, 1, True) # added King
wk1c = King(2, 2, True) # added King

bb1 = Bishop(3,3,False)
bb2 = Bishop(5,3,False)
bb3 = Bishop(1,2,False)
bb4 = Bishop(3, 2, False) # added bishop
bb5 = Bishop(5, 4, False) # added bishop
bb6 = Bishop(1, 3, False) # added bishop
bb7 = Bishop(4, 3, False) # added bishop
bb8 = Bishop(4, 2, False) # added bishop
bb9 = Bishop(4, 4, False) # added bishop
bb10 = Bishop(2, 3, False) # added bishop

bk1 = King(2,3,False)
bk1a = King(1, 5, False)

B1 = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1]) # preprovided from original code
B2 = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1, wb5, bb3, bb4]) # alternative board setup
B3 = (5, [wb1, bb1, wb2, bb2, wk1, bk1, wb5, bb3, bb4, bb5]) # alternative board setup

# is_piece_at tests:
def test_is_piece_at1(): # preprovided test from original code
    assert is_piece_at(2,2, B1) == False

def test_is_piece_at2(): # tile is not on the board, therefore False
    assert is_piece_at(0,0, B1) == False

def test_is_piece_at3(): # tile is not on the board, therefore False
    assert is_piece_at(50,50, B1) == False

def test_is_piece_at4(): # tile is not on the board, therefore False
    assert is_piece_at(-5,-10, B1) == False

def test_is_piece_at5(): # tile is empty, therefore False
    assert is_piece_at(1, 1, B1) == False

def test_is_piece_at6(): # tile is occupied by a white King, therefore True
    assert is_piece_at(3, 5, B1) == True

def test_is_piece_at7(): # tile is occupied by a black King, therefore True
    assert is_piece_at(2, 3, B1) == True

def test_is_piece_at8(): # tile is occupied by a white Bishop, therefore True
    assert is_piece_at(2, 5, B1) == True

def test_is_piece_at9(): # tile is occupied by a black Bishop, therefore True
    assert is_piece_at(3, 3, B1) == True

def test_is_piece_at10(): # tile is assigned, but not present in B1, therefore False
    assert is_piece_at(4, 1, B1) == False # wb5

def test_is_piece_at11(): # tile is assigned, but not present in B1, therefore False
    assert is_piece_at(1, 2, B1) == False # bb3

# piece_at tests:
def test_piece_at1(): # preprovided test from original code
    assert piece_at(3,3, B1) == bb1

def test_piece_at2(): 
    assert piece_at(2, 5, B1) == wb1

def test_piece_at3(): 
    assert piece_at(4, 4, B1) == wb2

def test_piece_at4(): 
    assert piece_at(5, 3, B1) == bb2

def test_piece_at5(): 
    assert piece_at(3,5, B1) == wk1

# can_reach tests (for bishops): 
def test_can_reach1(): # preprovided test from original code, bishop can reach a diagonal tile whose pathway is not blocked or occupied by the same side
    assert wb2.can_reach(5, 5, B1) == True

def test_can_reach2(): # bishop can reach a diagonal tile whose pathway is not blocked, but it is occupied by an enemy piece (which will be captured)
    assert bb1.can_reach(4, 4, B1) == True

def test_can_reach3(): # bishop can not reach a diagonal tile whose pathway is not blocked, but it is occupied by a same side piece
    assert wb2.can_reach(3, 5, B1) == False

def test_can_reach4(): # bishop on a white tile can not reach black tile adjacent to it (because not a diagnoal move)
    assert wb2.can_reach(5, 4, B1) == False

def test_can_reach5(): # bishop can not reach tile with a piece, from any side, blocking the pathway to it 
    assert bb1.can_reach(5, 5, B1) == False 

# can_reach tests (for kings):
def test_can_reach6(): # king can not reach a tile not on the board
    assert wk1.can_reach(6, 5, B1) == False

def test_can_reach7(): # king can not reach a tile 2 tiles away from it
    assert bk1.can_reach(1, 1, B1) == False

# can_move_to tests (for bishops):
def test_can_move_to1(): # bishop can move to a reachable, empty, space, while not putting own King in check 
    assert wb2.can_move_to(5,5, B1) == True

def test_can_move_to2(): # bishop can move to a reachable, enemy occupied, space, while not putting own King in check 
    assert bb1.can_move_to(4, 4, B2) == True

def test_can_move_to3(): # king can not move to unreachable space 
    assert wb2.can_move_to(2, 2, B2) == False # jumping over an enemy piece

def test_can_move_to4(): # bishops can not move to unreachable spaces
    assert bb3.can_move_to(-1, 0, B2) == False # off the board
    assert bb4.can_move_to(1, 4, B2) == False # jumping over one's own piece

# can_move_to tests (for kings):
def test_can_move_to5(): # king can move to a reachable space, while not putting self in check 
    assert bk1.can_move_to(2, 2, B3) == True

# is_check tests:
def test_is_check1(): # preprovided test from original code
    B4 = (5, [wb1, wk1, bk1, bb1, bb2, wb3]) # White king in check from black bishop
    assert is_check(True, B4) == True

def test_is_check1a(): # same as test_is_check1, but with different variable convention
    B4 = (5, [King(2,3,False), Bishop(2,5,True), Bishop(3,1,True), Bishop(3,3,False), King(3,5,True), Bishop(5,3, False)])
    assert is_check(True, B4) == True

def test_is_check2(): # Black king in check from white bishop (wb6), board size increased to 6x6
    B5 = (6, [King(2,3,False), Bishop(2,5,True), Bishop(3,1,True), Bishop(3,3,False), King(3,5,True), Bishop(5,6,True)])
    assert is_check(False, B5) == True

def test_is_check3_and_4(): # there is not a check for the white or the black king
    B5 = (5,[wk1,bk1,wb1])
    assert is_check(True, B5) == False
    assert is_check(False, B5) == False

def test_is_check5_and_6(): # Stalemate (therefore not check), board size decreased to 3x3
    B7 = (3, [wk1b, bk1])
    assert is_check(True, B7) == False
    assert is_check(False, B7) == False

# is_checkmate tests:
def test_is_checkmate1(): # preprovided test from original code
    B8 = (5, [wk1a, wb4, bk1, bb2, bb3, wb3, wb5]) # black king in check, can't move out of the way
    assert is_checkmate(False, B8) == True

def test_is_checkmate2(): # White king in checkmate, no bishops can save and nowhere to run 
    B9 = (5, [wk1a, bk1, bb1, bb6, bb7])
    assert is_checkmate(True, B9) == True   

def test_is_checkmate3(): # White king in check, but not checkmate because it can run out of the way
    B10 = (5, [wk1, bk1, bb1, bb7])
    assert is_checkmate(True, B10) == False

def test_is_checkmate4(): # Black king in check, but not checkmate because a bishop can destroy the piece putting it into check
    B11 = (5, [wk1a, bk1, bb1, bb7, wb7])
    assert is_checkmate(False, B11) == False

def test_is_checkmate5(): # White king in checkmate, can not reach any safe tile or destroy the piece putting it into check
    B12 = (4, [wk1b, bk1, bb7, bb8, bb9])
    assert is_checkmate(True, B12) == True

# is_stalemate tests:
def test_is_stalemate1(): # black is in stalemate
    B13 = (4, [King(1,1, True), Bishop(1, 2, True), Bishop(2, 1, True), Bishop(4, 2, True), King(4, 4, False)])
    assert is_stalemate(False, B13) == True

def test_is_stalemate2(): # black in stalemate: can't move the king anywhere or it will be in check
    B14 = (4, [King(1, 4, False), King(2, 2, True), Bishop(4, 2, True)])
    assert is_stalemate(False, B14) == True

def test_is_stalemate3(): # black is in check and can move away, so it's not a stalemate
    B15 = (4, [King(1, 4, False), King(2, 2, True), Bishop(3, 2, True)])
    assert is_stalemate(False, B15) == False

def test_is_stalemate4(): # white in stalemate
    B16 = (4, [King(1, 1, True), King(2, 3, False), Bishop(4, 3, False)])
    assert is_stalemate(False, B16) == False

def test_is_stalemate5(): # It's a checkmate so it's not a stalemate, because a. it's a checkmate and b. a checkmate is predicated on a check which means it can not be a stalemate
    B17 = (4, [wk1b, bk1, bb7, bb8, bb9])
    assert is_stalemate(True, B17) == False

# read_board tests:
def test_read_board1(): # preprovided example test from original code
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_read_board2(): # assert that filename can't be something not in the directory
    with pytest.raises(IOError):
        read_board("i_love_guinea_pigs.txt")

def test_read_board3(): # filename has no file type
    with pytest.raises(IOError):
        read_board("board_examp")

def test_read_board4(): # does not end in txt format
    with pytest.raises(IOError):
        read_board("board_examp.doc")
        read_board("board_examp.pdf")
        read_board("board_examp.css")

def test_read_board5(): # filename input is empty
    with pytest.raises(IOError):
        read_board("")

def test_read_board6(): # no out of bound pieces
    B = read_board("board_examp.txt")
    board_size = B[0]
    for piece in B[1]:
        assert 1 <= piece.pos_x <= board_size
        assert 1 <= piece.pos_y <= board_size

def test_read_board7(): # test that each side has a king: 
    B = read_board("board_examp.txt")
    white_king_count = 0
    black_king_count = 0
    for piece in B[1]:
        if isinstance(piece, King):
            if piece.side == True:
                white_king_count += 1
            elif piece.side == False:
                black_king_count += 1
    # there should be 2 kings: one white king, one black king
    assert white_king_count == 1 # one white king
    assert black_king_count == 1 # one black king

def test_read_board8(): # test that no pieces share the same tile 
    B = read_board("board_examp.txt")
    positions = set()
    for piece in B[1]:
        pos = (piece.pos_x, piece.pos_y)
        assert pos not in positions, f"Duplicate piece found at position {pos}"
        positions.add(pos)

# conf2unicode tests:
def test_conf2unicode1(): 
    board = (3, [King(2, 3, True), King(2, 1, False)])  # try for white King and black King
    expected = " ♔ \n   \n ♚ \n"
    assert conf2unicode(board) == expected

def test_conf2unicode2():
    board = (4, [King(2, 3, True), King(4, 4, False)])  # expand board size, change locaiton of black King
    expected = "   ♚\n ♔  \n    \n    \n"
    assert conf2unicode(board) == expected

def test_conf2unicode3():  # add a white Bishop to test2
    board = (4, [King(2, 3, True), King(4, 4, False), Bishop(1, 1, True)])
    expected = "   ♚\n ♔  \n    \n♗   \n"
    assert conf2unicode(board) == expected

def test_conf2unicode4(): # expand board size, try with pieces in the new squares, add a black Bishop
    board = (5, [King(2, 3, True), King(4, 4, False), Bishop(5, 5, True), Bishop(5, 1, False)])
    expected = "    ♗\n   ♚ \n ♔   \n     \n    ♝\n"
    assert conf2unicode(board) == expected

def test_conf2unicode5():  # try for empty board
    board = (3, [])
    expected = "   \n   \n   \n"
    assert conf2unicode(board) == expected

# move_to tests: 
def test_move_to1(): # preprovided code from assignment, check if piece wb2a is present on board
    wb2a = Bishop(3,3,True)
    B1 = (5, [wb2a, wb1, wk1, bk1, wb3]) 
    Actual_B = wb2a.move_to(1, 1, B1) # wb2a moves to (1,1)
    wb2a.pos_x, wb2a.pos_y = 1, 1
    Expected_B = (5, [wb2a, wb1, wk1, bk1, wb3]) 

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to2(): # board size 6x6, white bishop moves, does not capture anything
    wb2a = Bishop(3,3,True)
    B1 = (6, [wb2a, wb1, wk1, bk1, bb2, wb3])
    Actual_B = wb2a.move_to(6, 6, B1)
    wb2a.pos_x, wb2a.pos_y = 6, 6
    Expected_B = (6, [wb2a, wb1, wk1, bk1, bb2, wb3])

    # Check if actual board has the same contents as expected
    assert Actual_B[0] == 6

    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to3():  # black bishop moves, captures white bishop
    wb2b = Bishop(6, 4, True) 
    bb2a = Bishop(4, 2, False)
    B1 = (6, [wb2b, wb1, wk1, bk1, bb2a, wb3]) 
    Actual_B = bb2a.move_to(6, 4, B1) # move black bishop, capture white bishop (wb2b) at (6,4)
    bb2a.pos_x, bb2a.pos_y = 6, 4 
    Expected_B = (6, [bb2a, wb1, wk1, bk1, wb3])

    # Check if actual board has the same contents as expected
    assert Actual_B[0] == 6

    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to4():  # black king moves, does not capture anything
    wb2a = Bishop(3, 3, True)
    bk1b = King(3, 2, False)
    B1 = (6, [wb2a, wb1, wk1, bk1])
    Actual_B = bk1.move_to(3, 2, B1) # move black king
    Expected_B = (6, [wb2a, wb1, wk1, bk1b])

    # Check if actual board has the same contents as expected
    assert Actual_B[0] == 6

    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to5(): # white king is in check, moves out of check 
    bb3 = Bishop(4, 5, False)
    wk1 = King(3, 5, True)
    B1 = (5, [bb3, wk1, bk1, bb2])
    Actual_B = wk1.move_to(2, 5, B1) # white king moves to safety (out of check)
    wk1.pos_x, wk1.pos_y = 2, 5
    Expected_B = (5, [bb3, wk1, bk1, bb2])

    # Check if actual board has the same contents as expected
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found