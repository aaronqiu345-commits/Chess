from functions import *
import pygame
import sys

pygame.init()
pygame.font.init()

screenWidth = 500
screenHeight = screenWidth
text = pygame.font.SysFont('Arial', int(screenWidth/25))
textColor = (200, 50, 50)

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

def renderPieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]

            if piece not in ("  ", "w_", "b_"):
                x = col * tileSize
                y = row * tileSize

                screen.blit(imageDict[piece.lower()], (x, y))

def renderBoard():
    screen.blit(boardRender, (0, 0))
    if activePlayerInCheck == True:
        kingPos = findKing(board, playerColor)
        x = kingPos[0] * tileSize + tileSize/2
        y = kingPos[1] * tileSize + tileSize/2
        pygame.draw.circle(screen, (50, 50, 200), (x, y), 25, width=0)
    renderPieces()

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
    
# playing field: board[0][1] to board[7][8]
turn = 0
lastWhitePassant = ""
lastBlackPassant = ""
whitePassantShadow = ""
blackPassantShadow = ""
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
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_r, pygame.K_n, pygame.K_b, pygame.K_q) and gamestate == "promote":
            if event.key == pygame.K_r:
                board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + "R"
            elif event.key == pygame.K_n:
                board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + "N"
            elif event.key == pygame.K_b:
                board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + "B"
            elif event.key == pygame.K_q:
                board[requestedTile[1]][requestedTile[0]] = board[requestedTile[1]][requestedTile[0]][0] + "Q"
            renderBoard()
            gamestate = "end"

    pygame.display.flip()

    if gamestate == "promote":
        texts = ("Rook (R)", "Knight (N)", "Bishop (B)", "Queen (Q)")
        for i in range(4):
            screen.blit(text.render(texts[i], True, textColor), (20+i*120, screenHeight/2))

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
            updateCheck(board)
        if checkmateCheck(board, "White"):
            print("checkmate")
            screen.blit(text.render("Black wins!", True, textColor), (0.8*screenWidth/2, screenHeight/2))
            gamestate = "checkmate"
        if checkmateCheck(board, "Black"):
            print("checkmate")
            screen.blit(text.render("White wins!", True, textColor), (0.8*screenWidth/2, screenHeight/2))
            gamestate = "checkmate"
        renderBoard()
        gamestate = "started"

    if gamestate == "select":
        selectedPiecePosition = (int(colDict[cord[0]]), int(rowDict[cord[1]]))
        selectedPieceType = board[selectedPiecePosition[1]][selectedPiecePosition[0]]
        if selectedPieceType == "  ":
            gamestate = "started"
        else:
            selectedPieceName = f"{colorDict[selectedPieceType[0]]} {typeDict[selectedPieceType[1]].__name__}"
            if colorDict[selectedPieceType[0]] != colorDict[playerColor]:
                gamestate = "started"
            else:
                pieceClass = typeDict[selectedPieceType[1]]
                pieceColor = colorDict[selectedPieceType[0]]
                for row in range(8):
                    for col in range(8):
                        request = (row, col)
                        x = row * tileSize + tileSize/2
                        y = col * tileSize + tileSize/2

                        if request == selectedPiecePosition:
                            pygame.draw.circle(screen, (200, 50, 50), (x, y), 25, width=0)
                            renderPieces()
                            continue
                        if board[request[1]][request[0]] != "  " and colorDict[board[request[1]][request[0]][0]] == pieceColor:
                            continue
                        if not isValidMove(board, selectedPiecePosition, request, pieceClass, colorDict[playerColor]):
                            continue
                        if not checkLegality(board, selectedPiecePosition, request, colorDict[playerColor]):
                            continue

                        pygame.draw.circle(screen, (100,100,100), (x, y), 20, width=0)
                        renderPieces()

                gamestate = "selected"
                

    if gamestate == "move":

        moveCord = (int(colDict[cord[0]]), int(rowDict[cord[1]]))
        if moveCord == selectedPiecePosition:
            renderBoard()
            selectedPiecePosition = None
            moveCord = None
            gamestate = "started"
            
        else:
            currentTile = selectedPiecePosition
            requestedTile = moveCord
            if isValidMove(board, currentTile, requestedTile, pieceClass, pieceColor) == False:
                gamestate = "selected"
            elif checkLegality(board, currentTile, requestedTile, colorDict[playerColor]) == False:
                gamestate = "selected"
            elif board[requestedTile[1]][requestedTile[0]] != "  " and colorDict[board[requestedTile[1]][requestedTile[0]][0]] == pieceColor:
                gamestate = "selected"
            else:
                if pieceClass == Knight or collisionDetect(board, currentTile, requestedTile) == True:
                    if pieceClass == Pawn:
                        if pieceColor == "White":
                            if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] + 1) and board[requestedTile[1]][requestedTile[0]] == "  ":
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
                                    gamestate = "selected"
                            else:
                                gamestate = "selected"
                            if requestedTile[1] == 0:
                                gamestate = "promote"
                                    
                                        
                        else:
                            if abs(currentTile[0] - requestedTile[0]) == 1 and currentTile[1] == (requestedTile[1] - 1) and board[requestedTile[1]][requestedTile[0]] == "  ":
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
                                    gamestate = "selected"
                            else:
                                gamestate = "selected"
                            if requestedTile[1] == 7:    
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
        turn += 1
        gamestate = "start"
                    
pygame.quit()
sys.exit