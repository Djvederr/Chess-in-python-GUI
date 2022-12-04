import numpy as np
import math
EMPTY = 0
WK = 1
WQ = 2
WN1 = 3
WN2 = 4
WB1 = 5
WB2 = 6
WR1 = 7
WR2 = 8
WP1 = 9
WP2 = 10
WP3 = 11
WP4 = 12
WP5 = 13
WP6 = 14
WP7 = 15
WP8 = 16
BK = 17
BQ = 18
BN1 = 19
BN2 = 20
BB1 = 21
BB2 = 22
BR1 = 23
BR2 = 24
BP1 = 25
BP2 = 26
BP3 = 27
BP4 = 28
BP5 = 29
BP6 = 30
BP7 = 31
BP8 = 32


class ChessEngine:

    def __init__(self):
        self.board = np.array([[WR1, WN1, WB1, WK, WQ, WB2, WN2, WR2],
                               [WP1, WP2, WP3, WP4, WP5, WP6, WP7, WP8],
                               [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                               [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                               [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                               [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
                               [BP1, BP2, BP3, BP4, BP5, BP6, BP7, BP8],
                               [BR1, BN1, BB1, BK, BQ, BB2, BN2, BR2]])
        self.rooks = [WR1, WR2, BR1, BR2]
        self.knights = [WN1, WN2, BN1, BN2]
        self.bishops = [WB1, WB2, BB1, BB2]
        self.queens = [WQ, BQ]
        self.kings = [WK, BK]
        self.pawns = [WP1, WP2, WP3, WP4, WP5, WP6, WP7, WP8, BP1, BP2, BP3, BP4, BP5, BP6, BP7, BP8]
        self.white_pieces = [WR1, WN1, WB1, WQ, WK, WB2, WN2, WR2, WP1, WP2, WP3, WP4, WP5, WP6, WP7, WP8]
        self.black_pieces = [BP1, BP2, BP3, BP4, BP5, BP6, BP7, BP8, BR1, BN1, BB1, BQ, BK, BB2, BN2, BR2]
        self.turn=0
        self.status={"is_check":False,
                     "checkmate":False,
                     "stalemate":False,
                     "castle":{"white":{"CanCastle":True,
                                        "0,0Rook":True,
                                        "0,7Rook":True},
                               "black":{"CanCastle":True,
                                        "7,0Rook":True,
                                        "7,7Rook":True}},
                     "promote":{"white":False,
                                "black":False},
                     "game_end":False,
                     "black_en_pascante":[False,None],
                     "white_en_pascante":[False,None]
                     }
    def check_castling(self,start_pos,colour):
        possible_moves=[]
        if colour=="w":
            if self.status["castle"]["white"]["CanCastle"]==False:
                return []
            else:
                if self.board[start_pos[0]][start_pos[1]] in self.kings:
                    if self.status["castle"]["white"]["0,0Rook"]==True and self.board[0][1]==EMPTY and self.board[0][2]==EMPTY:
                        possible_moves.append((0,0))
                    if self.status["castle"]["white"]["0,7Rook"]==True and self.board[0][6]==EMPTY and self.board[0][5]==EMPTY and self.board[0][4]==EMPTY:
                        possible_moves.append((0,7))
        elif colour=="b":
            if self.status["castle"]["black"]["CanCastle"]==False:
                return []
            else:
                if self.board[start_pos[0]][start_pos[1]] in self.kings:
                    if self.status["castle"]["black"]["7,0Rook"]==True and self.board[7][1]==EMPTY and self.board[7][2]==EMPTY:
                        possible_moves.append((7,0))
                    if self.status["castle"]["black"]["7,7Rook"]==True and self.board[7][6]==EMPTY and self.board[7][5]==EMPTY and self.board[7][4]==EMPTY:
                        possible_moves.append((7,7))
        return possible_moves

    def set_board(self,board):
        self.board=board.copy()

    def update_game_status(self,cur_colour):
        if self.is_check(cur_colour):
            self.status["is_check"] = True
        else:
            self.status["is_check"] = False
        if cur_colour=="w":
            possible_moves=[]
            for r in range(8):
                for c in range(8):
                    if self.board[r][c] in self.white_pieces:
                        for x in self.check_legal_moves((r,c),"w"):
                            possible_moves.append(x)
            if len(possible_moves)==0:
                if self.status["is_check"]==True:
                    self.status["checkmate"]=True
                    self.status["game_end"]=True
                elif self.status["is_check"]==False:
                    self.status["stalemate"] = True
                    self.status["game_end"] = True
        elif cur_colour=="b":
            possible_moves=[]
            for r in range(8):
                for c in range(8):
                    if self.board[r][c] in self.black_pieces:
                        for x in self.check_legal_moves((r,c),"b"):
                            possible_moves.append(x)
            if len(possible_moves)==0:
                if self.status["is_check"]==True:
                    self.status["checkmate"]=True
                    self.status["game_end"] = True
                elif self.status["is_check"]==False:
                    self.status["stalemate"] = True
                    self.status["game_end"] = True
    def is_check(self,cur_colour):
        if cur_colour=="b":
            possible_moves=[]
            for r in range(8):
                for c in range(8):
                    if self.board[r][c] in self.white_pieces:
                        for x in self.find_legal_moves((r,c),"w"):
                            possible_moves.append(x)
                    if self.board[r][c] == BK:
                        king_pos=(r,c)
            if king_pos in possible_moves:
                return True
            else:
                return False
        elif cur_colour=="w":
            possible_moves=[]
            for r in range(8):
                for c in range(8):
                    if self.board[r][c] in self.black_pieces:
                        for x in self.find_legal_moves((r,c),"b"):
                            possible_moves.append(x)
                    if self.board[r][c] == WK:
                        king_pos=(r,c)
            if king_pos in possible_moves:
                return True
            else:
                return False
    def get_piece_colour(self,cell):
        if self.board[cell[0]][cell[1]] in self.white_pieces:
            return "w"
        elif self.board[cell[0]][cell[1]] in self.black_pieces:
            return "b"
        else:
            return "empty"

    def get_colour(self):
        if self.turn % 2 == 0:
            return "w"
        else:
            return "b"

    def display_board(self):
        print(self.board)

    def illegaly_move(self, start_pos, end_pos):
        self.board[end_pos[0]][end_pos[1]] = self.board[start_pos[0]][start_pos[1]]
        self.board[start_pos[0]][start_pos[1]] = EMPTY

    def move(self,start_pos, end_pos):
        if self.board[start_pos[0]][start_pos[1]] in self.white_pieces and self.turn%2==0:
            colour="w"
        elif self.board[start_pos[0]][start_pos[1]] in self.black_pieces and self.turn%2==1:
            colour="b"
        moves=self.check_legal_moves(start_pos,colour)
        if end_pos in moves:
            if self.board[start_pos[0]][start_pos[1]] in self.rooks and self.board[start_pos[0]][start_pos[1]] in self.white_pieces:
                if start_pos==(0,0):
                    self.status["castle"]["white"]["0,0Rook"]=False
                elif start_pos==(0,7):
                    self.status["castle"]["white"]["0,7Rook"] = False
            elif self.board[start_pos[0]][start_pos[1]] in self.rooks and self.board[start_pos[0]][start_pos[1]] in self.black_pieces:
                if start_pos==(7,0):
                    self.status["castle"]["black"]["7,0Rook"]=False
                elif start_pos==(7,7):
                    self.status["castle"]["black"]["7,7Rook"] = False
            elif self.board[start_pos[0]][start_pos[1]] in self.kings:
                if self.board[start_pos[0]][start_pos[1]] == WK:
                    self.status["castle"]["white"]["CanCastle"] = False
                elif self.board[start_pos[0]][start_pos[1]] == BK:
                    self.status["castle"]["black"]["CanCastle"] = False
            if self.board[start_pos[0]][start_pos[1]] in self.kings:
                if self.board[start_pos[0]][start_pos[1]] == WK:
                    if start_pos==(0,3) and end_pos==(0,1):
                        self.illegaly_move((0,0),(0,2))
                    elif start_pos==(0,3) and end_pos==(0,5):
                        self.illegaly_move((0, 7), (0, 4))
                elif self.board[start_pos[0]][start_pos[1]] == BK:
                    if start_pos==(7,3) and end_pos==(7,1):
                        self.illegaly_move((7,0),(7,2))
                    elif start_pos==(7,3) and end_pos==(7,5):
                        self.illegaly_move((7, 7), (7, 4))
            if colour=="w" and self.board[start_pos[0]][start_pos[1]] in self.pawns:
                if end_pos[0]==7:
                    self.status["promote"]["white"]=True
            elif colour=="b" and self.board[start_pos[0]][start_pos[1]] in self.pawns:
                if end_pos[0]==0:
                    self.status["promote"]["black"] = True
            if (self.board[start_pos[0]][start_pos[1]] in self.pawns) and (self.board[end_pos[0]][end_pos[1]]==EMPTY) and (abs(start_pos[1]-end_pos[1])==1 and abs(start_pos[0]-end_pos[0])==1):
                print("Hello")
                if colour=="w":
                    self.board[4][self.status["black_en_pascante"][1]]=EMPTY
                if colour=="b":
                    self.board[3][self.status["white_en_pascante"][1]]=EMPTY
            if (self.board[start_pos[0]][start_pos[1]] in self.pawns) and (abs(end_pos[0]-start_pos[0])==2):
                if colour == "w":
                    self.status["white_en_pascante"] = [True,start_pos[1]]
                    self.status["black_en_pascante"]=[False, None]
                elif colour == "b":
                    self.status["black_en_pascante"] = [True, start_pos[1]]
                    self.status["white_en_pascante"] = [False, None]

                print(self.status["white_en_pascante"],self.status["black_en_pascante"]," En pascante")
            else:
                [self.status["white_en_pascante"],self.status["black_en_pascante"]]=[[False, None],[False, None]]
                print(self.status["white_en_pascante"], self.status["black_en_pascante"], " En pascante")
            self.board[end_pos[0]][end_pos[1]]=self.board[start_pos[0]][start_pos[1]]
            self.board[start_pos[0]][start_pos[1]]=EMPTY
            self.turn+=1
            self.update_game_status(self.get_colour())
        else:
            print("Illegal move!")

    def check_legal_moves(self,start_pos,colour):
        moves=self.find_legal_moves(start_pos,colour)
        legal_moves=[]
        temp=ChessEngine()
        for item in moves:
            temp.set_board(self.board)
            temp.illegaly_move(start_pos,item)
            if not temp.is_check(colour):
                legal_moves.append(item)
        return legal_moves




    def find_legal_moves(self, start_pos, colour):
        if self.board[start_pos[0]][start_pos[1]] in self.kings:
            return self.find_king_moves(start_pos, colour)
        elif self.board[start_pos[0]][start_pos[1]] in self.pawns:
            return self.find_pawn_moves(start_pos, colour)
        elif self.board[start_pos[0]][start_pos[1]] in self.knights:
            return self.find_knight_moves(start_pos, colour)
        elif self.board[start_pos[0]][start_pos[1]] in self.rooks:
            return self.find_rook_moves(start_pos, colour)
        elif self.board[start_pos[0]][start_pos[1]] in self.bishops:
            return self.find_bishop_moves(start_pos, colour)
        elif self.board[start_pos[0]][start_pos[1]] in self.queens:
            return self.find_queen_moves(start_pos, colour)

    def find_queen_moves(self,start_pos,colour):
        possible_moves = []
        if colour == "w":
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1] + 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1] + 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1])
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1])
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0], space[1] + 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0], space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
        elif colour == "b":
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1]+1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1]-1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0]-1, space[1] + 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0]+1, space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1])
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1])
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0], space[1] + 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0], space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
        removed_items = []
        for x in range(len(possible_moves)):
            if possible_moves[x][0] < 0 or possible_moves[x][1] < 0 or possible_moves[x][0] > 7 or possible_moves[x][1] > 7:
                removed_items.append(possible_moves[x])
        for x in removed_items:
            possible_moves.remove(x)
        return possible_moves

    def find_bishop_moves(self,start_pos,colour):
        possible_moves = []
        if colour == "w":
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1]+1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1]-1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0]-1, space[1] + 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]] == EMPTY) or (space == start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0]+1, space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
        elif colour == "b":
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1]+1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1]-1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0]-1, space[1] + 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0]+1, space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
        removed_items = []
        for x in range(len(possible_moves)):
            if possible_moves[x][0] < 0 or possible_moves[x][1] < 0 or possible_moves[x][0] > 7 or possible_moves[x][1] > 7:
                removed_items.append(possible_moves[x])
        for x in removed_items:
            possible_moves.remove(x)
        return possible_moves

    def find_rook_moves(self,start_pos,colour):
        possible_moves=[]
        if colour=="w":
            space=start_pos
            while (self.board[space[0]][space[1]]==EMPTY) or (space==start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space==start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1])
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]]==EMPTY) or (space==start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1])
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]]==EMPTY) or (space==start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0], space[1]+1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while (self.board[space[0]][space[1]]==EMPTY) or (space==start_pos) or (self.board[space[0]][space[1]] in self.black_pieces):
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0], space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.black_pieces:
                    possible_moves.append((space[0], space[1]))
                    break
        elif colour=="b":
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] + 1, space[1])
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces :
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0] - 1, space[1])
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces :
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0], space[1] + 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces :
                    possible_moves.append((space[0], space[1]))
                    break
            space = start_pos
            while self.board[space[0]][space[1]] == EMPTY or space == start_pos or self.board[space[0]][space[1]] in self.white_pieces:
                if space == start_pos:
                    pass
                else:
                    possible_moves.append(space)
                space = (space[0], space[1] - 1)
                if space[0] > 7 or space[0] < 0 or space[1] > 7 or space[1] < 0 or self.board[space[0]][space[1]] in self.white_pieces :
                    possible_moves.append((space[0], space[1]))
                    break
        removed_items = []
        for x in range(len(possible_moves)):
            if possible_moves[x][0] < 0 or possible_moves[x][1] < 0 or possible_moves[x][0] > 7 or possible_moves[x][1] > 7:
                removed_items.append(possible_moves[x])
        for x in removed_items:
            possible_moves.remove(x)
        return possible_moves

    def find_knight_moves(self,start_pos,colour):
        possible_moves=[]
        moves=[(start_pos[0]+1,start_pos[1]+2),(start_pos[0]+1,start_pos[1]-2),(start_pos[0]+2,start_pos[1]+1),(start_pos[0]+2,start_pos[1]-1),
               (start_pos[0]-1,start_pos[1]+2),(start_pos[0]-1,start_pos[1]-2),(start_pos[0]-2,start_pos[1]+1),(start_pos[0]-2,start_pos[1]-1)]
        if colour=="w":
            for m in moves:
                if self.is_inside_board(m[0],m[1]) and (self.board[m[0]][m[1]]==EMPTY or self.board[m[0]][m[1]] in self.black_pieces):
                    possible_moves.append(m)
        elif colour=="b":
            for m in moves:
                if self.is_inside_board(m[0], m[1]) and (self.board[m[0]][m[1]] == EMPTY or self.board[m[0]][m[1]] in self.white_pieces):
                    possible_moves.append(m)

        removed_items = []

        for x in range(len(possible_moves)):
            if possible_moves[x][0] < 0 or possible_moves[x][1] < 0 or possible_moves[x][0] > 7 or possible_moves[x][1] > 7:
                removed_items.append(possible_moves[x])
        for x in removed_items:
            possible_moves.remove(x)
        return possible_moves

    def find_pawn_moves(self, start_pos, colour):
        possible_moves = []
        if colour == "w":
            if start_pos[0]<7:
                if start_pos[0] == 1 and self.board[start_pos[0] + 2][start_pos[1]] == EMPTY:
                    possible_moves.append((start_pos[0] + 2, start_pos[1]))
                if self.board[start_pos[0] + 1][start_pos[1]] == EMPTY:
                    possible_moves.append((start_pos[0] + 1, start_pos[1]))
                if self.is_inside_board(start_pos[0]+1,start_pos[1]+1) and (self.board[start_pos[0] + 1][start_pos[1] + 1] in self.black_pieces):
                    possible_moves.append((start_pos[0] + 1, start_pos[1] + 1))
                if self.board[start_pos[0] + 1][start_pos[1] - 1] in self.black_pieces:
                    possible_moves.append((start_pos[0] + 1, start_pos[1] - 1))
                if start_pos[0]==4 and self.status["black_en_pascante"][0]:
                    if self.status["black_en_pascante"][1] == start_pos[1]-1:
                        possible_moves.append((start_pos[0] + 1, start_pos[1] - 1))
                    if self.status["black_en_pascante"][1] == start_pos[1] + 1:
                        possible_moves.append((start_pos[0] + 1, start_pos[1] + 1))
        if colour == "b":
            if start_pos[0]>0:
                if start_pos[0] == 6 and self.board[start_pos[0] - 2][start_pos[1]] == EMPTY:
                    possible_moves.append((start_pos[0] - 2, start_pos[1]))
                if self.board[start_pos[0] - 1][start_pos[1]] == EMPTY:
                    possible_moves.append((start_pos[0] - 1, start_pos[1]))
                if self.is_inside_board(start_pos[0]-1,start_pos[1]+1) and self.board[start_pos[0] - 1][start_pos[1] + 1] in self.white_pieces:
                    possible_moves.append((start_pos[0] - 1, start_pos[1] + 1))
                if self.board[start_pos[0] - 1][start_pos[1] - 1] in self.white_pieces:
                    possible_moves.append((start_pos[0] - 1, start_pos[1] - 1))
                if start_pos[0]==3 and self.status["white_en_pascante"][0]:
                    if self.status["white_en_pascante"][1] == start_pos[1]-1:
                        possible_moves.append((start_pos[0] - 1, start_pos[1] - 1))
                    if self.status["white_en_pascante"][1] == start_pos[1] + 1:
                        possible_moves.append((start_pos[0] - 1, start_pos[1] + 1))
        removed_items = []

        for x in range(len(possible_moves)):
            if possible_moves[x][0] < 0 or possible_moves[x][1] < 0 or possible_moves[x][0] > 7 or possible_moves[x][1] > 7:
                removed_items.append(possible_moves[x])
        for x in removed_items:
            possible_moves.remove(x)
        return possible_moves

    def is_inside_board(self,r,c):
        if r<8 and r>=0 and c<8 and c>=0:
            return True
        return False

    def find_king_moves(self, start_pos, colour):
        possible_moves = []
        moves = [(start_pos[0] + 1, start_pos[1] + 1),(start_pos[0] + 1, start_pos[1] - 1),(start_pos[0] - 1, start_pos[1] + 1),(start_pos[0] - 1, start_pos[1] - 1),
                 (start_pos[0] , start_pos[1] + 1),(start_pos[0], start_pos[1] - 1),(start_pos[0] + 1, start_pos[1]),(start_pos[0]-1, start_pos[1])]
        if colour == "w":
            for m in moves:
                if self.is_inside_board(m[0], m[1]) and (self.board[m[0]][m[1]] == EMPTY or self.board[m[0]][m[1]] in self.black_pieces):
                    possible_moves.append(m)
        elif colour == "b":
            for m in moves:
                if self.is_inside_board(m[0], m[1]) and (self.board[m[0]][m[1]] == EMPTY or self.board[m[0]][m[1]] in self.white_pieces):
                    possible_moves.append(m)

        removed_items = []

        for x in range(len(possible_moves)):
            if possible_moves[x][0] < 0 or possible_moves[x][1] < 0 or possible_moves[x][0] > 7 or possible_moves[x][1] > 7:
                removed_items.append(possible_moves[x])
        for x in removed_items:
            possible_moves.remove(x)
        castle_moves=self.check_castling(start_pos,colour)
        if len(castle_moves) != 0:
            for item in castle_moves:
                if item==(0,0):
                    possible_moves.append((0,1))
                if item==(0,7):
                    possible_moves.append((0, 5))
                if item==(7,0):
                    possible_moves.append((7,1))
                if item==(7,7):
                    possible_moves.append((7, 5))
        return possible_moves


"""
test = ChessEngine()
test.display_board()
test.move((4,2),(3,2))
test.illegaly_move((1, 0), (3, 0))
test.illegaly_move((1, 4), (3, 4))
test.illegaly_move((1, 5), (3, 5))
test.illegaly_move((0,7),(4,7))
test.illegaly_move((6,7),(2,7))
print(test.find_legal_moves((4, 7), "w"))
print(test.find_legal_moves((0, 4), "w"))
print(test.find_legal_moves((1, 6), "w"))
print(test.find_legal_moves((3,5),"w"))
print(test.find_legal_moves((7,7),"b"))
test.display_board()"""
