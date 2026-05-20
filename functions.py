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
    while (checkX, checkY) != (reqX, reqY) and checkX < 7 and checkY < 7:
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
        if canCastle(board, current, request, pieceColor):
            return (distX <= 1 and distY <= 1 and distX + distY > 0) or (distX == 2 and distY == 0)
        return distX <= 1 and distY <= 1 and distX + distY > 0

    if pieceClass == Pawn:
        if pieceColor == "White":
            if board[request[1]][request[0]] != "  ":
                return abs(current[0] - request[0]) == 1 and current[1] == (request[1] + 1)
            else:
                return collisionDetect(board, current, request) and current[0] - request[0] == 0 and (((current[1] == (request[1] + 2) and board[current[1]][current[0]] == board[current[1]][current[0]].upper()) or current[1] == (request[1] + 1)))

        if pieceColor == "Black":
            if board[request[1]][request[0]] != "  ":
                if abs(current[0] - request[0]) == 1 and current[1] == (request[1] - 1):
                    return abs(current[0] - request[0]) == 1 and current[1] == (request[1] - 1)
            else:
                if ((current[1] == (request[1] - 2) and board[current[1]][current[0]] == board[current[1]][current[0]].upper()) or current[1] == (request[1] - 1)):
                    return collisionDetect(board, current, request) and current[0] - request[0] == 0 and (((current[1] == (request[1] - 2) and board[current[1]][current[0]] == board[current[1]][current[0]].upper()) or current[1] == (request[1] - 1)))
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

def simulateMove(board, current, request):
    testBoard = copy.deepcopy(board)
    piece = testBoard[current[1]][current[0]]

    if piece == "  ":
        return None

    testBoard[request[1]][request[0]] = piece
    testBoard[current[1]][current[0]] = "  "
    return testBoard

def checkLegality(board, current, request, color):
    testBoard = simulateMove(board, current, request)
    if testBoard is None:
        return False

    kingPos = findKing(testBoard, color)
    if kingPos is None:
        return False

    enemyColor = "Black" if color == "White" else "White"

    return not attackCheck(testBoard, kingPos, enemyColor)

def updateCheck(board):
    global whiteInCheck
    global blackInCheck
    wKing = findKing(board, "White")
    bKing = findKing(board, "Black")
    whiteInCheck = attackCheck(board, wKing, "Black")
    blackInCheck = attackCheck(board, bKing, "White")
    return (whiteInCheck, blackInCheck)

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

                    piece = board[current[1]][current[0]]

                    if piece == "  " or colorDict[piece[0]] != color:
                        continue

                    pieceClass = typeDict[piece[1]]

                    if isValidMove(board, current, request, pieceClass, color):
                        if checkLegality(board, current, request, color):
                            return False

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