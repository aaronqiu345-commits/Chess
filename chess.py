import copy
class Piece:
    def __init__(self, color, position):
        self.color = color
        self.pos = position

    def move_rules(self):
        print("This is a placeholder that you shouldn't be seeing.")

class Pawn(Piece):
    def move_rules(self):
        print("The Pawn moves forward 1 space.")
        print("On its first movement, it may move forward 2 spaces (denoted by full-caps).")
        print("It may only capture the diagonal left and right tiles in front of it.")
        print("Promotion: If a Pawn makes it to the end of the board, it may become any other non-King piece type.")
        print("En Passant: If a Pawn moves 2 tiles forwards, it may be captured by an opposing Pawn as if it had only moved 1 tile.")

class Rook(Piece):
    def move_rules(self):
        print("The Rook moves and captures in horizontal and vertical lines.")
        print("See King piece for castling rules.")

class Knight(Piece):
    def move_rules(self):
        print("The Knight moves 3 tiles per action in an L-shape. It may jump over other pieces this way.")
        print("i.e. 2 vertical 1 horizonal / 2 horizontal 1 vertical")

class Bishop(Piece):
    def move_rules(self):
        print("The Bishop moves and captures in diagonal lines.")

class Queen(Piece):
    def move_rules(self):
        print("The Queen moves and captures horizontally, vertically, and diagonally.")

class King(Piece):
    def move_rules(self):
        print("The King moves and captures 1 tile in any direction.")
        print("You may not make any moves that would put the King in danger.")
        print("Check: If the King is ever at risk of capture next turn, you must make a move to protect it.")
        print("If you cannot protect the King next turn, you lose.")
        print("Castling: The King may move 2 spaces towards a Rook, who will then jump over the King.")
        print("This may only be done if there is a clear path and neither piece has moved this game (denoted by full-caps).")

colDict = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,
           "0":"A","1":"B","2":"C","3":"D","4":"E","5":"F","6":"G","7":"H"}
rowDict = {"8":0,"7":1,"6":2,"5":3,"4":4,"3":5,"2":6,"1":7, "0":8}

typeDict = {"P":Pawn, "R":Rook, "N":Knight, "B":Bishop, "Q":Queen, "K":King}
colorDict = {"w":"White", "W":"White", "b":"Black", "B":"Black"}

rowDividers = ["8", "7", "6", "5", "4", "3", "2", "1"]
colDividers = ["  A"," B"," C"," D"," E"," F"," G"," H"]
board = [
    ["BR","bN","bB","bQ","BK","bB","bN","BR"],
    ["BP","BP","BP","BP","BP","BP","BP","BP"],
    ["  ","  ","  ","  ","  ","  ","  ","  "],
    ["  ","  ","  ","  ","  ","  ","  ","  "],
    ["  ","  ","  ","  ","  ","  ","  ","  "],
    ["  ","  ","  ","  ","  ","  ","  ","  "],
    ["WP","WP","WP","WP","WP","WP","WP","WP"],
    ["WR","wN","wB","wQ","WK","wB","wN","WR"],
    ["__________________________________________________"]
]

for i, row in enumerate(board[:8]):
    for j, piece in enumerate(row):
        if piece != "  ":
            posDex = (j, i)
            pieceColor = colorDict[piece[0]]
            pieceType = typeDict[piece[1]]
            piecePosition = (f"{colDict[str(posDex[0])]}{rowDict[str(posDex[1])]}")
            makePiece = pieceType(pieceColor, piecePosition)
            print(f"Created {pieceColor} {pieceType.__name__} at {piecePosition}")

def collisionDetect(board, current, request):
    curX = current[0]
    curY = current[1]
    reqX = request[0]
    reqY = request[1]
    
    dirX = reqX - curX
    dirY = reqY - curY
    # booleans are 0 or 1
    moveX = (dirX > 0) - (dirX < 0)
    moveY = (dirY > 0) - (dirY < 0)

    checkX = curX + moveX
    checkY = curY + moveY
    while (checkX, checkY) != (reqX, reqY):
        if board[checkY][checkX] != "  ":
            return False
        checkX += moveX
        checkY += moveY
    return True

