import argparse
import utils
import copy


N = 5
MOVES_LIMIT = 200
gameBoard = [[None for i in range(N)] for i in range(N)]
lower_captured = []
upper_captured = []

moves_count = 0

k_position = (-1,-1)
K_position = (-1,-1)

class Piece:

	def __init__(self, piece_type, position):
		self.piece_type = piece_type
		self.position = position
		self.promoted = False
		self.moveTypes = set([piece_type])

	def __str__(self):
		return "{}{}".format(('+' if self.promoted else ''), self.piece_type)

	def promote(self):
		if self.piece_type in ['K', 'k', 'g', 'G']:
			return
		self.promoted = True
		if self.piece_type == 'p':
			self.moveTypes = set(['g'])
		elif self.piece_type == 'P':
			self.moveTypes = set(['G'])
		elif self.piece_type == 's':
			self.moveTypes = set(['g'])
		elif self.piece_type == 'S':
			self.moveTypes = set(['G'])
		elif self.piece_type == 'b':
			self.moveTypes.add('k')
		elif self.piece_type == 'B':
			self.moveTypes.add('K')
		elif self.piece_type == 'r':
			self.moveTypes.add('k')
		elif self.piece_type == 'R':
			self.moveTypes.add('K')

	def demote(self):
		if self.piece_type in ['K', 'k', 'g', 'G']:
			return
		self.promoted = False
		self.moveTypes = set([self.piece_type])

	def possible_moves(self, gameBoard):

		all_moves = []
		for moveType in self.moveTypes:
			func = moves[moveType]
			all_moves.extend(func(self.position, gameBoard))
		return all_moves

def notSamePlayer(x1,y1,x2,y2,gameBoard):
	if (gameBoard[x1][y1] is None) or (gameBoard[x2][y2] is None):
		return True
	if gameBoard[x1][y1].piece_type.islower() and gameBoard[x2][y2].piece_type.islower():
		return False
	if gameBoard[x1][y1].piece_type.isupper() and gameBoard[x2][y2].piece_type.isupper():
		return False
	return True

def king_moves(curr_pos, gameBoard):
	
	valid_moves = []
	x = curr_pos[0]
	y = curr_pos[1]

	if (0 <= x+1 < N) and (0 <= y < N) and notSamePlayer(x,y,x+1,y,gameBoard):
		valid_moves.append((x+1,y))
	if (0 <= x+1 < N) and (0 <= y+1 < N) and notSamePlayer(x,y,x+1,y+1,gameBoard):
		valid_moves.append((x+1,y+1))
	if (0 <= x+1 < N) and (0 <= y-1 < N) and notSamePlayer(x,y,x+1,y-1,gameBoard):
		valid_moves.append((x+1,y-1))
	if (0 <= x < N) and (0 <= y+1 < N) and notSamePlayer(x,y,x,y+1,gameBoard):
		valid_moves.append((x,y+1))
	if (0 <= x < N) and (0 <= y-1 < N) and notSamePlayer(x,y,x,y-1,gameBoard):
		valid_moves.append((x,y-1))
	if (0 <= x-1 < N) and (0 <= y < N) and notSamePlayer(x,y,x-1,y,gameBoard):
		valid_moves.append((x-1,y))
	if (0 <= x-1 < N) and (0 <= y+1 < N) and notSamePlayer(x,y,x-1,y+1,gameBoard):
		valid_moves.append((x-1,y+1))
	if (0 <= x-1 < N) and (0 <= y-1 < N) and notSamePlayer(x,y,x-1,y-1,gameBoard):
		valid_moves.append((x-1,y-1))

	return valid_moves

