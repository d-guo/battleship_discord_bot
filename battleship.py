import random

class Battleship:

    def __init__(self, player1ID, player2ID):
        self.player1ID = player1ID
        self.player2ID = player2ID
        self.playersStatus = {player1ID: False, player2ID: False} # True when board is set up
        self.boardsPrivate = {player1ID: self.initPlayBoard(), player2ID: self.initPlayBoard()}
        self.boardsTracking = {player1ID: self.initClearBoard(), player2ID: self.initClearBoard()}

        self.turn = 1

    def hit(self, playerID, hitloc):
        # return 0 for miss, 1 for hit, 2 for sink
        player = 1 if playerID == self.player1ID else 2
        if self.turn != player:
            return -1

        playerReceiveID = self.player1ID if self.player1ID != playerID else self.player2ID
        if self.boardsPrivate[playerReceiveID][hitloc[0]][hitloc[1]] in ['a', 'b', 'c', 'd', 'e']:
            hitFlag = True
            hitType = self.boardsPrivate[playerReceiveID][hitloc[0]][hitloc[1]]
        else:
            hitFlag = False

        self.boardsPrivate[playerReceiveID][hitloc[0]][hitloc[1]] = 2 if hitFlag else 1
        self.boardsTracking[playerID][hitloc[0]][hitloc[1]] = 2 if hitFlag else 1
        self.turn = 1 if player == 2 else 2

        gameOverFlag = self.allSunk(playerReceiveID)
        if gameOverFlag:
            return 3

        return 2 if hitFlag and not self.existsInBoard(playerReceiveID, hitType) else (1 if hitFlag else 0)
    
    def boardSetupRandom(self, playerID):
        needToPlace = ['e', 'd', 'c', 'b', 'a']
        sizes = {'a': 5, 'b': 4, 'c': 3, 'd': 3, 'e': 2}
        board = self.boardsPrivate[playerID]

        for _ in range(5):
            ship = needToPlace.pop()
            size = sizes[ship]
            
            while True:
                try:
                    head = (random.choice([i for i in range(8)]), random.choice([i for i in range(8)]))
                    orientation = random.choice(['H', 'V'])
                    proposed = []
                    for i in range(size):
                        if orientation == 'H':
                            proposed.append(board[head[0]][head[1] + i])
                        else:
                            proposed.append(board[head[0] + i][head[1]])
                    for p in proposed:
                        if p != 0:
                            raise Exception('collision when setting up board')
                    for i in range(size):
                        if orientation == 'H':
                            board[head[0]][head[1] + i] = 0
                            board[head[0]][head[1] + i] = ship
                        else:
                            board[head[0] + i][head[1]] = 0
                            board[head[0] + i][head[1]] = ship
                    print('reached end')
                    break
                except:
                    print('failed')
                    print(board)
                    print(ship)
                    print(size)
                    continue

    def boardSetup(self, playerID, boardString):
        # 5 ships
        # carrier - 5 - a
        # battleship - 4 - b
        # cruiser - 3 - c
        # submarine - 3 - d
        # destroyer - 2 - e
        # sample boardString
        # a A1 h
        # b B1 h
        # c C1 h
        # d D1 h
        # e E1 h
        pass


    def initClearBoard(self):
        board = [[0 for _ in range(8)] for _ in range(8)]
        return board
    
    def initPlayBoard(self):
        board = [[0 for _ in range(8)] for _ in range(8)]
        return board
    
    def existsInBoard(self, playerID, shipType):
        for row in self.boardsPrivate[playerID]:
            if shipType in row:
                return True
        return False
    
    def allSunk(self, playerID):
        for row in self.boardsPrivate[playerID]:
            for pos in row:
                if pos in ['a', 'b', 'c', 'd', 'e']:
                    return False
        return True