def isValidMove(board, current, request, pieceClass, pieceColor):

    distX = abs(current[0] - request[0])
    distY = abs(current[1] - request[1])

    if pieceClass == Knight:
        return (distX, distY) in [(1,2),(2,1)]

    if pieceClass == Rook:
        if current[0] == request[0] or current[1] == request[1]:
            return collisionDetect(board, current, request)
        return False

    if pieceClass == Bishop:
        if distX == distY:
            return collisionDetect(board, current, request)
        return False

    if pieceClass == Queen:
        if current[0] == request[0] or current[1] == request[1] or distX == distY:
            return collisionDetect(board, current, request)
        return False

    if pieceClass == King:
        return distX <= 1 and distY <= 1 and distX + distY > 0

    if pieceClass == Pawn:
        if pieceColor == "White":
            if board[request[1]][request[0]] != "  ":
                return abs(current[0] - request[0]) == 1 and current[1] == (request[1] + 1)
            else:
                return ((current[1] == (request[1] + 2) and board[current[1]][current[0]] == board[current[1]][current[0]].upper()) or current[1] == (request[1] + 1))

        if pieceColor == "Black":
            if board[request[1]][request[0]] != "  ":
                if abs(current[0] - request[0]) == 1 and current[1] == (request[1] - 1):
                    return collisionDetect(board, current, request)
            else:
                if ((current[1] == (request[1] - 2) and board[current[1]][current[0]] == board[current[1]][current[0]].upper()) or current[1] == (request[1] - 1)):
                    return collisionDetect(board, current, request)
    return False

def findKing(board, color):
    target = color[0].upper() + "K"
    for y in range(8):
        for x in range(8):
            if board[y][x].upper() == target:
                return (x, y)
    return None

def attackCheck(board, current, enemyColor):
    startX = current[0]
    startY = current[1]

    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece == "  ":
                continue
            checkColor = colorDict[piece[0]]
            if checkColor != enemyColor:
                continue
            checkType = piece[1]
            distX = startX - x
            distY = startY - y

            if checkType == "P":
                if enemyColor == "White":
                    if distY == -1 and abs(distX) == 1:
                        return True
                else:
                    if distY == 1 and abs(distX) == 1:
                        return True
            elif checkType == "R":
                if distX == 0 or distY == 0:
                    if collisionDetect(board, (x, y), (startX, startY)):
                        return True
            elif checkType == "N":
                if (abs(distX), abs(distY)) in [(1,2),(2,1)]:
                    return True
            elif checkType == "B":
                if abs(distX) == abs(distY):
                    if collisionDetect(board, (x, y), (startX, startY)):
                        return True
            elif checkType == "Q":
                if distX == 0 or distY == 0 or abs(distX) == abs(distY):
                    if collisionDetect(board,(x, y), (startX, startY)):
                        return True
            elif checkType == "X":
                if abs(distX) <= 1 and abs(distY) <= 1:
                    return True
    return False

def checkLegality(board, current, request, color):
    testBoard = copy.deepcopy(board)

    piece = testBoard[current[1]][current[0]]
    testBoard[request[1]][request[0]] = piece
    testBoard[current[1]][current[0]] = "  "

    kingPos = findKing(testBoard, color)

    enemyColor = None
    if color == "White":
        enemyColor = "Black"
    if color == "Black":
        enemyColor = "White"
    inCheck = attackCheck(testBoard, kingPos, enemyColor)
    
    return not inCheck                

def updateCheck(board):
    global whiteInCheck
    global blackInCheck
    wKing = findKing(board, "White")
    bKing = findKing(board, "Black")
    whiteInCheck = attackCheck(board, wKing, "Black")
    blackInCheck = attackCheck(board, bKing, "White")

def checkmateCheck(board, color):
    if color == "White":
        enemyColor = "Black"
    else:
        enemyColor = "White"

    kingPos = findKing(board, color)
    
    if attackCheck(board, kingPos, enemyColor) == False:
        return False

    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece == "  " or colorDict[piece[0]] != color:
                continue

            current = (x, y)

            for reqY in range(8):
                for reqX in range(8):
                    request = (reqX, reqY)

                    if current == request:
                        continue

                    if checkLegality(board, current, request, color) and isValidMove(board, current, request, typeDict[piece[1]], colorDict[piece[0]]):
                        return False
    print("checkfinish")
    return True