def rook_moves(curr_pos, gameBoard):

	valid_moves = []
	x1 = curr_pos[0]
	y1 = curr_pos[1]

	for i in range(1,5):
		x2 = x1 - i
		y2 = y1
		if not (0 <= x2 < N):
			break
		if (0 <= x2 < N) and (0 <= y2 < N):
			if gameBoard[x2][y2] is not None:
				if notSamePlayer(x1,y1,x2,y2,gameBoard):
					valid_moves.append((x2,y2))
					break
				else:
					break
			else:
				valid_moves.append((x2,y2))
	
	for i in range(1,5):
		x2 = x1 + i
		y2 = y1
		if not (0 <= x2 < N):
			break
		if (0 <= x2 < N) and (0 <= y2 < N):
			if gameBoard[x2][y2] is not None:
				if notSamePlayer(x1,y1,x2,y2,gameBoard):
					valid_moves.append((x2,y2))
					break
				else:
					break
			else:
				valid_moves.append((x2,y2))

	for i in range(1,5):
		y2 = y1 - i
		x2 = x1
		if not (0 <= y2 < N):
			break
		if (0 <= x2 < N) and (0 <= y2 < N):
			if gameBoard[x2][y2] is not None:
				if notSamePlayer(x1,y1,x2,y2,gameBoard):
					valid_moves.append((x2,y2))
					break
				else:
					break
			else:
				valid_moves.append((x2,y2))

	for i in range(1,5):
		y2 = y1 + i
		x2 = x1
		if not (0 <= y2 < N):
			break
		if (0 <= x2 < N) and (0 <= y2 < N):
			if gameBoard[x2][y2] is not None:
				if notSamePlayer(x1,y1,x2,y2,gameBoard):
					valid_moves.append((x2,y2))
					break
				else:
					break
			else:
				valid_moves.append((x2,y2))


	return valid_moves

def bishop_moves(curr_pos, gameBoard):

	valid_moves = []
	x1 = curr_pos[0]
	y1 = curr_pos[1]

	for i in range(1,5):
		x2 = x1 + i
		y2 = y1 + i
		if not ((0 <= x2 < N) and (0 <= y2 < N)):
			break
		if (0 <= x2 < N) and (0 <= y2 < N):
			if gameBoard[x2][y2] is not None:
				if notSamePlayer(x1,y1,x2,y2,gameBoard):
					valid_moves.append((x2,y2))
					break
				else:
					break
			else:
				valid_moves.append((x2,y2))

	for i in range(1,5):
		x2 = x1 + i
		y2 = y1 - i
		if not ((0 <= x2 < N) and (0 <= y2 < N)):
			break
		if (0 <= x2 < N) and (0 <= y2 < N):
			if gameBoard[x2][y2] is not None:
				if notSamePlayer(x1,y1,x2,y2,gameBoard):
					valid_moves.append((x2,y2))
					break
				else:
					break
			else:
				valid_moves.append((x2,y2))

	for i in range(1,5):
		x2 = x1 - i
		y2 = y1 + i
		if not ((0 <= x2 < N) and (0 <= y2 < N)):
			break
		if (0 <= x2 < N) and (0 <= y2 < N):
			if gameBoard[x2][y2] is not None:
				if notSamePlayer(x1,y1,x2,y2,gameBoard):
					valid_moves.append((x2,y2))
					break
				else:
					break
			else:
				valid_moves.append((x2,y2))

	for i in range(1,5):
		x2 = x1 - i
		y2 = y1 - i
		if not ((0 <= x2 < N) and (0 <= y2 < N)):
			break
		if (0 <= x2 < N) and (0 <= y2 < N):
			if gameBoard[x2][y2] is not None:
				if notSamePlayer(x1,y1,x2,y2,gameBoard):
					valid_moves.append((x2,y2))
					break
				else:
					break
			else:
				valid_moves.append((x2,y2))

	return valid_moves

def gold_general_moves(curr_pos, gameBoard):

	valid_moves = []
	x = curr_pos[0]
	y = curr_pos[1]

	if gameBoard[x][y].piece_type.islower():
		
		x2 = x-1
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x-1
		y2 = y
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x+1
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x+1
		y2 = y
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))

	else:

		x2 = x-1
		y2 = y
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x-1
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x+1
		y2 = y
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x+1
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))

	return valid_moves

def silver_general_moves(curr_pos, gameBoard):

	valid_moves = []
	x = curr_pos[0]
	y = curr_pos[1]

	if gameBoard[x][y].piece_type.islower():
		
		x2 = x-1
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x-1
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x+1
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x+1
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))

	else:

		x2 = x-1
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x-1
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x+1
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
		x2 = x+1
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))

	return valid_moves

def pawn_moves(curr_pos, gameBoard):
	#if ends up in promotion zone, then promote automatically
	valid_moves = []
	x = curr_pos[0]
	y = curr_pos[1]

	if gameBoard[x][y].piece_type.islower():
		x2 = x
		y2 = y+1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))
	else:
		x2 = x
		y2 = y-1
		if (0 <= x2 < N) and (0 <= y2 < N) and notSamePlayer(x,y,x2,y2,gameBoard):
			valid_moves.append((x2,y2))

	return valid_moves

