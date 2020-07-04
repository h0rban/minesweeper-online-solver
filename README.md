# Mine Sweeper Online Solver
[Minesweeper Online](http://minesweeperonline.com/) Solver with Selenium and Python. Solver strategy is a generalized version of this [guide](http://www.minesweeper.info/wiki/Strategy)

### How to run
- Download a webdriver you prefer and place it in the cloned folder. In Board.py modify the driver object if you are not using Chrome and the second argument of its parameters to match the name of your preferred driver. I am using chromium that I downloaded from the link saved in Info.py as DRIVER_LINK.
- Modify strings starting with LOG_ in Info.py if you want to customize the log of actions taken by the solver.
- Initialize Board object to your preference in Runner. Difficulties of 1, 2, and 3 correspond to the beginner, intermediate and expert modes respectively. Booleans log and mark_flags represent whether the solver will print log in the console and mark mines with flags on the web page.
- Stop the solver once the board is solved!

**Demo**

<p align="center">
  <img src="https://raw.githubusercontent.com/h0rban/minesweeper-online-solver/master/solver_example.gif" alt="MineSweeperOnline demo" height="400"/>
</p>


### API
```pyhton
from Board import Board
Board(difficulty=3, log=True, mark_flags=True).play()
```
```pyhton
from Board import Board
Board().play()
```

### Todos
- Combining Python inheritance with mutation of the existing objects
- Account for the relationship of number cells neighboring through the blank cell and improve probability
- Optimize computation by storing the results
- Selenium alert and error handling
- More tests

### Why
- Fun
- Competition with my girlfriend
- Prove that I can do better with code than manually
