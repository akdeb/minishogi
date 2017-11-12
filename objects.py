from utils import *
import pprint
from copy import *

class Minishogi(object):
    def __init__(self, vals):
        self.currentPlayer = lower
        self.currentMove = ''
        self.gameInCheck = False

        self.boardPieces = {}   #dict of objects
        self.capturedPieces = {lower:[], upper:[]}

        self.boardImage = [['' for i in range(5)] for j in range(5)]

        self.numberOfMoves = 0
        self.gameOver = False
        self.outMessage = ''
        self.waysOutofCheck = []

        # naturally, you'd want your pieces to be existing and
        # then you'd want to act on your set of moves
        self.placeAllPieces(vals['initialPieces'], vals['lowerCaptures'], vals['upperCaptures'])
        self.makeMovesArray(vals['moves'])
        self.main()

        #for debugging only
        #self.printPieces()
        # self.display()

    #HACK FOR DEBUGGING PURPOSES ONLY
    def printPieces(self):
        pprint.pprint(self.boardPieces)


    def possibleMovesOutOfCheck(self, player):
        possibleMoves = ['1']
        #check possible piece movements and check for a check
        #check for drops and check for check
        return possibleMoves


    def isKingExposed(self, king, allOtherPieces, playerWho):
        for piece in allOtherPieces:
            if piece.isMovePossibleDispatcher(piece.getPosition(), king.getPosition(), self.boardPieces, playerWho):
                return True
        return False


    #getting shadowing here
    def isInCheck(self, thePlayerInCheck):
        kingPieces = {}
        pieceColors = {upper:[], lower:[]}
        for position in self.boardPieces:
            currPlayer = self.boardPieces[position].getPlayer()
            if self.boardPieces[position].getPieceID() in uncapturablePieces:
                kingPieces[currPlayer] = self.boardPieces[position]
            pieceColors[currPlayer].append(self.boardPieces[position])
        if self.isKingExposed(kingPieces[thePlayerInCheck], pieceColors[oppositePlayer[thePlayerInCheck]], oppositePlayer[thePlayerInCheck]):
            return True
        return False


    def convertBackToBoardConfig(sel, position):
        x,y = position
        return str(chr(97+x)) + str(y+1)

    def isThisCheckmate(self, thePlayerInCheck):
        storeBoard = deepcopy(self.boardPieces)
        storeCaptures = deepcopy(self.capturedPieces)
        storeOutMessage = deepcopy(self.outMessage)
        gameOver = deepcopy(self.gameOver)

        finalPossibleMoves = []
        ourPiecesToMove = {}
        otherPlayerPieces = []
        ourKing = None
        for position in self.boardPieces:
            player = self.boardPieces[position].getPlayer()
            if ourKing == None and self.boardPieces[position].getPieceID() == self.correctCase('k',thePlayerInCheck):
                ourKing = self.boardPieces[position]
            if player == thePlayerInCheck:
                ourPiecesToMove[position] = self.boardPieces[position]
            else:
                otherPlayerPieces.append(self.boardPieces[position])
        # for pc in ourPiecesToMove:
        #     print(ourPiecesToMove[pc])

        for start in ourPiecesToMove:
            possibleEndPositionsForPiece = ourPiecesToMove[start].derivedPieceMove(start, self.boardPieces, thePlayerInCheck)
            for end in possibleEndPositionsForPiece:
                #restore these values with a deepcopy
                move = 'move ' + self.convertBackToBoardConfig(start) + ' ' + self.convertBackToBoardConfig(end)
                #print(move)
                self.applyMove(move.split(' '))
                if (not self.isKingExposed(ourKing, otherPlayerPieces, oppositePlayer[thePlayerInCheck])) and self.gameOver == False:
                    finalPossibleMoves.append(move)

                self.boardPieces = deepcopy(storeBoard)
                self.capturedPieces = deepcopy(storeCaptures)
                self.storeOutMessage = deepcopy(storeOutMessage)
                self.gameOver = deepcopy(gameOver)

        for piece in self.capturedPieces[thePlayerInCheck]:
            for x in range(5):
                for y in range(5):
                    move = 'drop ' + piece.getPieceID().lower() + ' ' + self.convertBackToBoardConfig((x,y))
                    #print(move + str(self.numberOfMoves))
                    self.applyDrop(move.split(' '))
                    #print(ourKing)
                    #print(str(self.isKingExposed(ourKing, otherPlayerPieces, oppositePlayer[thePlayerInCheck])))
                    if (not self.isKingExposed(ourKing, otherPlayerPieces, oppositePlayer[thePlayerInCheck])) and self.gameOver == False:
                        finalPossibleMoves.append(move)

                    self.boardPieces = deepcopy(storeBoard)
                    self.capturedPieces = deepcopy(storeCaptures)
                    self.storeOutMessage = deepcopy(storeOutMessage)
                    self.gameOver = deepcopy(gameOver)

        if len(finalPossibleMoves) == 0:
            return False
        self.waysOutofCheck = finalPossibleMoves
        return False

    def makeMovesArray(self, moves):
        for move in moves:
            sequence = move.split(' ')
            self.currentMove = move
            del self.waysOutofCheck[:]
            previousState = deepcopy(self.boardPieces)
            previousCaptures = deepcopy(self.capturedPieces)
            # case1: move <pos1> <pos2> (promote)
            # case2: drop <piece> <pos>
            # case3: anything else

            if (sequence[0] == 'move') and (len(sequence) == 3 or len(sequence) == 4):
                if not (self.isLegalPosition(sequence[1]) and self.isLegalPosition(sequence[2])):
                    self.gameOverExiting(1)
                elif len(sequence) == 4 and sequence[3] != 'promote':
                        self.gameOverExiting(1)
                else:
                    # APPLY MOVE HERE
                    self.applyMove(sequence)
            elif (sequence[0] == 'drop') and (len(sequence) == 3):
                if not (self.isLegalPosition(sequence[2])):
                    self.gameOverExiting(1)
                elif not (len(sequence[1]) == 1 and (sequence[1] in pieceTypes)):
                    self.gameOverExiting(1)
                else:
                    # APPLY DROP HERE
                    self.applyDrop(sequence)
            else:
                self.gameOverExiting(1)

            #setting back to previous state
            #two such cases:
            #moving into a check
            #dropping pawn for mate
            if self.isInCheck(self.currentPlayer):
                self.boardPieces = previousState
                self.capturedPieces = previousCaptures
                self.gameOverExiting(1)
            elif move[0] == 'drop' and move[1] == 'p':
                if self.isThisCheckmate(oppositePlayer[self.currentPlayer]):
                    self.boardPieces = previousState
                    self.capturedPieces = previousCaptures
                    self.gameOverExiting(1)
            else:
                #print('printing?')
                self.gameInCheck = False
            #print('nonlmao' + str(self.numberOfMoves))
            if self.isInCheck(oppositePlayer[self.currentPlayer]):
                #print('lmao' + str(self.numberOfMoves))
                if self.isThisCheckmate(oppositePlayer[self.currentPlayer]):
                    self.gameInCheck = False
                    self.gameOverExiting(2)
                self.gameInCheck = True

            #if the game is over, break
            if self.gameOver:
                break

            #FIXME try to fix the currentPlayer repitition problem
            self.currentPlayer = oppositePlayer[self.currentPlayer]
            self.numberOfMoves+=1

            #FIXME
            if self.numberOfMoves == 400:
                self.currentPlayer = oppositePlayer[self.currentPlayer]
                self.gameOverExiting(3)
                break

        #FIXME
        if not self.gameOver:
            self.currentPlayer = oppositePlayer[self.currentPlayer]
            self.gameOverExiting(200)
        return



    def applyMove(self, move):
        start = self.getCoordinates(move[1])
        end = self.getCoordinates(move[2])

        if (len(move) == 4):
            #already promoted piece being promoted
            if len(self.boardPieces[start].getPieceID()) == 2:
                self.gameOverExiting(1)
                return
            #wrong promotion [not going into, at, going out of promotion zone]
            if not (start[1] == promotionZone[self.currentPlayer] or end[1] == promotionZone[self.currentPlayer]):
                self.gameOverExiting(1)
                return
            #wrong piece being promoted [k,K,g,G]
            if self.boardPieces[start].getPieceID() in unpromotablePieces:
                self.gameOverExiting(1)
                return

        #gibberish piece
        if start not in self.boardPieces:
            self.gameOverExiting(1)
            return
        #moving other player's piece
        if self.boardPieces[start].getPlayer() != self.currentPlayer:
            self.gameOverExiting(1)
            return

        originalBoard = deepcopy(self.boardPieces)
        if not self.boardPieces[start].isMovePossibleDispatcher(start, end, originalBoard, self.currentPlayer):
            self.gameOverExiting(1)
            return

        #capture and capturing own piece
        if end in self.boardPieces:
            if self.boardPieces[end].getPlayer() == self.currentPlayer:
                self.gameOverExiting(1)
                return
            else:
                self.applyCapture(start, end)

        #modify board pieces dict
        self.boardPieces[end] = self.boardPieces[start]
        self.boardPieces[end].setPosition(end)
        del self.boardPieces[start]

        #first move a piece and then promote
        #FIXME maybe create a function for isPromotionZone()
        if len(move) == 4 or (self.boardPieces[end].getPieceID().lower() == 'p' and (start[1] == promotionZone[self.currentPlayer] or end[1] == promotionZone[self.currentPlayer])):
            self.applyPromote(end)



    #change letter case according to current player
    def correctCase(self, piece, playerWho):
        return piece.lower() if playerWho==lower else piece.upper()


    def applyCapture(self, start, end):
        capPiece = self.correctCase(self.boardPieces[end].getPieceID(), self.currentPlayer)
        self.capturedPieces[self.currentPlayer].append(shogiPieces[capPiece.lower()](capPiece[1] if len(capPiece) == 2 else capPiece, self.currentPlayer))
        del self.boardPieces[end]




    def applyDrop(self, move):
        place = self.getCoordinates(move[2])
        dropPiece =  self.correctCase(move[1], self.currentPlayer)

        #check if no piece exists at the drop spot
        if place in self.boardPieces:
            self.gameOverExiting(1)
            return

        #check if piece exists
        found = False
        if not any(pc.getPieceID() == dropPiece for pc in self.capturedPieces[self.currentPlayer]):
            self.gameOverExiting(1)
            return

        '''

        for pc in self.capturedPieces[self.currentPlayer]:
            if dropPiece == pc.getPieceID():
                found = True
                break
        if found is False:
            self.gameOverExiting(1)
            return
        '''

        if dropPiece.lower() == 'p':
            # same column pawn?
            if any((self.boardPieces[pc].getPieceID() == dropPiece) and (self.boardPieces[pc].getPosition()[0] == place[0]) for pc in self.boardPieces):
                self.gameOverExiting(1)
                return
            '''
            for pc in self.boardPieces:
                if (self.boardPieces[pc].getPieceID() in pawnSet) and (self.boardPieces[pc].getPosition()[0] == place[0]):
                    self.gameOverExiting(1)
                    return
            '''
            #dropping to promotion zone
            if place[1] == promotionZone[self.currentPlayer]:
                self.gameOverExiting(1)
                return
        '''
        obj = (pc.getPieceID() == dropPiece for pc in self.capturedPieces[self.currentPlayer]).next()
        if not obj:
            self.capturedPieces[self.currentPlayer].remove(pc)

        '''
        # drop the piece now
        for pc in self.capturedPieces[self.currentPlayer]:
            if pc.getPieceID() == dropPiece:
                self.boardPieces[place] = shogiPieces[dropPiece.lower()](dropPiece, self.currentPlayer, place, False)
                self.capturedPieces[self.currentPlayer].remove(pc)
                break
        return



    def applyPromote(self, end):
        newPieceID = '+' + self.boardPieces[end].getPieceID()
        self.boardPieces[end].setPieceID = newPieceID
        self.boardPieces[end].setIsPromoted = True
        newPiece = shogiPieces[newPieceID.lower()](newPieceID, self.currentPlayer, end, True)
        del self.boardPieces[end]
        self.boardPieces[end] = newPiece


    #check if sensible position
    #now check if within board
    def isLegalPosition(self, position):
        if len(position) != 2:
            return False
        return self.isWithinBoard(position)


    def isWithinBoard(self, position):
        if not ('a' <= position[0] <= 'e' and '1' <= position[1] <= '5'):
            return False
        return True

    #case 1: '<opposite> player wins. Illegal Move.'
    #case 2: '<current> player wins. Checkmate.'
    #case 3: 'Tie game. Too many moves.'
    def gameOverExiting(self, case):
        self.gameOver = True
        if case == 1:
            self.outMessage = oppositePlayer[self.currentPlayer] + ' player wins.  Illegal move.'
        elif case == 2:
            self.outMessage = self.currentPlayer + ' player wins.  Checkmate.'
        elif case == 3:
            self.outMessage = 'Tie game.  Too many moves.'
        else:
            self.outMessage = oppositePlayer[self.currentPlayer] + '> '



    def placeAllPieces(self, piecesOnBoard, lowerCaptures, upperCaptures):
        for pc in lowerCaptures:
            self.capturedPieces[lower].append(shogiPieces[pc](pc, lower))
        for pc in upperCaptures:
            self.capturedPieces[upper].append(shogiPieces[pc.lower()](pc, upper))
        for pc in piecesOnBoard:
            # case where piece is illegal
            if pc['piece'] not in allPossiblePieces:
                self.gameOverExiting(1)
                break
            self.boardPieces[self.getCoordinates(pc['position'])] = \
            shogiPieces[pc['piece'].lower()](pc['piece'], self.whichPlayer(pc['piece']), self.getCoordinates(pc['position']), len(pc['piece']) == 2)


    def whichPlayer(self, pieceID):
        if len(pieceID)==2:
            return upper if pieceID[1].isupper() else lower
        return upper if pieceID.isupper() else lower


    def getCoordinates(self, position):
        return (ord(position[0])-97, int(position[1])-1)

    def main(self):
        for pc in self.boardPieces:
            coord = self.boardPieces[pc].getPosition()
            self.boardImage[coord[0]][coord[1]] = self.boardPieces[pc].getPieceID()

        print(self.currentPlayer + ' player action: ' + self.currentMove)
        print(stringifyBoard(self.boardImage))
        print('Captures UPPER: ' + ' '.join([i.getPieceID() for i in self.capturedPieces[upper]]))
        print('Captures lower: ' + ' '.join([i.getPieceID() for i in self.capturedPieces[lower]]))
        if self.gameInCheck:
            print('\n' + oppositePlayer[self.currentPlayer] + ' player is in check!')
            print('Available moves:')
            for possibleMove in self.waysOutofCheck:
                print(possibleMove)
            print(self.outMessage)
        else:
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

    '''
    It is recommended that you check these funtions and change their implementation
    '''
    def isMovePossibleDispatcher(self, start, end, currentBoard, playerWho):
        if end in self.derivedPieceMove(start, currentBoard, playerWho):
            return True
        return False

    def stillInsideBoard(self, position):
        #'''checks if prospective piece position is on board'''
        x,y = position
        if x>=0 and x<5 and y>=0 and y<5:
            return True
        return False

    def noPossibleConflict(self, position, currentBoard, playerWho):
        #''' is there a conflict (without thinking of check) if there is a piece here'''
        if self.stillInsideBoard(position) and (position not in currentBoard or (currentBoard[position].getPlayer() != playerWho)):
            return True
        return False

    def performMovesIter(self,position,currentBoard,pieceMoves, playerWho):
        possibleMove = []
        pc_x, pc_y = position
        for xi,yi in pieceMoves:
            x,y = pc_x+xi, pc_y+yi
            while self.stillInsideBoard((x,y)):
                pieceAtXY = currentBoard.get((x,y),None)
                if pieceAtXY is None: possibleMove.append((x, y))
                elif playerWho != pieceAtXY.getPlayer():
                #and pieceAtXY.getPieceID() not in uncapturablePieces:
                #pieceAtXY.getPlayer() != self.getPlayer() and pieceAtXY.getPieceID() not in uncapturablePieces:
                    possibleMove.append((x,y))
                    break
                else:
                    break
                x,y = x+xi, y+yi
        return possibleMove

    # the gold general and silver general and pawn are unsymmetric
    def handleUnsymmetricPieces(self, val1, val2):
        return val1+val2 if self.getPlayer() == lower else val1-val2


    def derivedPieceMove(self,position, currentBoard, playerWho):
        print('Should use dervied class class moves!')

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