def canCastle(board, current, request, color):
    king = board[current[1]][current[0]]
    if king[0] == king[0].upper():
        if color == "White":
            enemyColor = "Black"
        else:
            enemyColor = "White"
        
        if request[0] > current[0]:
            rookCol = 7
            checkEmpty = [current[0]+1, current[0]+2]
        else:
            rookCol = 0
            checkEmpty = [current[0]-1, current[0]-2, current[0]-3]

        rookPos = board[current[1]][rookCol]
        if rookPos == "  " or rookPos.upper() != rookPos:
            return False
        
        for tile in checkEmpty:
            if board[current[1]][tile] != "  ":
                return False
        
        for tile in checkEmpty[:2]:
            testBoard = copy.deepcopy(board)
            testBoard[current[1]][tile] = king
            testBoard[current[1]][current[0]] = "  "

            if attackCheck(testBoard, (tile, current[1]), enemyColor):
                return False
        
        return True


    

    
    
# playing field: board[0][1] to board[7][8]
turn = 0
boardDisplay = True
lastWhitePassant = ""
lastBlackPassant = ""
whitePassantShadow = ""
blackPassantShadow = ""
validPromotions = ("R", "K", "B", "Q")
whiteInCheck = False
blackInCheck = False
activePlayerInCheck = False