moves = {'k': king_moves, 'K': king_moves, 'r': rook_moves, 'R': rook_moves, 'b': bishop_moves, 'B': bishop_moves, 'g': gold_general_moves, 'G': gold_general_moves, 's': silver_general_moves, 'S': silver_general_moves, 'p': pawn_moves, 'P': pawn_moves}

def position_to_coord(pos):
	x = ord(pos[0]) - 97
	y = int(pos[1]) - 1
	if x > 4 or y > 4:
		return None
	return (x,y)

def coord_to_pos(coord):
	x = coord[0]
	y = coord[1]
	x = chr(ord('a')+x)
	y = str(y+1)
	return str(x+y)

def gameBoard_to_stringBoard(gameBoard): #print them as +p and so own if they are promoted
	stringBoard = [[str(gameBoard[i][j]) if gameBoard[i][j] != None else '' for j in range(N)] for i in range(N)]
	return stringBoard

def init_gameBoard(gameBoard):
	global k_position
	global K_position
	gameBoard[0][4] = Piece('R', (0,4))
	gameBoard[1][4] = Piece('B', (1,4))
	gameBoard[2][4] = Piece('S', (2,4))
	gameBoard[3][4] = Piece('G', (3,4))
	gameBoard[4][4] = Piece('K', (4,4))
	K_position = (4,4)
	gameBoard[4][3] = Piece('P', (4,3))
	gameBoard[0][1] = Piece('p', (0,1))
	gameBoard[0][0] = Piece('k', (0,0))
	k_position = (0,0)
	gameBoard[1][0] = Piece('g', (1,0))
	gameBoard[2][0] = Piece('s', (2,0))
	gameBoard[3][0] = Piece('b', (3,0))
	gameBoard[4][0] = Piece('r', (4,0))

def init_gameBoard_partial(gameBoard, init_pieces):
	
	global k_position
	global K_position

	for pp in init_pieces:
		piece = pp['piece']
		position = pp['position']
		position = position_to_coord(position)
		promote_it = False
		if piece[0] == '+':
			promote_it = True
			piece = piece[1:]
		gameBoard[position[0]][position[1]] = Piece(piece, position)
		if promote_it:
			gameBoard[position[0]][position[1]].promote()
		if piece == 'k':
			k_position = position
		if piece == 'K':
			K_position = position

	return

def create_upper_captured(upper_captured, input_uc):

	for p in input_uc:
		if p[0] == '+':
			p = p[1:]
		upper_captured.append(Piece(p.upper(), (-1,-1)))

def create_lower_captured(lower_captured, input_lc):

	for p in input_lc:
		if p[0] == '+':
			p = p[1:]
		lower_captured.append(Piece(p.lower(), (-1,-1)))


def move(gameBoard, move_played, lowers_turn, promote = False):
	
	global K_position
	global k_position

	start_pos = move_played[0]
	end_pos = move_played[1]

	#check if the move is valid
	piece_at_start_pos = gameBoard[start_pos[0]][start_pos[1]]
	if piece_at_start_pos == None:
		return -1
	if (piece_at_start_pos.piece_type.islower() and (not lowers_turn)) or (piece_at_start_pos.piece_type.isupper() and lowers_turn):
		return -1
	if end_pos not in piece_at_start_pos.possible_moves(gameBoard):
		return -1

	#see if any captures are to be done
	if gameBoard[end_pos[0]][end_pos[1]] is not None:
		captured_piece = gameBoard[end_pos[0]][end_pos[1]]
		captured_piece.demote()
		if lowers_turn:
			lower_captured.append(captured_piece)
		else:
			upper_captured.append(captured_piece)
		captured_piece.position = (-1,-1)
		if (lowers_turn and captured_piece.piece_type == 'K') or ((not lowers_turn) and captured_piece.piece_type == 'k'):
			return 0

	#update GameBoard and the piece's position
	gameBoard[end_pos[0]][end_pos[1]] = piece_at_start_pos
	gameBoard[start_pos[0]][start_pos[1]] = None
	piece_at_start_pos.position = end_pos

	#promotion check
	if promote and ((lowers_turn and end_pos[1] != 4) or ((not lowers_turn) and end_pos[1] != 0)):
		return -1

	#if pawn moves into the promotion zone, automatically promote him
	if promote or (piece_at_start_pos.piece_type == 'p' and end_pos[1] == 4) or (piece_at_start_pos.piece_type == 'P' and end_pos[1] == 0):
		piece_at_start_pos.promote()

	if (piece_at_start_pos.piece_type == 'K' and (not lowers_turn)):
		K_position = end_pos
	if (piece_at_start_pos.piece_type == 'k' and lowers_turn):
		k_position = end_pos

	return 1

