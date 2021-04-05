import numpy as np
from PIL import Image
import copy


def findBoardXY():
    boardX, boardY = -1, -1

    for i in range(H):
        for j in range(W):
            if boardArray[i][j].any() > 0:
                boardX, boardY = j, i
                break
        if boardX != -1:
            break

    print(str(boardY) + "," + str(boardX))
    return boardX, boardY


def findTileSize():
    for i in range(boardX, W):
        if np.array_equal(boardArray[boardY][i], blackColor):
            return i - boardX


def getTileColor(color):
    tilePath = folderPath + "\\tiles\\" + color + ".png"
    tileImg = Image.open(tilePath).convert('RGB')
    tileArray = np.array(tileImg, dtype='uint8')

    return tileArray[0][0]


def loadPieces():
    figureMap = dict([])

    figureNames = ["bishop", "king", "knight", "pawn", "queen", "rook"]
    whitePiecesPath = folderPath + "\\pieces\\white\\"
    blackPiecesPath = folderPath + "\\pieces\\black\\"

    for figure in figureNames:
        pieceImg = Image.open(whitePiecesPath+figure+".png").resize((tileSize, tileSize), resample=Image.NEAREST).convert('L')
        figureMap["white " + figure] = np.array(pieceImg, dtype='uint8') / 255
    for figure in figureNames:
        pieceImg = Image.open(blackPiecesPath+figure+".png").resize((tileSize, tileSize), resample=Image.NEAREST).convert('L')
        figureMap["black " + figure] = np.array(pieceImg, dtype='uint8') / 255

    return figureMap


def checkOccupied(x, y):

    for p in range(y, y + tileSize):
        for q in range(x, x + tileSize):
            if not np.array_equal(boardArray[p][q], whiteColor) and not np.array_equal(boardArray[p][q], blackColor):
                return True

    return False


def ssq(arg1, arg2):
    summ = 0
    for i in range(tileSize):
        for j in range(tileSize):
            summ += (arg1[i][j] - arg2[i][j]) ** 2
    return summ


def getFigure(x, y):
    tileOld = boardArray[y: y + tileSize, x: x + tileSize]
    tmp = Image.fromarray(tileOld).convert("L")
    tile = np.array(tmp, dtype='uint8') / 255

    for i in range(tileSize):
        for j in range(tileSize):
            if np.array_equal(tileOld[i][j], whiteColor) or np.array_equal(tileOld[i][j], blackColor):
                tile[i][j] = 0

    min = float('inf')
    fig = None

    for figureName, figureArray in figureMap.items():
        corrCoef = ssq(tile, figureArray)
        print(corrCoef, figureName)
        if corrCoef < min:
            min = corrCoef
            fig = figureName

    return fig


def fillMap():
    for i in range(8):
        for j in range(8):
            x = boardX + j * tileSize
            y = boardY + i * tileSize
            if checkOccupied(x, y):
                figureName = getFigure(x, y)
                chessBoard[i][j] = figureName


def boardToFEN():
    outputStr = ""

    for i in range(8):
        emptyCounter = 0

        for j in range(8):
            if chessBoard[i][j] is not None:
                if emptyCounter > 0:
                    outputStr += str(emptyCounter)
                    emptyCounter = 0

                color, figureName = chessBoard[i][j].split(" ")

                if color == "white":
                    if figureName == "knight":
                        outputStr += "N"
                    else:
                        outputStr += figureName[0].upper()
                if color == "black":
                    if figureName == "knight":
                        outputStr += "n"
                    else:
                        outputStr += figureName[0].lower()
            else:
                emptyCounter += 1
        if emptyCounter > 0:
            outputStr += str(emptyCounter)
        outputStr += "/"

    print(outputStr[:-1])


def horizontalCheck(p, q, color, checkList):
    moves = [[0, 1],
             [0, -1]]

    for move in moves:
        p1 = p + move[0]
        q1 = q + move[1]

        while 0 <= p1 <= 7 and 0 <= q1 <= 7:
            piece = chessBoard[p1][q1]

            if chessBoard[p1][q1] is not None:

                pieceColor, pieceFigure = piece.split(" ")

                if pieceColor != color:
                    if pieceFigure == "queen" or pieceFigure == "rook":
                        checkList.append((piece, p1, q1, move))
                    if pieceFigure == "king" and abs(q - q1) == 1:
                        checkList.append((piece, p1, q1, move))

                break
            p1 = p1 + move[0]
            q1 = q1 + move[1]