#classes inheriting from Piece
#virtual function derivedPieceMove calls performMoves
class Pawn(Piece):
    def derivedPieceMove(self,position, currentBoard, playerWho=None):
        if playerWho is None : playerWho = self.getPlayer()
        x,y=position
        return [(self.handleUnsymmetricPieces(x,i), self.handleUnsymmetricPieces(y,j)) for (i,j) in upsq if self.noPossibleConflict((self.handleUnsymmetricPieces(x,i),self.handleUnsymmetricPieces(y,j)), currentBoard, playerWho)]
        pass

class King(Piece):
    def derivedPieceMove(self,position, currentBoard, playerWho=None):
        if playerWho is None:
            playerWho = self.getPlayer()
        x,y=position
        return [(x+i, y+j) for (i,j) in udlr + topdiag + botdiag if self.noPossibleConflict((x+i, y+j), currentBoard, playerWho)]

class Gold(Piece):
    def derivedPieceMove(self,position, currentBoard, playerWho=None):
        if playerWho is None:
            playerWho = self.getPlayer()
        x,y = position
        return [(self.handleUnsymmetricPieces(x,i),self.handleUnsymmetricPieces(y,j)) for (i,j) in udlr + topdiag if self.noPossibleConflict((self.handleUnsymmetricPieces(x,i),self.handleUnsymmetricPieces(y,j)), currentBoard, playerWho)]