def find_k(gameBoard):
	
	global k_position
	return k_position

def find_K(gameBoard):

	global K_position
	return K_position

def getAllUpperMoves(gameBoard):

	all_upper_moves = []
	for i in range(N):
		for j in range(N):
			if (gameBoard[i][j] is not None) and (gameBoard[i][j].piece_type.isupper()):
				ps_moves = gameBoard[i][j].possible_moves(gameBoard)
				for k in ps_moves:
					all_upper_moves.append(((i,j), k))
	return all_upper_moves

def getAllLowerMoves(gameBoard):

	all_lower_moves = []
	for i in range(N):
		for j in range(N):
			if (gameBoard[i][j] is not None) and (gameBoard[i][j].piece_type.islower()):
				ps_moves = gameBoard[i][j].possible_moves(gameBoard)
				for k in ps_moves:
					all_lower_moves.append(((i,j), k))
	return all_lower_moves

def moveWithoutEffect(gameBoard, move):

	#assumes move is valid
	#assumes a copy of gameBoard is passed in
	start_pos = move[0]
	end_pos = move[1]

	piece_at_start_pos = gameBoard[start_pos[0]][start_pos[1]]
	gameBoard[end_pos[0]][end_pos[1]] = piece_at_start_pos
	gameBoard[start_pos[0]][start_pos[1]] = None

	return gameBoard

def checkDetection(gameBoard, lowers_turn):

	if lowers_turn:

		kings_pos = find_k(gameBoard)
		#get all possible moves for all of opponent's active pieces
		opponents_moves = getAllUpperMoves(gameBoard)

		#if any of them end up on king's pos, then player is in check, else return
		inCheck = False
		for move in opponents_moves:
			if move[1] == kings_pos:
				inCheck = True
				break

		return inCheck

	else:

		kings_pos = find_K(gameBoard)
		#get all possible moves for all of opponent's active pieces
		opponents_moves = getAllLowerMoves(gameBoard)

		#if any of them end up on king's pos, then player is in check, else return
		inCheck = False
		for move in opponents_moves:
			if move[1] == kings_pos:
				inCheck = True
				break

		return inCheck

	return True

def getOutOfCheckMoves(gameBoard, lowers_turn):
	
	if lowers_turn:
		my_possible_moves = getAllLowerMoves(gameBoard)
		valid_moves = []
		#check which of these result in a non-check state
		for move in my_possible_moves:
			if not checkDetection(moveWithoutEffect(copy.deepcopy(gameBoard), move), lowers_turn):
				valid_moves.append(move)

		return valid_moves
	
	else:
		my_possible_moves = getAllUpperMoves(gameBoard)
		valid_moves = []
		#check which of these result in a non-check state
		for move in my_possible_moves:
			if not checkDetection(moveWithoutEffect(copy.deepcopy(gameBoard), move), lowers_turn):
				valid_moves.append(move)

		return valid_moves

	return None