def verticalCheck(p, q, color, checkList):
    moves = [[-1, 0],
             [1, 0]]

    for move in moves:
        p1 = p + move[0]
        q1 = q + move[1]

        while 0 <= p1 <= 7 and 0 <= q1 <= 7:
            piece = chessBoard[p1][q1]

            if chessBoard[p1][q1] is not None:

                pieceColor, pieceFigure = piece.split(" ")

                if pieceColor != color:
                    if pieceFigure == "queen" or pieceFigure == "rook":
                        checkList.append((piece, p1, q1, move))
                    if pieceFigure == "king" and abs(p - p1) == 1:
                        checkList.append((piece, p1, q1, move))

                break
            p1 = p1 + move[0]
            q1 = q1 + move[1]


def diagonalsCheck(p, q, color, checkList):

    moves = [[-1, -1],
             [-1, 1],
             [1, 1],
             [1, -1]]

    for move in moves:
        p1 = p + move[0]
        q1 = q + move[1]

        while 0 <= p1 <= 7 and 0 <= q1 <= 7:
            piece = chessBoard[p1][q1]

            if chessBoard[p1][q1] is not None:

                pieceColor, pieceFigure = piece.split(" ")

                if pieceColor != color:
                    if pieceFigure == "queen" or pieceFigure == "bishop":
                        checkList.append((piece, p1, q1, move))
                    if pieceFigure == "king" and (abs(p - p1) == 1 or abs(q-q1) == 1):
                        checkList.append((piece, p1, q1, move))
                    if pieceFigure == "pawn":
                        if color == "white" and move == [p1-p, q1-q]:
                            checkList.append((piece, p1, q1, move))
                        if color == "black" and move == [p1-p, q1-q]:
                            checkList.append((piece, p1, q1, move))

                break
            p1 = p1 + move[0]
            q1 = q1 + move[1]


def knightCheck(p, q, color, checkList):
    moves = [[-1, -2],
             [-1, 2],
             [1, -2],
             [1, 2],
             [-2, -1],  # todo test primer 2, kada nisam imao 2 tj po x a po y je trebalo da mi zapravo fali, neki bug ima ovde sigurno sam izmenio x i y osu
             [-2, 1],
             [2, -1],
             [2, 1]]

    for move in moves:
        p1 = p + move[0]
        q1 = q + move[1]

        if 0 <= p1 <= 7 and 0 <= q1 <= 7:

            piece = chessBoard[p1][q1]

            if piece is not None:

                pieceColor, pieceFigure = piece.split(" ")

                if pieceColor != color:
                    if pieceFigure == "knight":
                        checkList.append((piece, p1, q1, move))
                continue


def checkCheckAtPositionWithColor(p, q, color, checkList):

    # todo Debug ovde za svaki da vidim gde sjebem
    horizontalCheck(p, q, color, checkList)

    verticalCheck(p, q, color, checkList)

    diagonalsCheck(p, q, color, checkList)

    knightCheck(p, q, color, checkList)

    #print(checkList)

    if len(checkList) > 0:
        return 1
    else:
        return 0


def checkCheck():

    for i in range(8):
        for j in range(8):
            if chessBoard[i][j] == "white king":
                checkList = []
                if checkCheckAtPositionWithColor(i, j, "white", checkList):
                    return "B", checkmateChecker(i, j, "white", checkList)
            elif chessBoard[i][j] == "black king":
                checkList = []
                if checkCheckAtPositionWithColor(i, j, "black", checkList):
                    return "W", checkmateChecker(i, j, "black", checkList)

    return "-", 0


