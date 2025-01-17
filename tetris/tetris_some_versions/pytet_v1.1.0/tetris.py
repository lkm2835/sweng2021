from matrix import *
from random import *
from enum import Enum

class TetrisState(Enum):
    Running = 0
    NewBlock = 1
    Finished = 2
### end of class TetrisState():

class Tetris():
    nBlockTypes = 0
    nBlockDegrees = 0
    setOfBlockObjects = 0
    iScreenDw = 0   # larget enough to cover the largest block
    nBlocks = 0

    @classmethod
    def init(cls, setOfBlockArrays):
        Tetris.nBlockTypes = len(setOfBlockArrays)
        Tetris.nBlockDegrees = len(setOfBlockArrays[0])
        Tetris.setOfBlockObjects = [[0] * Tetris.nBlockDegrees for _ in range(Tetris.nBlockTypes)]
        arrayBlk_maxSize = 0
        for i in range(Tetris.nBlockTypes):
            if arrayBlk_maxSize <= len(setOfBlockArrays[i][0]):
                arrayBlk_maxSize = len(setOfBlockArrays[i][0])
        Tetris.iScreenDw = arrayBlk_maxSize     # larget enough to cover the largest block

        for i in range(Tetris.nBlockTypes):
            for j in range(Tetris.nBlockDegrees):
                Tetris.setOfBlockObjects[i][j] = Matrix(setOfBlockArrays[i][j])
        return

##############################################################
### Data model related code
##############################################################

    @classmethod
    def initSetOfBlockArrays(cls):
        Tetris.nBlocks

        arrayBlks = [ [ [ 0, 0, 1, 0 ],     # I shape
                        [ 0, 0, 1, 0 ],     
                        [ 0, 0, 1, 0 ],     
                        [ 0, 0, 1, 0 ] ],   
                    [ [1, 0, 0],          # J shape
                        [1, 1, 1],          
                        [0, 0, 0] ],
                    [ [0, 0, 1],          # L shape
                        [1, 1, 1],          
                        [0, 0, 0] ],        
                    [ [1, 1],             # O shape
                        [1, 1] ],           
                    [ [0, 1, 1],          # S shape
                        [1, 1, 0],          
                        [0, 0, 0] ],
                    [ [0, 1, 0],          # T shape    
                        [1, 1, 1],          
                        [0, 0, 0] ],
                    [ [1, 1, 0],          # Z shape
                        [0, 1, 1],          
                        [0, 0, 0] ]         
                    ]

        Tetris.nBlocks = len(arrayBlks)
        setOfBlockArrays = [[0] * 4 for _ in range(Tetris.nBlocks)]

        def rotate(m_array):
            size = len(m_array)
            r_array = [[0] * size for _ in range(size)]

            for y in range(size):
                for x in range(size):
                    r_array[x][size-1-y] = m_array[y][x]

            return r_array

        for idxBlockType in range(Tetris.nBlocks):
            temp_array = arrayBlks[idxBlockType]
            setOfBlockArrays[idxBlockType][0] = temp_array
            for idxBlockDegree in range(1,4):
                temp_array = rotate(temp_array)
                setOfBlockArrays[idxBlockType][idxBlockDegree] = temp_array

        return setOfBlockArrays

