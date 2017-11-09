from utils import *
import pprint

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
        self.currentPlayer = lower
        self.currentMove = ''

        self.boardPieces = {}   #dict of objects
        self.capturedPieces = {lower:[], upper:[]}

        self.boardImage = [['' for i in range(5)] for j in range(5)]
        self.capturedImage = {lower:[], upper:[]}

        self.numberOfMoves = 0
        self.gameOver = False
        self.outMessage = ''

        # naturally, you'd want your pieces to be existing and
        # then you'd want to act on your set of moves
        self.placeAllPieces(vals['initialPieces'], vals['lowerCaptures'], vals['upperCaptures'])
        self.makeMovesArray(vals['moves'])
        self.main()

        #for debugging only
        # self.printPieces()
        # self.display()

    #HACK FOR DEBUGGING PURPOSES ONLY
    def printPieces(self):
        pprint.pprint(self.boardPieces)

    def makeMovesArray(self, moves):
        for move in moves:
            if self.numberOfMoves == 400:
                self.gameOverExiting(3)
                break
            sequence = move.split(' ')
            self.currentMove = move
            # case1: move <pos1> <pos2> (promote)
            # case2: drop <piece> <pos>
            # case3: anything else
            if (sequence[0] == 'move') and (len(sequence) == 3 or len(sequence) == 4):
                if not (self.isLegalPosition(sequence[1]) and self.isLegalPosition(sequence[2])):
                    self.gameOverExiting(1)
                    break
                else:
                    #self.display()
                    #print(sequence)
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
            self.currentPlayer = oppositePlayer[self.currentPlayer]
            self.numberOfMoves+=1

        if not self.gameOver:
            self.currentPlayer = oppositePlayer[self.currentPlayer] #needed because all moves over and it was the previous person's turn
            self.gameOverExiting(3)
        return


    def applyMove(self, move):
        start = self.getCoordinates(move[1])
        end = self.getCoordinates(move[2])

        #handle all edge cases
        if start not in self.boardPieces:
            self.gameOverExiting(1)
            return
        if self.boardPieces[start].getPlayer() != self.currentPlayer:
            self.gameOverExiting(1)
            return
        if end in self.boardPieces:
            if self.boardPieces[end].getPlayer() == self.currentPlayer:
                self.gameOverExiting(1)
                return
            else:
                self.applyCapture(move)

        #modify board image
        self.boardImage[end[0]][end[1]] = self.boardImage[start[0]][start[1]]
        self.boardImage[start[0]][start[1]] = ''

        #modify board pieces dict
        self.boardPieces[end] = self.boardPieces[start]
        self.boardPieces[end].setPosition(end)
        del self.boardPieces[start]

    def applyCapture(self, move):
        
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
            self.outMessage = oppositePlayer[self.currentPlayer] + ' player wins. Illegal Move.'
        elif case == 2:
            self.outMessage = self.currentPlayer + ' player wins. Checkmate.'
        elif case == 3:
            self.outMessage = 'Tie game.  Too many moves.'


    def placeAllPieces(self, piecesOnBoard, lowerCaptures, upperCaptures):
        for pc in lowerCaptures:
            self.capturedPieces[lower].append(shogiPieces[pc](pc, lower))
        for pc in upperCaptures:
            self.capturedPieces[upper].append(shogiPieces[pc.lower()](pc, upper))
        for pc in piecesOnBoard:
            coord = self.getCoordinates(pc['position'])
            self.boardImage[coord[0]][coord[1]] = pc['piece']

            # case where piece is illegal
            if pc['piece'] not in allPossiblePieces:
                self.gameOverExiting(1)
                break

            if len(pc['piece']) == 1:
                self.boardPieces[coord] = shogiPieces[pc['piece'].lower()](pc['piece'], self.whichPlayer(pc['piece']), coord, False)
            else:
                self.boardPieces[coord] = promotion[pc['piece'][1].lower()](pc['piece'], self.whichPlayer(pc['piece']), coord, True)


    def whichPlayer(self, pieceID):
        if len(pieceID)==2:
            return upper if pieceID[1].isupper() else lower
        return upper if pieceID.isupper() else lower


    def getCoordinates(self, position):
        return (ord(position[0])-97, int(position[1])-1)


    def main(self):
        print(self.currentPlayer + ' player action: ' + self.currentMove)
        print(stringifyBoard(self.boardImage))
        print('Captures UPPER: ' + ' '.join([i.getPieceID() for i in self.capturedPieces[upper]]))
        print('Captures lower: ' + ' '.join([i.getPieceID() for i in self.capturedPieces[lower]]))
        print('\n' + self.outMessage)

    # JUST FOR DEBUGGING
    def display(self):
        #pprint.pprint(self.capturedPieces)
        print(stringifyBoard(self.boardImage))

    def __str__(self):
        return 'This is minishogi'


class Piece:
    def __init__(self, pieceID, player, position=None, isPromoted=False):
        self.pieceID = pieceID
        self.player = player
        self.position = position
        self.isPromoted = isPromoted

    def getPieceID(self):
        return self.pieceID

    def getPlayer(self):
        return self.player

    def getPosition(self):
        return self.position

    def getIsPromoted(self):
        return self.isPromoted

    def setPieceID(self, pieceID):
        self.pieceID = pieceID

    def setPlayer(self, player):
        self.player = player

    def setPosition(self, position):
        self.position = position

    def setIsPromoted(self, isPromoted):
        self.isPromoted = isPromoted

    def __repr__(self):
        return self.pieceID + ', ' +  self.player +  ', ' + str(self.position) +  ', ' +  str(self.isPromoted)

    def __str__(self):
        return self.pieceID + ', ' +  self.player +  ', ' + str(self.position) +  ', ' +  str(self.isPromoted)

    def performMoves(self,x,y,board,PieceID,possibleMoves):
        pass

    def derivedPieceMove(self,x,y,pieceID,player,promoted,board):
        print('Should use dervied class class moves!')

#classes inheriting from Piece
#virtual function derivedPieceMove calls performMoves
class Pawn(Piece):
    def derivedPieceMove(self,x,y,pieceID,player,isPromoted,board):
        pass

class King(Piece):
    def derivedPieceMove(self,x,y,pieceID,player,isPromoted,board):
        pass

class Gold(Piece):
    def derivedPieceMove(self,x,y,pieceID,player,isPromoted,board):
        pass

class Silver(Piece):
    def derivedPieceMove(self,x,y,pieceID,player,isPromoted,board):
        pass

class Rook(Piece):
    def derivedPieceMove(self,x,y,pieceID,player,isPromoted,board):
        pass

class Bishop(Piece):
    def derivedPieceMove(self,x,y,pieceID,player,isPromoted,board):
        pass

class dragonHorse(Piece):
    def derivedPieceMove(self,x,y,pieceID,player,isPromoted,board):
        pass

class dragonKing(Piece):
    def derivedPieceMove(self,x,y,pieceID,player,isPromoted,board):
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
#if trying to promote k or g, throw error
promotion = {'s':Gold,
             'b':dragonHorse,
             'r':dragonKing,
             'p':Gold}