class Silver(Piece):
    def derivedPieceMove(self,position, currentBoard, playerWho=None):
        if playerWho is None:
            playerWho = self.getPlayer()
        x,y = position
        return [(self.handleUnsymmetricPieces(x,i),self.handleUnsymmetricPieces(y,j)) for (i,j) in topdiag + botdiag + upsq if self.noPossibleConflict((self.handleUnsymmetricPieces(x,i),self.handleUnsymmetricPieces(y,j)), currentBoard, playerWho)]

class Rook(Piece):
    def derivedPieceMove(self,position, currentBoard, playerWho=None):
        if playerWho is None:
            playerWho = self.getPlayer()
        return self.performMovesIter(position, currentBoard, udlr, playerWho)

class Bishop(Piece):
    def derivedPieceMove(self,position, currentBoard, playerWho=None):
        if playerWho is None:
            playerWho = self.getPlayer()
        return self.performMovesIter(position, currentBoard, topdiag+botdiag, playerWho)

class dragonHorse(King, Bishop):
    def derivedPieceMove(self,position, currentBoard, playerWho=None):
        if playerWho is None:
            playerWho = self.getPlayer()
        return King.derivedPieceMove(self, position,currentBoard, playerWho) + Bishop.derivedPieceMove(self, position, currentBoard, playerWho)