##############################################################
##############################################################
##############################################################

    def createArrayScreen(self):
        self.arrayScreenDx = Tetris.iScreenDw * 2 + self.iScreenDx
        self.arrayScreenDy = self.iScreenDy + Tetris.iScreenDw
        self.arrayScreen = [[0] * self.arrayScreenDx for _ in range(self.arrayScreenDy)]
        for y in range(self.iScreenDy):
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][x] = 1
            for x in range(self.iScreenDx):
                self.arrayScreen[y][Tetris.iScreenDw + x] = 0
            for x in range(Tetris.iScreenDw):
                self.arrayScreen[y][Tetris.iScreenDw + self.iScreenDx + x] = 1

        for y in range(Tetris.iScreenDw):
            for x in range(self.arrayScreenDx):
                self.arrayScreen[self.iScreenDy + y][x] = 1

        return self.arrayScreen

    def __init__(self, iScreenDy, iScreenDx):
        self.iScreenDy = iScreenDy
        self.iScreenDx = iScreenDx
        self.idxBlockDegree = 0
        arrayScreen = self.createArrayScreen()
        self.iScreen = Matrix(arrayScreen)
        self.oScreen = Matrix(self.iScreen)
        self.justStarted = True
        return

    def accept(self, key):
        self.state = TetrisState.Running

        if key >= '0' and key <= '6':
            if self.justStarted == False:
                self.deleteFullLines()
            self.iScreen = Matrix(self.oScreen)
            self.idxBlockType = int(key)
            self.idxBlockDegree = 0
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            self.top = 0
            self.left = Tetris.iScreenDw + self.iScreenDx//2 - self.currBlk.get_dx()//2
            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk
            self.justStarted = False
            print()

            if self.tempBlk.anyGreaterThan(1):
                self.state = TetrisState.Finished
            self.oScreen = Matrix(self.iScreen)
            self.oScreen.paste(self.tempBlk, self.top, self.left)
            return self.state
        elif key == 'q':
            pass
        elif key == 'a': # move left
            self.left -= 1
        elif key == 'd': # move right
            self.left += 1
        elif key == 'y': # move down
            self.top += 1
        elif key == 'w': # rotate the block clockwise
            self.idxBlockDegree = (self.idxBlockDegree + 1) % Tetris.nBlockDegrees
            self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
        elif key == ' ': # drop the block
            while not self.tempBlk.anyGreaterThan(1):
                    self.top += 1
                    self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
                    self.tempBlk = self.tempBlk + self.currBlk
        else:
            print('Wrong key!!!')
            
        self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
        self.tempBlk = self.tempBlk + self.currBlk

        if self.tempBlk.anyGreaterThan(1):   ## 벽 충돌시 undo 수행
            if key == 'a': # undo: move right
                self.left += 1
            elif key == 'd': # undo: move left
                self.left -= 1
            elif key == 'y': # undo: move up
                self.top -= 1
                self.state = TetrisState.NewBlock
            elif key == 'w': # undo: rotate the block counter-clockwise
                self.idxBlockDegree = (self.idxBlockDegree - 1) % Tetris.nBlockDegrees
                self.currBlk = Tetris.setOfBlockObjects[self.idxBlockType][self.idxBlockDegree]
            elif key == ' ': # undo: move up
                self.top -= 1
                self.state = TetrisState.NewBlock
            
            self.tempBlk = self.iScreen.clip(self.top, self.left, self.top+self.currBlk.get_dy(), self.left+self.currBlk.get_dx())
            self.tempBlk = self.tempBlk + self.currBlk

        self.oScreen = Matrix(self.iScreen)
        self.oScreen.paste(self.tempBlk, self.top, self.left)

        return self.state

    def deleteFullLines(self):
        nDeleted = 0
        nScanned = self.currBlk.get_dy()

        if self.top + self.currBlk.get_dy() - 1 >= self.iScreenDy:
            nScanned -= (self.top + self.currBlk.get_dy() - self.iScreenDy)

        zero = Matrix([[ 0 for x in range(0, (self.iScreenDx - 2*Tetris.iScreenDw))]])
        for y in range(nScanned - 1, -1, -1):
            cy = self.top + y + nDeleted
            line = self.oScreen.clip(cy, 0, cy+1, self.oScreen.get_dx())
            if line.sum() == self.oScreen.get_dx():
                temp = self.oScreen.clip(0, 0, cy, self.oScreen.get_dx())
                self.oScreen.paste(temp, 1, 0)
                self.oScreen.paste(zero, 0, Tetris.iScreenDw)
                nDeleted += 1

        return nScanned

    def getScreen(self):
        return self.oScreen

### end of class Tetris():
    