while True:
    updateCheck(board)
    if checkmateCheck(board, "White"):
        print("White cannot escape check. Black wins!")
        break
    if checkmateCheck(board, "Black"):
        print("Black cannot escape check. White wins!")
        break
    if turn % 2 == 0:
        playerColor = "w"
        activePlayerInCheck = whiteInCheck
        if len(whitePassantShadow) == 2 and board[whitePassantShadow[0]][whitePassantShadow[1]] == "w_":
            board[whitePassantShadow[0]][whitePassantShadow[1]] = "  "
    else:
        playerColor = "b"
        activePlayerInCheck = blackInCheck
        if len(blackPassantShadow) == 2 and board[blackPassantShadow[0]][blackPassantShadow[1]] == "b_":
            board[blackPassantShadow[0]][blackPassantShadow[1]] = "  "
        
    if boardDisplay == True:
        boardDisplay = False
        for index, line in zip(rowDividers, board):
            print(index, line)
        print(board[8])
        print(colDividers)
    if activePlayerInCheck == True:
        print("You are in check and must make a move to escape it.")

    pieceSelect = input(f"It's {colorDict[playerColor]}'s turn. Select a {colorDict[playerColor]} piece by tile index:\n")
    selectedPiecePosition = (colDict[pieceSelect.upper()[0]], rowDict[pieceSelect[1]])
    selectedPieceType = board[selectedPiecePosition[1]][selectedPiecePosition[0]]
    if selectedPieceType == "  ":
        print(f"Selected empty tile. Select a {colorDict[playerColor]} piece instead.")
    else:
        selectedPieceName = f"{colorDict[selectedPieceType[0]]} {typeDict[selectedPieceType[1]].__name__}"
        if colorDict[selectedPieceType[0]] != colorDict[playerColor]:
            print(f"Wrong color selected. Select a {colorDict[playerColor]} piece instead.")
        else:
            print(f"Selected {selectedPieceName} at {pieceSelect}.")
            while True:
                turnTaken = False
                pieceClass = typeDict[selectedPieceType[1]]
                pieceColor = colorDict[selectedPieceType[0]]
                typeSelect = input(f"If you would like to move the piece, input a tile. \n If you would like piece rules, input HELP. \n To deselect, input BACK. \n")
                if typeSelect.upper() == "BACK":
                    break
                if typeSelect.upper() == "HELP":
                    pieceClass.move_rules(pieceClass)
                if len(typeSelect) == 2:
                    currentTile = (colDict[pieceSelect[0].upper()], rowDict[pieceSelect[1]])
                    requestedTile = (colDict[typeSelect[0].upper()], rowDict[typeSelect[1]])
                    if isValidMove(board, currentTile, requestedTile, pieceClass, pieceColor) == False:
                        print("Invalid move. Check piece movement rules with HELP, or make sure nothing is in the way.")
                        continue
                    if checkLegality(board, currentTile, requestedTile, colorDict[playerColor]) == False:
                        print("That move would put you in check.")
                        continue
                    if board[requestedTile[1]][requestedTile[0]] != "  " and colorDict[board[requestedTile[1]][requestedTile[0]][0]] == pieceColor:
                        print("You may not capture your own pieces.")
                        continue
                    if pieceClass == Knight or collisionDetect(board, currentTile, requestedTile) == True:
                        if pieceClass == Pawn:
                            if pieceColor == "White":
                                if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] + 1) and board[requestedTile[1]][requestedTile[0]] != "  ":
                                    if board[requestedTile[1]][requestedTile[0]] == "b_":
                                        board[lastBlackPassant[0]][lastBlackPassant[1]] = "  "
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                elif currentTile[0] == requestedTile[0]:
                                    if currentTile[1] == (requestedTile[1] + 2) and board[currentTile[1]][currentTile[0]] == board[currentTile[1]][currentTile[0]].upper() and board[requestedTile[1]][requestedTile[0]] == "  ":
                                        board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                        board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                        board[requestedTile[1]+1][requestedTile[0]] = "w_"
                                        whitePassantShadow = (requestedTile[1]+1, requestedTile[0])
                                        lastWhitePassant = (requestedTile[1], requestedTile[0])
                                        turnTaken = True
                                    elif currentTile[1] == (requestedTile[1] + 1) and board[requestedTile[1]][requestedTile[0]] == "  ":
                                        board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                        board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                        turnTaken = True
                                if requestedTile[1] == 0:
                                    while True:
                                        promote = input("Congratulations, your Pawn has reached the end of the board! \n You may turn it into a Rook (R), Knight (K), Bishop (B), or Queen (Q).")
                                        if promote.upper() in validPromotions:
                                            board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + promote
                                            break
                            else:
                                if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] - 1) and board[requestedTile[1]][requestedTile[0]] != "  ":
                                    if board[requestedTile[1]][requestedTile[0]] == "w_":
                                        board[lastWhitePassant[0]][lastWhitePassant[1]] = "  "
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], board[requestedTile[1]][requestedTile[0]]
                                    board[currentTile[1]][currentTile[0]] = "  "
                                    turnTaken = True
                                elif currentTile[0] == requestedTile[0]:
                                    if currentTile[1] == (requestedTile[1] - 2) and board[currentTile[1]][currentTile[0]] == board[currentTile[1]][currentTile[0]].upper() and board[requestedTile[1]][requestedTile[0]] == "  ":
                                        board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                        board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], board[requestedTile[1]][requestedTile[0]]
                                        board[requestedTile[1]-1][requestedTile[0]] = "b_"
                                        blackPassantShadow = (requestedTile[1]-1, requestedTile[0])
                                        lastBlackPassant = (requestedTile[1], requestedTile[0])
                                        board[currentTile[1]][currentTile[0]] = "  "
                                        turnTaken = True
                                    elif currentTile[1] == (requestedTile[1] - 1) and board[requestedTile[1]][requestedTile[0]] == "  ":
                                        board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                        board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], board[requestedTile[1]][requestedTile[0]]
                                        board[currentTile[1]][currentTile[0]] = "  "
                                        turnTaken = True
                                if requestedTile[1] == 7:
                                    while True:
                                        promote = input("Congratulations, your Pawn has reached the end of the board! \n You may turn it into a Rook (R), Knight (K), Bishop (B), or Queen (Q).")
                                        if promote.upper() in validPromotions:
                                            board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + promote
                                            break
                        elif pieceClass == King:
                            distanceCheck = (abs(currentTile[0] - requestedTile[0]), abs(currentTile[1] - requestedTile[1]))
                            if distanceCheck[0] == 2 and canCastle(board, currentTile, requestedTile, pieceColor):
                                if requestedTile[0] - currentTile[0] == 2:
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                    board[currentTile[1]][5] = board[currentTile[1]][7]
                                    board[currentTile[1]][7] = "  "
                                    turnTaken = True
                                else:
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                    board[currentTile[1]][3] = board[currentTile[1]][0]
                                    board[currentTile[1]][0] = "  "
                                    turnTaken = True
                            else:
                                board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                turnTaken = True
                        else:
                            board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                            board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                            turnTaken = True
                        if turnTaken == True:
                            boardDisplay = True
                            turn += 0
                            break