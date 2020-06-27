
# MineSweeperOnlineSolver
Minesweeper Online Solver with Selenium and Python

### How to run
- Modify 'DRIVER_PATH' to match the location of your webdriver in Info.py. I am using chromium that from the link saved in Info.py as DRIVER_LINK
- Modify LOG_... strings in Info.py if you want to customize the log of actions taken by the solver
- Initialize Board object to your preference in Runner. Difficulties of 1, 2, and 3 correspond to the beginner, intermediate and expert modes respectively. Booleans log and mark_flags represent whether the solver will print log in the console and mark mines with flags on the web page.
- Stop the solver once the board is solved!

**Demo**

![MineSweeperOnline demo](https://raw.githubusercontent.com/h0rban/MineSweeperOnlineSolver/master/solver_example.gif)

### API
```pyhton
Board(difficulty=3, log=True, mark_flags=True).play()
```

### Todos
- Combining Python inheritance with mutation of the existing objects
- Account the relationship of number cells neighboring through the blank cell and improve probability
- Optimize computation by storing the results
- Selenium alert and error handling
- More tests

### Why
- Fun
- Competition with my girlfriend
- Prove that I can do better with code than manually
