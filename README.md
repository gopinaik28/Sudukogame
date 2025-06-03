**Sudoku Solver 🧩**
    This project implements a Sudoku puzzle solver using the classic backtracking algorithm in Python. The core logic resides in the sudoku.py file.

**🔍 Overview:**
    The solver fills a 9x9 Sudoku grid by recursively attempting to place digits 1 through 9 in empty cells, ensuring that each digit appears only once per row, column, and 3x3 subgrid. If a conflict arises, the algorithm backtracks and tries alternative numbers until the puzzle is solved.

**📁 File Structure**
sudoku.py – Contains the main implementation of the backtracking algorithm.
README.md – Project documentation.

**🚀 Getting Started**
**Prerequisites**
Python 3.x

**Installation**
1)Clone the repository:
  1)git clone https://github.com/Sai-Nihal-Pampara/Sudoku-Game.git
  2)cd Sudoku-Game
2)Run the solver:
  1)python sudoku.py

**🧠 How It Works**
The backtracking algorithm operates as follows:
1)Find an empty cell in the grid.
2)Attempt to place digits 1 through 9 in the empty cell.
3)Check for validity:
  1)The digit is not present in the current row.
  2)The digit is not present in the current column.
  3)The digit is not present in the current 3x3 subgrid.
4)Place the digit if it passes all checks.
5)Recursively attempt to fill the rest of the grid.
6)Backtrack if no valid digit can be placed, and try the next possible digit.
7)This process continues until the grid is completely filled with valid digits.

**🛠️ Features**
1)Solves any valid 9x9 Sudoku puzzle.
2)Utilizes a recursive backtracking approach.



📸 Example
Given the following Sudoku puzzle:
grid = 
![Screenshot (20)](https://github.com/user-attachments/assets/33ce9705-267a-4e21-8c90-1dd9d89a0040)

The solver will output the completed puzzle:
![Screenshot (23)](https://github.com/user-attachments/assets/264bed3a-b9b1-4652-8727-7ffa4970560b)


Thank You!