def tryToMove(p, q, color):

    moves = [[0, 1],
             [0, -1],
             [1, 0],
             [-1, 0],
             [1, 1],
             [1, -1],
             [-1, 1],
             [-1, -1]]
    # todo da li stoji figura tu i jel sme da jede
    for move in moves:
        p1 = p + move[0]
        q1 = q + move[1]

        if 0 <= p1 <= 7 and 0 <= q1 <= 7:
            # ne sme svoju da jede

            oldPiece = chessBoard[p1][q1]

            if chessBoard[p1][q1] is not None:
                pieceColor, pieceFigure = oldPiece.split(" ")
                if pieceColor == color:
                    continue

            oldPiece = chessBoard[p1][q1]
            chessBoard[p1][q1] = color + " king"
            chessBoard[p][q] = None

            retVal = checkCheckAtPositionWithColor(p1, q1, color, [])

            chessBoard[p1][q1] = oldPiece
            chessBoard[p][q] = color + " king"

            if retVal == 0:
                return 1

    return 0


def tryToEat(iKing, jKing, colorKing, checkList):
    # Figure can be eaten if is in check todo check this statement

    pieceAttacker, iAttacker, jAttacker, moveAttacker = checkList[0]
    colorAttacker, figureAttacker = pieceAttacker.split(" ")

    eatList = []
    checkCheckAtPositionWithColor(iAttacker, jAttacker, colorAttacker, eatList)

    if len(eatList) == 0:
        return 0

    # Check if it can be eated only by king and if king is in check when he eats
    if len(eatList) == 1:
        pieceEater, iEater, jEater, _ = eatList[0]
        colorEater, figureEater = pieceEater.split(" ")

        # We tried to move king here and failed before
        if figureEater == "king":
            return 0

    # todo kad pojedes sa figurom, proveri da li je onda opet sah
    for eater in eatList:

        pieceEater, iEater, jEater, _ = eater
        colorEater, figureEater = pieceEater.split(" ")

        if figureEater == "king":
            continue

        chessBoard[iAttacker][jAttacker] = pieceEater
        chessBoard[iEater][jEater] = None

        retVal = checkCheckAtPositionWithColor(iKing, jKing, colorKing, [])

        chessBoard[iAttacker][jAttacker] = pieceAttacker
        chessBoard[iEater][jEater] = pieceEater

        if retVal == 0:
            return 1

    return 0


