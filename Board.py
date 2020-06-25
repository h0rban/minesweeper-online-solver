import time
import Info
import random
from Cell import Cell
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


# represents a MineSweeper Board
class Board:

    # constructor
    def __init__(self, difficulty: int, log: bool) -> None:

        start_t = time.time()

        if not 1 <= difficulty <= 3:
            raise Exception('Difficulty should be in range [1, 3]')

        # define dimensions
        rows, cols, mines, link = Info.DIFFICULTIES[difficulty - 1]
        driver = webdriver.Chrome(Info.DRIVER_PATH)
        driver.get(link)

        # assign fields
        self.log: bool = log
        self.rows: int = rows
        self.cols: int = cols
        self.mines: int = mines
        self.blank: set = set()
        self.bombs: set = set()
        self.numbers: set = set()
        self.workset: set = set()
        self.matrix: list = list()
        self.driver: webdriver = driver
        self.face: WebElement = driver.find_element_by_id('face')

        # initialize fields and cells todo is this a good idea to call this here?
        self.init_fields_and_cells()

        if log:
            print(f'{round(time.time() - start_t, 3)} seconds to initialize a board with {self.rows * self.cols} cells')

    # main game loop
    def play(self) -> None:

        # todo add a check method that asserts that sets are of certain
        #  length, that each cell has no bombs that its integer
        #  assert that the field parameters changed by this much

        while not len(self.blank) == 0:
            to_flag = self.get_cells_to_flag()
            to_reveal = self.get_cells_to_reveal()
            if len(to_flag) == 0 and len(to_reveal) == 0:
                if self.log:
                    print("REVEALING RANDOM")
                self.reveal_random()
            else:
                self.flag_all(to_flag)
                self.reveal_all(to_reveal)

        while True:
            # todo check for alert
            print('Not Implemented')

    # resets the board's sets and cells
    def reset_game(self) -> None:

        if self.log:
            print(Info.LOG_GAME_RESET)

        # click face to restart the game
        self.face.click()
        # clear sets
        self.blank.clear()
        self.bombs.clear()
        self.numbers.clear()
        self.workset.clear()
        # reset every cell in the matrix
        for row in self.matrix:
            for cell in row:
                cell.reset()
                self.blank.add(cell)

    # reveals a random cell from the blank set
    def reveal_random(self) -> None:
        # todo pick one with least probability, among blank
        #  neighbors of numbers and the rest of the field / num bombs
        cell = random.sample(self.blank, 1)[0]
        cell.click()
        self.update_from({cell})

    # initialize the board's matrix, blank set with cells
    def init_fields_and_cells(self) -> None:
        # initialize matrix and blank set
        for row in range(self.rows):
            row_to_add = []
            for col in range(self.cols):
                cell = Cell(row, col, self.driver)
                row_to_add.append(cell)
                self.blank.add(cell)
            self.matrix.append(row_to_add)
        # for each cell assigns the neighbors in range
        for row in self.matrix:
            for cell in row:
                cell.assign_neighbors(
                    # returns a set of cells at the given posns
                    set([self.matrix[posn.row][posn.col] for posn in cell.neighbors_posns(self.rows, self.cols)]))

    # flags all cells in the given set
    def flag_all(self, to_flag: set) -> None:
        for cell in to_flag:
            cell.flag()
            self.blank.discard(cell)
            self.bombs.add(cell)

    # updates the cells from a set of cells
    def update_from(self, workset: set) -> None:
        start_time = time.time()
        counter = 0
        visited = set()
        while not len(workset) == 0:
            popped = workset.pop()
            if popped not in visited:
                visited.add(popped)
                updated, boom = popped.update()
                if boom:
                    self.reset_game()
                    return
                elif updated:
                    workset |= popped.blank_neighbors()
                    self.blank.discard(popped)
                    self.numbers.add(popped)
                    if popped.should_add_to_workset():
                        self.workset.add(popped)
                    counter += 1
        if self.log:
            print(f'{round(time.time() - start_time, 3)} seconds to update {counter} cells')

    # reveals all cells in the given set
    def reveal_all(self, to_reveal: set) -> None:

        if len(to_reveal) == len(self.blank):
            for cell in to_reveal:
                # todo the only issue here is if one cell is pressed and it reveals
                #  the rest, then the alert is raised and we get an error, might want
                #  to check in click if alert is present
                cell.click()
                self.blank.discard(cell)
                self.numbers.add(cell)
            print('THE GAME SHOULD BE COMPLETE')
        else:
            to_update = set()
            for cell in to_reveal:
                cell.click()
                to_update.add(cell)
            self.update_from(to_update)

    # returns a set of cells to flag
    def get_cells_to_flag(self) -> set:
        to_flag = set()
        for cell in self.workset:
            to_flag |= cell.get_neighbors_to_flag()
        return to_flag

    # returns a set of cells to reveal
    def get_cells_to_reveal(self) -> set:
        to_reveal = set()
        to_discard = set()
        for cell in self.workset:
            cell_exhausted, neighbors = cell.get_neighbors_to_reveal()
            if cell_exhausted:
                to_discard.add(cell)
            # this has to be outside of if because can have cells to reveal without being exhausted
            to_reveal |= neighbors
        # discards the exhausted cells from the workset
        self.workset = self.workset.difference(to_discard)
        return to_reveal

    # returns a string representation of the state of this board
    def __str__(self) -> str:

        # blank = len(self.blank)
        # bombs = len(self.bombs)
        # numbers = len(self.numbers)
        # workset = len(self.workset)
        # total = blank + bombs + numbers
        # return f'{blank}\t{bombs}\t{numbers}\t{total}\t\t{workset}'

        out = f'Board(rows = {self.rows},\n' \
              + f'\tcols = {self.cols}\n' \
              + f'\tmines = {self.mines}\n' \
              + f'\tblank.size = {len(self.blank)}\n' \
              + f'\tbombs.size = {len(self.bombs)}\n' \
              + f'\tnumbers.size = {len(self.numbers)}\n' \
              + f'\tworkset.size = {len(self.workset)}\n' \
              + f'\tMatrix as String:\n'
        field = ''
        for row in self.matrix:
            field += '\t\t'
            for cell in row:
                field += cell.field_string() + ' '
            field += '\n'
        return out + field
