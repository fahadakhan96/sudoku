# sudoku

A simple sudoku game made in python using pyglet. The game uses pre-generated puzzles.

## How to run?
1. Install Python 2.7 if not already installed.
2. In cmd, type:
```cmd
python -m pip install pyglet
```
3. Run *guiSudoku.py*.

## Instructions
The game can be controlled using a keyboard and/or mouse. However, the buttons can only be accessed using a mouse.
When the user starts the program, a window opens with the menu shown. The user can then select the difficulty level of the puzzle ('Easy', 'Medium' or 'Hard') or he/she can close the program. Once the user selects a difficulty level, a puzzle is loaded from one of the .txt files and the game screen is shown. The puzzles used in the program were taken from [Sudoku Solver: Sudoku Solutions](http://www.sudoku-solutions.com/).

The puzzles are stored in the text files provided in /resources. You may add more puzzles to those files if you wish. In order to add a puzzle, just append the 9 rows in the text file (blank spaces in the puzzle are represented by "0").

## Controls:
- The user can navigate through the grid using either keyboard or mouse.
- The user can enter the numbers either through the keyboard or using the mouse (left-click increases the number by one, right-click decreases it by one).
- The user can click on the Check button at the bottom or press ENTER to check if his/her current solution is correct. The correctly entered numbers remain blue, whereas incorrect numbers turn red.
- The user can click on the Reset button at the bottom to remove all the entered numbers and return the puzzle to its original state.
- The user can click the Back button at the bottom to go back to the menu.
- Once the user gets the correct solution and clicks on Check or presses ENTER, a 'win screen' is shown that congratulates the user and has a Back button that, when clicked, takes the user back to the menu.
- The user may exit the program anytime by clicking on the 'X' on the top-right of the window.