def validDrop(gameBoard, piece, dropLocation, lowers_turn):

	if lowers_turn:

		piece = piece.upper()

		piece_to_drop = None
		for i in range(len(lower_captured)):
			if lower_captured[i].piece_type == piece:
				piece_to_drop = lower_captured[i]
				break
		if piece_to_drop is None:
			return -1
		
		lower_captured.remove(piece_to_drop)

		piece_to_drop.piece_type = piece_to_drop.piece_type.lower();
		piece_to_drop.demote()

		if gameBoard[dropLocation[0]][dropLocation[1]] is not None:
			return -1

		if piece == 'p' and dropLocation[1] == 4:
			return -1

		for i in range(N):
			if (gameBoard[dropLocation[0]][i] is not None) and (gameBoard[dropLocation[0]][i].piece_type == 'p'):
				return -1

		gameBoard[dropLocation[0]][dropLocation[1]] = piece_to_drop
		piece_to_drop.position = dropLocation

		if (checkDetection(gameBoard, (not lowers_turn)) and len(getOutOfCheckMoves(gameBoard, (not lowers_turn))) == 0):
			return -1

		return 1 

	else:

		piece = piece.lower()

		piece_to_drop = None
		for i in range(len(upper_captured)):
			if upper_captured[i].piece_type == piece:
				piece_to_drop = upper_captured[i]
				break
		if piece_to_drop is None:
			return -1
		
		upper_captured.remove(piece_to_drop)

		piece_to_drop.piece_type = piece_to_drop.piece_type.upper();
		piece_to_drop.demote()

		if gameBoard[dropLocation[0]][dropLocation[1]] is not None:
			return -1

		if piece == 'P' and dropLocation[1] == 0:
			return -1

		for i in range(N):
			if (gameBoard[dropLocation[0]][i] is not None) and (gameBoard[dropLocation[0]][i].piece_type == 'P'):
				return -1

		gameBoard[dropLocation[0]][dropLocation[1]] = piece_to_drop
		piece_to_drop.position = dropLocation

		if (checkDetection(gameBoard, (not lowers_turn)) and len(getOutOfCheckMoves(gameBoard, (not lowers_turn))) == 0):
			return -1

		return 1  

	return 1

def printIllegalMove(lowers_turn):
	print ("{} wins. Illegal move.".format('UPPER' if lowers_turn else 'lower'))

def printEnd(lowers_turn, last_cmd):
	global upper_captured
	global lower_captured
	global gameBoard
	print ("{} player action: {}".format('UPPER' if lowers_turn else 'lower', last_cmd))
	print (utils.stringifyBoard(gameBoard_to_stringBoard(gameBoard)))
	#print ("")
	print ("Captures UPPER:", *[p.piece_type for p in upper_captured])
	print ("Captures lower:", *[p.piece_type for p in lower_captured])
	print ("")
	print ("lower> " if lowers_turn else "UPPER> ")
	print ("")


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-i", action = 'store_true')
group.add_argument("-f", type = str)
args = parser.parse_args()

if (not args.i) and (args.f is None):
	print ("Select atleast one of -f and -i flags")
	exit(0)



if args.f is not None: #interactive mode
	
	info = utils.parseTestCase(args.f)
	#print (info)
	init_pieces = info['initialPieces']
	init_gameBoard_partial(gameBoard, init_pieces)
	create_upper_captured(upper_captured, info['upperCaptures'])
	create_lower_captured(lower_captured, info['lowerCaptures'])

	moves_to_play = info['moves']
	last_cmd = ''
	lowers_turn = True

	while moves_count < min(MOVES_LIMIT, len(moves_to_play)):
		moves_count += 1
		if (checkDetection(gameBoard, lowers_turn)):
			avail_moves = getOutOfCheckMoves(gameBoard, lowers_turn)
			if (len(avail_moves) == 0):
				printEnd(lowers_turn, last_cmd)
				print ("{} wins. Checkmate.".format('UPPER' if lowers_turn else 'lower'))
				exit(0)
			# else:
			# 	print ("{} player is in check!".format('lower' if lowers_turn else 'UPPER'))
			# 	print ("Available moves:")
			# 	for m in avail_moves:
			# 		print ("move {} {}".format(coord_to_pos(m[0]), coord_to_pos(m[1])))
		cmd = moves_to_play[moves_count-1]
		cmd = cmd.strip()
		last_cmd = copy.deepcopy(cmd)
		cmd = cmd.split()

		if len(cmd) > 4:
			printEnd(lowers_turn, last_cmd)
			printIllegalMove(lowers_turn)
			exit(0)

		if cmd[0] == 'move':

			start_pos = position_to_coord(cmd[1])
			end_pos = position_to_coord(cmd[2])

			if start_pos == None or end_pos == None:
				printEnd(lowers_turn, last_cmd)
				printIllegalMove(lowers_turn)
				exit(0)

			promote = False
			if len(cmd) == 4:
				if cmd[3] == 'promote':
					promote = True

			move_result = move(gameBoard, (start_pos, end_pos), lowers_turn, promote)
			if move_result == -1:
				printEnd(lowers_turn, last_cmd)
				printIllegalMove(lowers_turn)
				exit(0)
			if move_result == 0:
				printEnd(lowers_turn, last_cmd)
				print ("{} wins. Checkmate.".format('lower' if lowers_turn else 'UPPER'))
				exit(0)

		elif cmd[0] == 'drop':
			
			if len(cmd) > 3:
				printEnd(lowers_turn, last_cmd)
				printIllegalMove(lowers_turn)
				exit(0)

			piece_to_drop = cmd[1]
			dropLocation = cmd[2]
			dropLocation = position_to_coord(dropLocation)
			if dropLocation == None:
				printEnd(lowers_turn, last_cmd)
				printIllegalMove(lowers_turn)
				exit(0)

			drop_res = validDrop(gameBoard, piece_to_drop, dropLocation, lowers_turn)

			if (drop_res == -1):
				printEnd(lowers_turn, last_cmd)
				printIllegalMove(lowers_turn)
				exit(0)

		else:
			
			printEnd(lowers_turn, last_cmd)
			printIllegalMove(lowers_turn)
			exit(0)	
			
		lowers_turn = (not lowers_turn)


	printEnd(lowers_turn, last_cmd)
	if moves_count >= MOVES_LIMIT:
		print ("Tie game. Too many moves.")
		exit(0)