def tryToBlock(pK, qK, color, checkList):
    piece, pF, qF, move = checkList[0]
    _, figure = piece.split(" ")

    if figure == "knight":
        return 0


    blockableChessBoard = copy.deepcopy(chessBoard)
    i = pK + move[0]
    j = qK + move[1]
    while (i, j) != (pF, qF):
        blockableChessBoard[i][j] = -1
        i = i + move[0]
        j = j + move[1]

    #todo Ako blokiras proveri da li je opet sah kada blokiras
    for i in range(8):
        for j in range(8):
            if blockableChessBoard[i][j] == color + " knight":
                moves = [[-1, -2],
                         [-1, 2],
                         [1, -2],
                         [1, 2],
                         [-2, -1],
                         [-2, 1],
                         [2, -1],
                         [2, 1]]
                for move in moves:
                    iNew, jNew = i + move[0], j + move[1]
                    if 0 <= iNew <= 7 and 0 <= jNew <= 7:
                        if blockableChessBoard[iNew][jNew] == -1:

                            chessBoard[iNew][jNew] = color + " knight"
                            chessBoard[i][j] = None

                            retVal = checkCheckAtPositionWithColor(pK, qK, color, [])

                            chessBoard[iNew][jNew] = None
                            chessBoard[i][j] = color + " knight"

                            if retVal == 0:
                                return 1
            if blockableChessBoard[i][j] == color + " rook":
                moves = [[0, 1],
                         [0, -1],
                         [-1, 0],
                         [1, 0]]
                for move in moves:
                    iNew = i + move[0]
                    jNew = j + move[1]

                    while 0 <= iNew <= 7 and 0 <= jNew <= 7:
                        if blockableChessBoard[iNew][jNew] is not None:
                            if blockableChessBoard[iNew][jNew] == -1:

                                chessBoard[iNew][jNew] = color + " rook"
                                chessBoard[i][j] = None

                                retVal = checkCheckAtPositionWithColor(pK, qK, color, [])

                                chessBoard[iNew][jNew] = None
                                chessBoard[i][j] = color + " rook"

                                if retVal == 0:
                                    return 1
                            else:
                                break

                        iNew = iNew + move[0]
                        jNew = jNew + move[1]

            if blockableChessBoard[i][j] == color + " bishop":
                moves = [[-1, -1],
                         [-1, 1],
                         [1, 1],
                         [1, -1]]
                for move in moves:
                    iNew = i + move[0]
                    jNew = j + move[1]

                    while 0 <= iNew <= 7 and 0 <= jNew <= 7:
                        if blockableChessBoard[iNew][jNew] is not None:
                            if blockableChessBoard[iNew][jNew] == -1:
                                chessBoard[iNew][jNew] = color + " bishop"
                                chessBoard[i][j] = None

                                retVal = checkCheckAtPositionWithColor(pK, qK, color, [])

                                chessBoard[iNew][jNew] = None
                                chessBoard[i][j] = color + " bishop"

                                if retVal == 0:
                                    return 1
                            else:
                                break

                        iNew = iNew + move[0]
                        jNew = jNew + move[1]

            if blockableChessBoard[i][j] == color + " queen":
                moves = [[-1, -1],
                         [-1, 1],
                         [1, 1],
                         [1, -1],
                         [0, 1],
                         [0, -1],
                         [-1, 0],
                         [1, 0]]

                for move in moves:
                    iNew = i + move[0]
                    jNew = j + move[1]

                    while 0 <= iNew <= 7 and 0 <= jNew <= 7:
                        if blockableChessBoard[iNew][jNew] is not None:
                            if blockableChessBoard[iNew][jNew] == -1:
                                chessBoard[iNew][jNew] = color + " queen"
                                chessBoard[i][j] = None

                                retVal = checkCheckAtPositionWithColor(pK, qK, color, [])

                                chessBoard[iNew][jNew] = None
                                chessBoard[i][j] = color + " queen"

                                if retVal == 0:
                                    return 1
                            else:
                                break

                        iNew = iNew + move[0]
                        jNew = jNew + move[1]

            if blockableChessBoard[i][j] == color + " pawn":
                if color == "white":
                    moves = [[-1, 0]]
                else:
                    moves = [[1, 0]]

                for move in moves:
                    iNew = i + move[0]
                    jNew = j + move[1]

                    if 0 <= iNew <= 7 and 0 <= jNew <= 7:
                        if blockableChessBoard[iNew][jNew] == -1:
                            chessBoard[iNew][jNew] = color + " pawn"
                            chessBoard[i][j] = None

                            retVal = checkCheckAtPositionWithColor(pK, qK, color, [])

                            chessBoard[iNew][jNew] = None
                            chessBoard[i][j] = color + " pawn"

                            if retVal == 0:
                                return 1
    return 0


def checkmateChecker(p, q, color, checkList):
    # todo manuelno proveri listu i razloge za sah mat bez obzira na rezultate na petlji

    #print(checkList)

    movable = tryToMove(p, q, color)

    if len(checkList) > 1:
        #print("Double check " + str(movable))
        if movable:
            return 0
        else:
            return 1

    if movable:
        #print("Movable")
        return 0

    eatable = tryToEat(p, q, color, checkList)
    if eatable:
        #print("Eatable")
        return 0

    blockable = tryToBlock(p, q, color, checkList)
    if blockable:
        #print("Blockable")
        return 0

    #print("Checkmate")
    return 1


if __name__ == "__main__":
    DEBUG = True

    if DEBUG:
        folderPath = r"D:\PSIML_2021\d\set\0"
    else:
        folderPath = input()

    id = folderPath.split("\\")[-1]

    boardPath = folderPath + "\\" + str(id) + ".png"

    boardImg = Image.open(boardPath).convert('RGB')
    boardArray = np.array(boardImg, dtype='uint8')

    H, W, _ = boardArray.shape

    whiteColor = getTileColor("white")
    blackColor = getTileColor("black")

    boardX, boardY = findBoardXY()

    tileSize = findTileSize()

    chessBoard = np.array([[None for _ in range(8)] for _ in range(8)], dtype=object)

    figureMap = loadPieces()

    fillMap()

    boardToFEN()

    checkOut = checkCheck()
    print(checkOut[0])
    print(checkOut[1])
