import pyglet
import os
import sys
from copy import deepcopy
from random import randint
from pyglet.window import mouse, key

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class mysudoku(pyglet.window.Window):
    bgimage = pyglet.image.load(resource_path('resources\menuPicture.png'))					## Loads background image
    easyButtonImg = pyglet.image.load(resource_path('resources/easyButton.png'))			## Loads Easy button image
    mediumButtonImg = pyglet.image.load(resource_path('resources/mediumButton.png'))		## Loads Medium button image
    hardButtonImg = pyglet.image.load(resource_path('resources/hardButton.png'))			## Loads Hard button image
    exitButtonImg = pyglet.image.load(resource_path('resources/exitButton.png'))			## Loads Exit button image
    gridimage = pyglet.image.load(resource_path('resources/sudokuGrid.jpg'))				## Loads blank grid image
    selectedBox = pyglet.image.load(resource_path('resources/selectedBox.png'))				## Loads the Selected box image to distinguish selected square
    fixedBox = pyglet.image.load(resource_path('resources/fixedBox.png'))					## Loads the Fixed box image to distinguish selected uneditable square
    checkButtonImg = pyglet.image.load(resource_path('resources/checkButton.png'))			## Loads Check button image
    checkClickedImg = pyglet.image.load(resource_path('resources/checkClicked.png'))		## Loads Check button image for clicking animation
    backButtonImg = pyglet.image.load(resource_path('resources/backButton.png'))			## Loads Back button image
    resetButtonImg = pyglet.image.load(resource_path('resources/resetButton.png'))			## Loads Reset button image
    resetClickedImg = pyglet.image.load(resource_path('resources/resetClicked.png'))		## Loads Reset button image for clicking animation
    icon = pyglet.image.load(resource_path('resources/icon.png'))
    finalBoard = []								## Array that will store the final solution
    startBoard = []								## Array that will store the initial puzzle
    playBoard = []								## Array that will store the initial puzzle plus user's solution
    spriteArray = []							## Array that will store the sprites that distinguish selected squares
    labelBoard = []								## Array that will store the labels on each square
    currentX = 0								## Column index
    currentY = 0								## Row index
    boardDiff = resource_path('resources/easyBoards.txt')			## Path of file from which puzzle and solution will be loaded
    win = False								## Boolean to check if game won
    winLabel = pyglet.text.Label 				## Label for the winning message
    checkButton = pyglet.sprite.Sprite 			## Sprite for the check button
    checkClicked = pyglet.sprite.Sprite 		## Sprite for the check clicked button (for clicking animation)
    backButton = pyglet.sprite.Sprite 			## Sprite for the back button
    resetButton = pyglet.sprite.Sprite 			## Sprite for the reset button
    resetClicked = pyglet.sprite.Sprite 		## Sprite for the reset clicked button (for clicking animation)
    easyButton = pyglet.sprite.Sprite 			## Sprite for the easy button
    mediumButton = pyglet.sprite.Sprite 		## Sprite for the medium button
    hardButton = pyglet.sprite.Sprite 			## Sprite for the hard button
    exitButton = pyglet.sprite.Sprite 			## Sprite for the exit button
    winBackButton = pyglet.sprite.Sprite 		## Sprite for the back button on win screen 
    menu = True									## Boolean to check if in menu

    def __init__(self):
        super(mysudoku, self).__init__(594, 650,							## Creates window
                                       resizable=False,
                                       caption='Sudoku',
                                       config=pyglet.gl.Config(double_buffer=True),
                                       vsync=False)
        self.set_icon(self.icon)
        self.create_menu_buttons()											## Creates menu buttons


    def start_game(self):						## Starts game
        self.getBoard()							## Stores boards in the arrays
        self.create_labels()					## Creates all the board labels
        self.create_sprites()					## Creates all the box sprites
        self.create_buttons()					## Creates all buttons in game window
        self.spriteArray[self.currentY][self.currentX].visible = True	## Make top-left sprite selected
        self.winLabel = pyglet.text.Label('Congratulations! You win.',		## Creates winning label
                                          font_name = 'Georgia',
                                          font_size = 30, color = (32, 154, 187, 255),
                                          x = self.width // 2, y = self.height // 2,
                                          anchor_x = 'center', anchor_y = 'center')
        self.win = False						## Set win to False

    def getBoard(self):							## Gets all the boards
        self.finalBoard = []
        self.startBoard = []
        numLines = 0
        with open(self.boardDiff) as boardFile:			## Counts number of lines in txt
            for line in boardFile:
                numLines += 1
        numBoards = numLines // 18						## Calculates number of boards in txt
        boardNum = randint(0,numBoards-1)				## Generates a random integer
        with open(self.boardDiff) as boardFile:			## Gets the final solution and stores in finalBoard list
            for i in range(boardNum*18):
                boardFile.readline()
            for i in range(9):
                lineArray = boardFile.readline().strip('\n')
                x = []
                for i in lineArray:
                    x.append(int(i))
                self.finalBoard.append(x)
            for i in range(9):							## Gets the starting puzzle and stores in startBoard list
                lineArray = boardFile.readline().strip('\n')
                x=[]
                for i in lineArray:
                    x.append(int(i))
                self.startBoard.append(x)
        self.playBoard = deepcopy(self.startBoard)		## Deep copies the startBoard list to playBoard list
        #### ALL LISTS ARE TWO-DIMENSIONAL
    
    def on_draw(self):							## Funtion that runs when window is drawn
        self.clear()							## Clear window
        self.bgimage.blit(0,0)					## Blit background image
        if self.menu:							## Check if in menu
            self.draw_menu_buttons()			## If yes, draw menu buttons
        elif self.win:							## Check if game won
            self.draw_win()						## If yes, draw win screen
        else:
            self.gridimage.blit(0, 56)			## Draw blank grid
            self.draw_labels()					## Draw grid lablels
            self.draw_sprites()					## Draw all sprites
            self.draw_buttons()					## Draw game buttons

    def on_mouse_press(self, x, y, button, modifiers):
        if self.menu:							## If in menu
            if button == mouse.LEFT:			## Left mouse button
                if 227 < x < 367:
                    if 300 < y < 340:			## If Easy button clicked
                        self.boardDiff = resource_path('resources/easyBoards.txt')		## Load easy boards txt
                        self.start_game()
                        self.menu = False
                    elif 250 < y < 290:			## If Medium button clicked
                        self.boardDiff = resource_path('resources/mediumBoards.txt')	## Load medium boards txt
                        self.start_game()
                        self.menu = False
                    elif 200 < y < 240:			## If Hard button clicked
                        self.boardDiff = resource_path('resources/hardBoards.txt')		## Load hard boards txt
                        self.start_game()
                        self.menu = False
                    elif 150 < y < 190:			## If Exit clicked
                        self.close()			## Close program
        elif self.win:							## If on win screen
            if button == mouse.LEFT:			## Left mouse button
                if 227 < x < 367:
                    if 250 < y < 290:			## If Back button clicked
                        self.win = False
                        self.menu = True		## Goto menu
        else:									## If on game screen
            if y > 56:							## If clicked anywhere on grid
                if button == mouse.LEFT:		## Left mouse button
                    if self.currentX != x//66 or self.currentY != 8-(y-56)//66:			## If not already on the box
                        self.spriteArray[self.currentY][self.currentX].visible = False	## Make currently selected square disappear
                    self.currentX = x // 66							## Set current box column index
                    self.currentY = 8 - ((y-56) // 66)				## Set current box row index
                    if self.spriteArray[self.currentY][self.currentX].visible:			## If box already selected
                        if self.startBoard[self.currentY][self.currentX] == 0:			## If square is editable
                            if self.playBoard[self.currentY][self.currentX] == 9:		## If value is 9
                                self.playBoard[self.currentY][self.currentX] = 0		## Set value 0
                                self.labelBoard[self.currentY][self.currentX].text = ''	## Set label blank
                            else:
                                self.playBoard[self.currentY][self.currentX] += 1		## Increment square value
                                self.labelBoard[self.currentY][self.currentX].text = str(self.playBoard[self.currentY][self.currentX])		## Set square label
                            self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)		## Set label color to blue
                    else:
                        self.spriteArray[self.currentY][self.currentX].visible = True	## Set square as selected
                elif button == mouse.RIGHT:		## Right mouse button
                    if self.startBoard[self.currentY][self.currentX] == 0:				## If square is editable			
                        if self.playBoard[self.currentY][self.currentX] == 0:			## If square currently blank
                            self.playBoard[self.currentY][self.currentX] = 9			## Set value 9
                            self.labelBoard[self.currentY][self.currentX].text = '9'	## Set label 9
                        else:
                            self.playBoard[self.currentY][self.currentX] -= 1			## Decrement square value
                            if self.playBoard[self.currentY][self.currentX] == 0:		## If value is 0
                                self.labelBoard[self.currentY][self.currentX].text = ''	## Set label blank
                            else:
                                self.labelBoard[self.currentY][self.currentX].text = str(self.playBoard[self.currentY][self.currentX])		## Set square label
                        self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)			## Set label color to blue

            elif y > 8 and y < 48 and button == mouse.LEFT:
                if x > 29 and x < 169:								## If Check button clicked
                    self.checkButton.visible = False				## Clicking animation
                    self.checkClicked.visible = True
                    self.check()									## Run check button
                elif x > 425 and x < 565:							## If Back button clicked
                    self.menu = True								## Goto menu
                elif x > 227 and x < 367:							## If Reset button clicked
                    self.resetButton.visible = False				## Clicking animation
                    self.resetClicked.visible = True
                    self.reset_board()								## Reset board to initial puzzle

    def on_mouse_release(self, x, y, button, modifiers):
        if self.menu or self.win:
            pass
        else:														## If on game screen
            if button == mouse.LEFT:								## Left mouse button
                if self.checkClicked.visible:						## Check click animation
                    self.checkClicked.visible = False
                    self.checkButton.visible = True
                elif self.resetClicked.visible:						## Reset click animation
                    self.resetClicked.visible = False
                    self.resetButton.visible = True

    def on_key_press(self, symbol, modifiers):
        if self.win or self.menu:
            pass
        else:														## If on game screen
            if symbol == key.UP:									## If UP key pressed
                self.spriteArray[self.currentY][self.currentX].visible = False
                if self.currentY == 0:								## If on topmost square
                    self.currentY = 8								## Move to bottommost square
                else:
                    self.currentY -= 1								## Move to above square
                self.spriteArray[self.currentY][self.currentX].visible = True
            elif symbol == key.DOWN:								## If DOWN key pressed
                self.spriteArray[self.currentY][self.currentX].visible = False
                if self.currentY == 8:								## If on bottommost square
                    self.currentY = 0								## Move to topmost square
                else:
                    self.currentY += 1								## Move to square beneath
                self.spriteArray[self.currentY][self.currentX].visible = True
            elif symbol == key.RIGHT:								## If RIGHT key pressed
                self.spriteArray[self.currentY][self.currentX].visible = False
                if self.currentX == 8:								## If on rightmost square
                    self.currentX = 0								## Move to leftmost square
                else:
                    self.currentX += 1								## Move to square on right
                self.spriteArray[self.currentY][self.currentX].visible = True
            elif symbol == key.LEFT:								## If LEFT key pressed
                self.spriteArray[self.currentY][self.currentX].visible = False
                if self.currentX == 0:								## If on leftmost square
                    self.currentX = 8								## Move to rightmost square
                else:
                    self.currentX -= 1								## Move to square on left
                self.spriteArray[self.currentY][self.currentX].visible = True
            elif symbol == key.ENTER or symbol == key.RETURN:		## If ENTER or RETURN pressed
                self.check()										## Run check function
            elif self.startBoard[self.currentY][self.currentX] == 0:	## If square editable
                if symbol == key._0 or symbol == key.NUM_0:				## If 0 pressed
                    self.playBoard[self.currentY][self.currentX] = 0	## Clear square
                    self.labelBoard[self.currentY][self.currentX].color = (0,0,255,255)
                    self.labelBoard[self.currentY][self.currentX].text = ''
                elif symbol == key._1 or symbol == key.NUM_1:			## If 1 pressed
                    self.playBoard[self.currentY][self.currentX] = 1	## Set label 1
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '1'
                elif symbol == key._2 or symbol == key.NUM_2:			## If 2 pressed
                    self.playBoard[self.currentY][self.currentX] = 2	## Set label 2
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '2'
                elif symbol == key._3 or symbol == key.NUM_3:			## If 3 pressed
                    self.playBoard[self.currentY][self.currentX] = 3	## Set label 3
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '3'
                elif symbol == key._4 or symbol == key.NUM_4:			## If 4 pressed
                    self.playBoard[self.currentY][self.currentX] = 4	## Set label 4
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '4'
                elif symbol == key._5 or symbol == key.NUM_5:			## If 5 pressed
                    self.playBoard[self.currentY][self.currentX] = 5	## Set label 5
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '5'
                elif symbol == key._6 or symbol == key.NUM_6:			## If 6 pressed
                    self.playBoard[self.currentY][self.currentX] = 6	## Set label 6
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '6'
                elif symbol == key._7 or symbol == key.NUM_7:			## If 7 pressed
                    self.playBoard[self.currentY][self.currentX] = 7	## Set label 7
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '7'
                elif symbol == key._8 or symbol == key.NUM_8:			## If 8 pressed
                    self.playBoard[self.currentY][self.currentX] = 8	## Set label 8
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '8'
                elif symbol == key._9 or symbol == key.NUM_9:			## If 9 pressed
                    self.playBoard[self.currentY][self.currentX] = 9	## Set label 9
                    self.labelBoard[self.currentY][self.currentX].color = (0, 0, 255, 255)
                    self.labelBoard[self.currentY][self.currentX].text = '9'

    def create_labels(self):
        self.labelBoard = []					## Clear label array
        for i in range(9):
            rowArray = []
            for j in range(9):
                if self.startBoard[i][j] == 0:						## If value is 0, set label blank with blue color
                    element = pyglet.text.Label('',
                                                font_name='Arial',
                                                font_size=30, color=(0, 0, 255, 255),
                                                x=66 * (j + 0.5), y=66 * (8.5 - i)+56,
                                                anchor_x='center', anchor_y='center')
                else:
                    element = pyglet.text.Label(str(self.playBoard[i][j]),				## Set label to value with black color
                                                font_name='Arial',
                                                font_size=30, color=(0, 0, 0, 255),
                                                x=66 * (j + 0.5), y=66 * (8.5 - i)+56,
                                                anchor_x='center', anchor_y='center')
                rowArray.append(element)
            self.labelBoard.append(rowArray)			## Create 2D list of labels

    def draw_labels(self):								## Draw all the labels in label list
        for row in self.labelBoard:
            for label in row:
                label.draw()

    def create_sprites(self):							## Create sprite array
        for i in range(9):
            rowSprites = []
            for j in range(9):
                boxType = self.selectedBox
                if self.startBoard[i][j] > 0:
                    boxType = self.fixedBox
                newSprite = pyglet.sprite.Sprite(boxType, j * 66, (8 - i) * 66+54)
                newSprite.visible = False
                rowSprites.append(newSprite)
            self.spriteArray.append(rowSprites)			## Create 2D list of invisible sprites

    def draw_sprites(self):								## Draw all sprites
        for row in self.spriteArray:
            for sprite in row:
                sprite.draw()

    def create_buttons(self):							## Create all button sprites
        self.checkButton = pyglet.sprite.Sprite(self.checkButtonImg, 29, 8)
        self.checkClicked = pyglet.sprite.Sprite(self.checkClickedImg, 29, 8)
        self.checkClicked.visible = False
        self.resetButton = pyglet.sprite.Sprite(self.resetButtonImg, 227, 8)
        self.resetClicked = pyglet.sprite.Sprite(self.resetClickedImg, 227, 8)
        self.resetClicked.visible = False
        self.backButton = pyglet.sprite.Sprite(self.backButtonImg, 425, 8)

    def draw_buttons(self):								## Draw all buttons
        self.checkButton.draw()
        self.checkClicked.draw()
        self.backButton.draw()
        self.resetButton.draw()
        self.resetClicked.draw()

    def check(self):									## Check if entered numbers are correct
        if self.playBoard == self.finalBoard:			## If player solution is equal to actual solution
            self.create_win()							## Show win screen
            self.win = True
        else:
            for i in range(9):							## Iterate through player solution
                for j in range(9):
                    if self.playBoard[i][j] > 0 and self.playBoard[i][j] != self.finalBoard[i][j]:
                        self.labelBoard[i][j].color = (255, 0, 0, 255)		## If any number different from actual solution, change color to red

    def reset_board(self):				## Reset board to initial puzzle state
        self.playBoard = deepcopy(self.startBoard)		## Setting user array equal to puzzle array
        for i in range(9):
            for j in range(9):
                if self.playBoard[i][j] == 0:
                    self.labelBoard[i][j].text = ''		## Set all editable labels blank

    def update(self, dt):		## Update screen
        self.on_draw()

    def create_menu_buttons(self):			## Create menu buttons
        self.easyButton = pyglet.sprite.Sprite(self.easyButtonImg, 227, 300)
        self.mediumButton = pyglet.sprite.Sprite(self.mediumButtonImg, 227, 250)
        self.hardButton = pyglet.sprite.Sprite(self.hardButtonImg, 227, 200)
        self.exitButton = pyglet.sprite.Sprite(self.exitButtonImg, 227, 150)

    def draw_menu_buttons(self):			## Draw menu buttons
        self.easyButton.draw()
        self.mediumButton.draw()
        self.hardButton.draw()
        self.exitButton.draw()

    def create_win(self):					## Create win screen
        self.winBackButton = pyglet.sprite.Sprite(self.backButtonImg, 227, 250)

    def draw_win(self):						## Draw win screen
        self.winBackButton.draw()
        self.winLabel.draw()

def main():
    mygame = mysudoku()				## Create instance of game
    pyglet.clock.schedule_interval(mygame.update, 1 / 60.)			## Set update interval
    pyglet.app.run()				## Run game

if __name__ == "__main__":
    main()							## Run script
