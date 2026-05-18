from functions import *
import pygame
import sys

pygame.init()

screenWidth = 500
screenHeight = screenWidth
screen = pygame.display.set_mode((screenWidth, screenHeight))
boardRender = pygame.image.load("Chess Images/board.png").convert()
boardRender = pygame.transform.scale(boardRender, (screenWidth, screenHeight))

tileSize = screenWidth/8

imageTypes = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
imageDict = {}

for pieceType in imageTypes:
    image = pygame.image.load(f"Chess Images/{pieceType}.png").convert_alpha()
    image = pygame.transform.scale(image, (tileSize, tileSize))
    imageDict[pieceType] = image

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
    
# playing field: board[0][1] to board[7][8]
turn = 0
boardDisplay = True
lastWhitePassant = ""
lastBlackPassant = ""
whitePassantShadow = ""
blackPassantShadow = ""
validPromotions = ("R", "K", "B", "Q")
activePlayerInCheck = False
running = True
gamestate = "start"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            colClicked = str(int(x/tileSize))
            rowClicked = str(int(y/tileSize))
            cord = colDict[colClicked] + str(rowDict[rowClicked])
            if gamestate == "started":
                gamestate = "select"
            if gamestate == "selected":
                gamestate = "move"
            print(f"Input: {cord}")
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_r, pygame.K_n, pygame.K_b, pygame.K_q) and gamestate == "promote":
            if event.key == pygame.K_r:
                board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + "R"
            elif event.key == pygame.K_n:
                board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + "N"
            elif event.key == pygame.K_b:
                board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + "B"
            elif event.key == pygame.K_q:
                board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + "Q"
            gamestate = "end"

            

    screen.blit(boardRender, (0, 0))

    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece not in ("  ", "w_", "b_"):
                x = col * tileSize
                y = row * tileSize

                screen.blit(imageDict[piece.lower()], (x, y))

    pygame.display.flip()

    if gamestate == "start":
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
            print(f"Turn {turn+1}: {colorDict[playerColor]} to move.")
            updateCheck(board)
        if checkmateCheck(board, "White"):
            print("White cannot escape check. Black wins!")
            gamestate = "checkmate"
        if checkmateCheck(board, "Black"):
            print("Black cannot escape check. White wins!")
            gamestate = "checkmate"
        if activePlayerInCheck == True:
            print("You are in check and must make a move to escape it.")
        gamestate = "started"

    if gamestate == "select":
        selectedPiecePosition = (int(colDict[cord[0]]), int(rowDict[cord[1]]))
        print(selectedPiecePosition)
        selectedPieceType = board[selectedPiecePosition[1]][selectedPiecePosition[0]]
        if selectedPieceType == "  ":
            print(f"Selected empty tile. Select a {colorDict[playerColor]} piece instead.")
            gamestate = "started"
        else:
            selectedPieceName = f"{colorDict[selectedPieceType[0]]} {typeDict[selectedPieceType[1]].__name__}"
            if colorDict[selectedPieceType[0]] != colorDict[playerColor]:
                print(f"Wrong color selected. Select a {colorDict[playerColor]} piece instead.")
                gamestate = "started"
            else:
                print(f"Selected {selectedPieceName} at {cord}.")
                gamestate = "selected"
                

    if gamestate == "move":
        pieceClass = typeDict[selectedPieceType[1]]
        pieceColor = colorDict[selectedPieceType[0]]
        print(f"If you would like to move the piece, click a tile. \n To deselect, click the tile again. \n")
        moveCord = (int(colDict[cord[0]]), int(rowDict[cord[1]]))
        print(moveCord)
        if moveCord == selectedPiecePosition:
            print("Deselected.")
            selectedPiecePosition = None
            moveCord = None
            gamestate = "started"
            
        else:
            currentTile = selectedPiecePosition
            requestedTile = moveCord
            if isValidMove(board, currentTile, requestedTile, pieceClass, pieceColor) == False:
                print("Invalid move. Check piece movement rules, or make sure nothing is in the way.")
                gamestate = "selected"
                pass
            elif checkLegality(board, currentTile, requestedTile, colorDict[playerColor]) == False:
                print("That move would put you in check.")
                gamestate = "selected"
                pass
            elif board[requestedTile[1]][requestedTile[0]] != "  " and colorDict[board[requestedTile[1]][requestedTile[0]][0]] == pieceColor:
                print("You may not capture your own pieces.")
                gamestate = "selected"
                pass
            else:
                if pieceClass == Knight or collisionDetect(board, currentTile, requestedTile) == True:
                    if pieceClass == Pawn:
                        if pieceColor == "White":
                            if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] + 1) and board[requestedTile[1]][requestedTile[0]] == "  ":
                                print("Pawns must capture when they move diagonally.")
                                gamestate = "selected"
                            if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] + 1) and board[requestedTile[1]][requestedTile[0]] != "  ":
                                if board[requestedTile[1]][requestedTile[0]] == "b_":
                                    board[lastBlackPassant[0]][lastBlackPassant[1]] = "  "
                                board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                gamestate = "end"
                            elif currentTile[0] == requestedTile[0]:
                                if currentTile[1] == (requestedTile[1] + 2) and board[currentTile[1]][currentTile[0]] == board[currentTile[1]][currentTile[0]].upper() and board[requestedTile[1]][requestedTile[0]] == "  ":
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                    board[requestedTile[1]+1][requestedTile[0]] = "w_"
                                    whitePassantShadow = (requestedTile[1]+1, requestedTile[0])
                                    lastWhitePassant = (requestedTile[1], requestedTile[0])
                                    gamestate = "end"
                                elif currentTile[1] == (requestedTile[1] + 1) and board[requestedTile[1]][requestedTile[0]] == "  ":
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                    gamestate = "end"
                                else:
                                    print("Invalid move. Check piece movement rules with HELP.")
                                    gamestate = "selected"
                            else:
                                print("Invalid move. Check piece movement rules with HELP.")
                                gamestate = "selected"
                            if requestedTile[1] == 0:
                                print("Congratulations, your Pawn has reached the end of the board! \n You may turn it into a Rook (R), Knight (K), Bishop (B), or Queen (Q).")
                                gamestate = "promote"
                                    
                                        
                        else:
                            if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] - 1) and board[requestedTile[1]][requestedTile[0]] == "  ":
                                print("Pawns must capture when they move diagonally.")
                                gamestate = "selected"
                            if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] - 1) and board[requestedTile[1]][requestedTile[0]] != "  ":
                                if board[requestedTile[1]][requestedTile[0]] == "w_":
                                    board[lastWhitePassant[0]][lastWhitePassant[1]] = "  "
                                board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], board[requestedTile[1]][requestedTile[0]]
                                board[currentTile[1]][currentTile[0]] = "  "
                                gamestate = "end"
                            elif currentTile[0] == requestedTile[0]:
                                if currentTile[1] == (requestedTile[1] - 2) and board[currentTile[1]][currentTile[0]] == board[currentTile[1]][currentTile[0]].upper() and board[requestedTile[1]][requestedTile[0]] == "  ":
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], board[requestedTile[1]][requestedTile[0]]
                                    board[requestedTile[1]-1][requestedTile[0]] = "b_"
                                    blackPassantShadow = (requestedTile[1]-1, requestedTile[0])
                                    lastBlackPassant = (requestedTile[1], requestedTile[0])
                                    board[currentTile[1]][currentTile[0]] = "  "
                                    gamestate = "end"
                                elif currentTile[1] == (requestedTile[1] - 1) and board[requestedTile[1]][requestedTile[0]] == "  ":
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], board[requestedTile[1]][requestedTile[0]]
                                    board[currentTile[1]][currentTile[0]] = "  "
                                    gamestate = "end"
                                else:
                                    print("Invalid move. Check piece movement rules with HELP.")
                                    gamestate = "selected"
                            else:
                                print("Invalid move. Check piece movement rules with HELP.")
                                gamestate = "selected"
                            if requestedTile[1] == 7:    
                                print("Congratulations, your Pawn has reached the end of the board! \n You may turn it into a Rook (R), Knight (K), Bishop (B), or Queen (Q).")
                                gamestate = "promote"
                                        
                    elif pieceClass == King:
                            distanceCheck = (abs(currentTile[0] - requestedTile[0]), abs(currentTile[1] - requestedTile[1]))
                            if distanceCheck[0] == 2 and canCastle(board, currentTile, requestedTile, pieceColor):
                                if requestedTile[0] - currentTile[0] == 2:
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                    board[currentTile[1]][5] = board[currentTile[1]][7]
                                    board[currentTile[1]][7] = "  "
                                    gamestate = "end"
                                else:
                                    board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                    board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                    board[currentTile[1]][3] = board[currentTile[1]][0]
                                    board[currentTile[1]][0] = "  "
                                    gamestate = "end"
                            elif distanceCheck[0] <= 1 and distanceCheck[1] <= 1 and sum(distanceCheck) > 0:
                                board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                                board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                                gamestate = "end"
                    elif isValidMove(board, currentTile, requestedTile, pieceClass, pieceColor):
                        board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]][0].lower() + board[currentTile[1]][currentTile[0]][1]
                        board[requestedTile[1]][requestedTile[0]], board[currentTile[1]][currentTile[0]] = board[currentTile[1]][currentTile[0]], "  "
                        gamestate = "end"

    if gamestate == "end":
        boardDisplay = True
        turn += 1
        gamestate = "start"
                    
pygame.quit()
sys.exit