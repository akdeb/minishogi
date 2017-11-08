'''
# Initial board setup
---------------------
5 | R| B| S| G| K|
4 |__|__|__|__| P|
3 |__|__|__|__|__|
2 | p|__|__|__|__|
1 | k| g| s| b| r|
    a  b  c  d  e

# Useful links relating to Chess
--------------------------------
1. https://impythonist.wordpress.com/2017/01/01/modeling-a-chessboard-and-mechanics-of-its-pieces-in-python/
2. https://codereview.stackexchange.com/questions/94465/enumerating-moves-for-a-chess-piece
3. https://codereview.stackexchange.com/questions/101574/chess-game-in-python

# TODO
------
Unify functionality
Do not create 2 functions for lower and UPPER
Try to unify it.

# Initial pieces
----------------
R/r - Rook
B/b - Bishop
S/s - Silver general
G/g - Gold general
K/k - King
P/p - Pawn

# Move pieces
[move <location1> <location2>]
-------------


# Promoted pieces
[move <location1> <location2> promote]
-----------------
Rules:
Pawn must be automatically promoted
Pieces:
----- +k/+K - NOT POSSIBLE
----- +g/+G - NOT POSSIBLE
+s/+S - Promoted Silver general (Moves like Gold general)
+b/+B - Promoted Bishop [called Dragon horse] (Moves like Bishop/King)
+r/+R - Promoted Rook [called Dragon king] (Moves like Rook/King)
+p/+P - Promoted Pawn (Moves like Gold general)

# Dropping pieces rules
[drop <lower case piece> <location>]
-----------------------
1. Cannot drop piece on top of another piece
2. Cannot drop 2 pawns (of the same player) in the same column
3. Cannot drop pawn on promotion zone
4. Cannot drop pawn for immediate checkmate
5. Dropped piece must start unpromoted. Promotion/Capture on next move only

# Game End
----------
1. Checkmate. Output: “<UPPER/lower> player wins. Checkmate.”
2. Both players >= 200 moves. Output: “Tie game. Too many moves.”
3. Illegal Move. Output: “<UPPER/lower> player wins. Illegal move.”

# Modes
-------

-> Interactive Mode
-------------------
1. Enter moves, decide on game

-> File Mode
------------
1. Calculate current board state move by move

# Some Questions I have
-----------------------
1. What's a good way to unify operations which are meant for lower and UPPER?
    -> without writing explict conditions for UPPER and lower, how can I
        write a single case that covers both possibilities by both players

2. Dropped piece must start unpromoted. Promotion/Capture on next move only
    -> WHAT does this even mean?

3. If we find a illegalMove, do we print the board status after that move and
    -> then quit? or do we quit right away?

4. When I drop a piece. Can there be an identical piece there on the board?
'''