class dragonKing(King, Rook):
    def derivedPieceMove(self,position, currentBoard, playerWho=None):
        if playerWho is None:
            playerWho = self.getPlayer()
        return King.derivedPieceMove(self, position,currentBoard, playerWho) + Rook.derivedPieceMove(self, position, currentBoard, playerWho)


#define piece movements
udlr = [(0,1), (1,0), (0,-1), (-1,0)]
topdiag = [(1,1), (-1,1)]
botdiag = [(-1,-1), (1,-1)]
upsq = [(0,1)]

#these are all possible pieces
#for promoted pieces. see the plus
#call the class with the second letter
#and the case of the letter (upper case, lower case)
shogiPieces = {'k':King,
               'p':Pawn,
               's':Silver,
               'g':Gold,
               'r':Rook,
               'b':Bishop,
               '+s':Gold,
               '+b':dragonHorse,
               '+r':dragonKing,
               '+p':Gold}

lower = 'lower'
upper = 'UPPER'

oppositePlayer = {lower:upper, upper:lower}
allPossiblePieces = ['p','P',
                     'k','K',
                     'g', 'G',
                     's', 'S',
                     'b', 'B',
                     'r', 'R',
                     '+s', '+S',
                     '+b', '+B',
                     '+r', '+R',
                     '+p', '+P']

promotionZone = {lower:4, upper:0}
uncapturablePieces = ['k', 'K']
unpromotablePieces = ['k','g', 'K', 'G']
setOfPawns = {lower:['p','+p'],upper:['P','+P']}

#the type of pieces
pieceTypes = ['s','b','r','p','k','g']