else:

	init_gameBoard(gameBoard)
	lowers_turn = True
	last_cmd = ''
	while moves_count < MOVES_LIMIT:
		moves_count += 1
		if moves_count > 1:
			print ("{} player action: {}".format('UPPER' if lowers_turn else 'lower', last_cmd))
		print (utils.stringifyBoard(gameBoard_to_stringBoard(gameBoard)))
		print ("")
		print ("Captures UPPER:", *[p.piece_type for p in upper_captured])
		print ("Captures lower:", *[p.piece_type for p in lower_captured])
		print ("")
		if (checkDetection(gameBoard, lowers_turn)):
			avail_moves = getOutOfCheckMoves(gameBoard, lowers_turn)
			if (len(avail_moves) == 0):
				print ("{} wins. Checkmate.".format('UPPER' if lowers_turn else 'lower'))
				exit(0)
			else:
				print ("{} player is in check!".format('lower' if lowers_turn else 'UPPER'))
				print ("Available moves:")
				for m in avail_moves:
					print ("move {} {}".format(coord_to_pos(m[0]), coord_to_pos(m[1])))
		print ("lower> " if lowers_turn else "UPPER> ", end="")
		cmd = input()
		cmd = cmd.strip()
		last_cmd = copy.deepcopy(cmd)
		cmd = cmd.split()

		if len(cmd) > 4:
			printIllegalMove(lowers_turn)
			exit(0)

		if cmd[0] == 'move':

			start_pos = position_to_coord(cmd[1])
			end_pos = position_to_coord(cmd[2])

			if start_pos == None or end_pos == None:
				printIllegalMove(lowers_turn)
				exit(0)

			promote = False
			if len(cmd) == 4:
				if cmd[3] == 'promote':
					promote = True

			move_result = move(gameBoard, (start_pos, end_pos), lowers_turn, promote)
			if move_result == -1:
				printIllegalMove(lowers_turn)
				exit(0)
			if move_result == 0:
				print ("{} wins. Checkmate.".format('lower' if lowers_turn else 'UPPER'))
				exit(0)

		elif cmd[0] == 'drop':
			
			if len(cmd) > 3:
				printIllegalMove(lowers_turn)
				exit(0)

			piece_to_drop = cmd[1]
			dropLocation = cmd[2]
			dropLocation = position_to_coord(dropLocation)
			if dropLocation == None:
				printIllegalMove(lowers_turn)
				exit(0)

			drop_res = validDrop(gameBoard, piece_to_drop, dropLocation, lowers_turn)

			if (drop_res == -1):
				printIllegalMove(lowers_turn)
				exit(0)

		else:
			
			printIllegalMove(lowers_turn)
			exit(0)	
			
		lowers_turn = (not lowers_turn)


	if moves_count >= MOVES_LIMIT:
		print ("Tie game. Too many moves.")
		exit(0)









