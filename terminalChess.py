from functions import *

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
    ["  ","  ","  ","  ","wR","  ","  ","  "],
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

# playing field: board[0][1] to board[7][8]
turn = 0
boardDisplay = True
lastWhitePassant = ""
lastBlackPassant = ""
whitePassantShadow = ""
blackPassantShadow = ""
validPromotions = ("R", "K", "B", "Q")
activePlayerInCheck = False

while True:
    checks = updateCheck(board)
    if turn % 2 == 0:
        playerColor = "w"
        activePlayerInCheck = checks[0]
        if len(whitePassantShadow) == 2 and board[whitePassantShadow[0]][whitePassantShadow[1]] == "w_":
            board[whitePassantShadow[0]][whitePassantShadow[1]] = "  "
    else:
        playerColor = "b"
        activePlayerInCheck = checks[1]
        if len(blackPassantShadow) == 2 and board[blackPassantShadow[0]][blackPassantShadow[1]] == "b_":
            board[blackPassantShadow[0]][blackPassantShadow[1]] = "  "
        
    if boardDisplay == True:
        boardDisplay = False
        for index, line in zip(rowDividers, board):
            print(index, line)
        print(board[8])
        print(colDividers)
    if checkmateCheck(board, "White"):
        print("White cannot escape check. Black wins!")
        break
    if checkmateCheck(board, "Black"):
        print("Black cannot escape check. White wins!")
        break
    if activePlayerInCheck == True:
        print("You are in check and must make a move to escape it.")


    pieceSelect = input(f"It's {colorDict[playerColor]}'s turn. Select a {colorDict[playerColor]} piece by tile index:\n")
    selectedPiecePosition = (colDict[pieceSelect.upper()[0]], rowDict[pieceSelect[1]])
    selectedPieceType = board[selectedPiecePosition[1]][selectedPiecePosition[0]]
    if selectedPieceType == "  ":
        print(selectedPieceType)
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
                    if checkLegality(board, currentTile, requestedTile, colorDict[playerColor]) == False:
                        print(f"That move would put you in check.")
                        continue
                    if board[requestedTile[1]][requestedTile[0]] != "  " and colorDict[board[requestedTile[1]][requestedTile[0]][0]] == pieceColor:
                        print(f"You may not capture your own pieces.")
                        continue
                    if pieceClass == Knight or collisionDetect(board, currentTile, requestedTile) == True:
                        if pieceClass == Pawn:
                            if pieceColor == "White":
                                if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] + 1) and board[requestedTile[1]][requestedTile[0]] != "  ":
                                    if board[requestedTile[1]][requestedTile[0]] == "b_":
                                        board[lastBlackPassant[0]][lastBlackPassant[1]] = "  "
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                    turnTaken = True
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
                                    else:
                                        print("Invalid move. Check piece movement rules with HELP.")
                                        continue
                                else:
                                    print("Invalid move. Check piece movement rules with HELP.")
                                    continue
                                if requestedTile[1] == 0:
                                    while True:
                                        promote = input("Congratulations, your Pawn has reached the end of the board! \n You may turn it into a Rook (R), Knight (N), Bishop (B), or Queen (Q).")
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
                                    else:
                                        print("Invalid move. Check piece movement rules with HELP.")
                                        continue
                                else:
                                    print("Invalid move. Check piece movement rules with HELP.")
                                    continue
                                if requestedTile[1] == 7:
                                    while True:
                                        promote = input("Congratulations, your Pawn has reached the end of the board! \n You may turn it into a Rook (R), Knight (N), Bishop (B), or Queen (Q).")
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
                            elif distanceCheck[0] <= 1 and distanceCheck[1] <= 1 and sum(distanceCheck) > 0:
                                board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                turnTaken = True
                            else:
                                print("Invalid move. Check piece movement rules with HELP.")
                        elif isValidMove(board, currentTile, requestedTile, pieceClass, pieceColor):
                            board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                            board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                            turnTaken = True


                        if turnTaken == True:
                            boardDisplay = True
                            turn += 1
                            break
                    else:
                        print("Invalid move. Your piece is being blocked.")
                        pass