from utils import *

lower = 'lower'
upper = 'UPPER'

oppositePlayer = {lower:upper, upper:lower}
allPossiblePieces = {'p','P',
                     'k','K',
                     'g', 'G',
                     's', 'S',
                     'b', 'B',
                     'r', 'R',
                     '+s', '+S',
                     '+b', '+B',
                     '+r', '+R',
                     '+p', '+P'}

class Minishogi(object):
    def __init__(self, vals):
        self.currPlayer = lower

        self.boardPieces = {}
        self.boardImage = []

        self.numberOfMoves = 0
        self.gameOver = False
        self.outMessage = ''

        # naturally, you'd want your pieces to be existing and
        # then you'd want to act on your set of moves
        self.placeAllPieces(vals['initialPieces'], vals['lowerCaptures'], vals['upperCaptures'])
        self.makeMovesArray(vals['moves'])
        self.main()
        self.display()

    def makeMovesArray(self, moves):
        for move in moves:
            sequence = move.split(' ')
            # case1: move <pos1> <pos2> (promote)
            # case2: drop <piece> <pos>
            # case3: anything else
            if (sequence[0] == 'move') and (len(sequence) == 3 or len(sequence) == 4):
                if not (self.isLegalPosition(sequence[1]) and self.isLegalPosition(sequence[2])):
                    self.gameOverExiting(1)
                    break
                else:
                    self.applyMove(sequence)
            elif (sequence[0] == 'drop') and (len(sequence) == 3):
                if not (self.isLegalPosition(sequence[2])):
                    self.gameOverExiting(1)
                    break
                else:
                    self.applyDrop(sequence)
            else:
                self.gameOverExiting(1)
                break

    def applyMove(self, move):
        pass

    def applyDrop(self, move):
        pass

    def applyPromote(self, move):
        pass

    #check if sensible position
    #now check if within board
    def isLegalPosition(self, position):
        if len(position) != 2:
            return 0
        return self.isWithinBoard(position)


    def isWithinBoard(self, position):
        if not ('a' <= position[0] <= 'e' and '1' <= position[1] <= '5'):
            return 0
        return 1

    #case 1: '<opposite> player wins. Illegal Move.'
    #case 2: '<current> player wins. Checkmate.'
    #case 3: 'Tie game. Too many moves.'
    def gameOverExiting(self, case):
        self.gameOver = True
        if case == 1:
            self.outMessage = oppositePlayer[self.currPlayer] + ' player wins. Illegal Move.'
        elif case == 2:
            self.outMessage = self.currPlayer + ' player wins. Checkmate.'
        elif case == 3:
            self.outMessage = 'Tie game. Too many moves.'


    def placeAllPieces(self, piecesOnBoard, lowerCaptures, upperCaptures):
        self.upperCaptures = lowerCaptures
        self.lowerCaptures = upperCaptures
        pieceInfo = {}
        self.boardImage = [['' for i in range(5)] for j in range(5)]

        # TODO: Handle upper player pieces and piece to be promoted
        for pc in piecesOnBoard:
            coord = self.getCoordinates(pc['position'])
            self.boardPieces[coord] = shogiPieces[pc['piece']]()
            self.boardImage[coord[0]][coord[1]] = pc['piece']

        return


    def getCoordinates(self, position):
        return (ord(position[0])-97, int(position[1])-1)


    def main(self):
        pass

    def display(self):
        print(stringifyBoard(self.boardImage))

    def __str__(self):
        return str("sup")


class Piece:
    def __init__(self):
        pass

class Pawn(Piece):
    pass

class King(Piece):
    pass

class Gold(Piece):
    pass

class Silver(Piece):
    pass

class Rook(Piece):
    pass

class Bishop(Piece):
    pass

class dragonHorse(Piece):
    pass

class dragonKing(Piece):
    pass

#these are all possible pieces
#for promoted pieces. see the plus
#call the class with the second letter
#and the case of the letter (upper case, lower case)
shogiPieces = {'k':King,
               'p':Pawn,
               's':Silver,
               'g':Gold,
               'r':Rook,
               'b':Bishop}

#promoted pieces and how they move
#TODO if trying to promote k or g, throw error
promotion = {'s':Gold,
             'b':dragonHorse,
             'r':dragonKing,
             'p':Gold}
