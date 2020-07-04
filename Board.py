import os
import time
import Info
import random
from Cell import Cell
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


# returns one random element from the given set
def get_one_random(s: set):
    return random.sample(s, 1)[0]


# represents a MineSweeper Board
class Board:
    # global dictionary of actions for logging purposes
    ACTIONS: dict = {'flag': Info.LOG_FLAG,
                     'reveal': Info.LOG_REVEAL,
                     'random': Info.LOG_REVEAL_RANDOM,
                     'reset': Info.LOG_GAME_RESET,
                     'complete': Info.LOG_GAME_COMPLETE}

    # constructor
    def __init__(self, difficulty: int = 3, log: bool = True, mark_flags: bool = False) -> None:

        start_t = time.time()

        if not 1 <= difficulty <= 3:
            raise Exception('Difficulty should be in range [1, 3]')

        # define dimensions
        rows, cols, mines, link = Info.DIFFICULTIES[difficulty - 1]
        driver: webdriver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
        driver.get(link)

        # assign fields
        self.log: bool = log
        self.mark_flags: bool = mark_flags
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
        self.log_action(f'\t{round(time.time() - start_t, 3)} seconds to initialize '
                        + f'a board with {self.rows * self.cols} cells')

    # main game loop
    def play(self) -> None:
        while not len(self.blank) == 0:
            to_flag: set = self.get_cells_to_flag()
            if not len(to_flag) == 0:
                self.log_action('flag')
                self.flag_all(to_flag)
            else:
                to_reveal: set = self.get_cells_to_reveal()
                if not len(to_reveal) == 0:
                    self.log_action('reveal')
                    self.reveal_all(to_reveal)
                else:
                    self.log_action('random')
                    self.reveal_random()

        # todo remove later
        while True:
            x = 1

    # resets the board's sets and cells
    def reset_game(self) -> None:
        self.log_action('reset')
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
        no_numbers: set = set(filter(lambda c: len(c.non_zero_number_neighbors()) == 0, self.blank))
        # account for the case when set has length zero and yields a zero probability
        if len(no_numbers) == 0:
            lowest_prob: float = 1
            random_cell: Cell = get_one_random(self.blank)
        else:
            # todo find a way to subtract the number of bombs accounted for in the workset
            lowest_prob: float = (self.mines - len(self.bombs)) / len(no_numbers)
            random_cell: Cell = get_one_random(no_numbers)
        for cell in self.workset:
            blank: set = cell.blank_neighbors()
            if not len(blank) == 0:
                prob: float = cell.bombs_remaining() / len(blank)
                if prob < lowest_prob:
                    lowest_prob = prob
                    random_cell = get_one_random(blank)
        random_cell.click()
        self.update_from({random_cell})

    # initialize the board's matrix, blank set with cells
    def init_fields_and_cells(self) -> None:
        # initialize matrix and blank set
        for row in range(self.rows):
            row_to_add: list = []
            for col in range(self.cols):
                cell: Cell = Cell(row, col, self.driver)
                row_to_add.append(cell)
                self.blank.add(cell)
            self.matrix.append(row_to_add)
        # for each cell assigns the neighbors in range
        for row in self.matrix:
            for cell in row:
                cell.assign_neighbors(
                    # returns a set of cells at the given posns
                    set([self.matrix[posn.row][posn.col] for posn in cell.neighbors_posns(self.rows, self.cols)]))

    # if log is turned on returns the print out associated with the given action
    def log_action(self, action: str) -> None:
        if self.log:
            print(self.ACTIONS.get(action, action))

    # flags all cells in the given set
    def flag_all(self, to_flag: set) -> None:
        for cell in to_flag:
            cell.flag(self.mark_flags)
            self.blank.discard(cell)
            self.bombs.add(cell)

    # updates the cells from a set of cells
    def update_from(self, workset: set) -> None:
        start_time = time.time()
        counter: int = 0
        visited: set = set()
        while not len(workset) == 0:
            popped: Cell = workset.pop()
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
        self.log_action(f'\t{round(time.time() - start_time, 3)} seconds to update {counter} cells')

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
            self.log_action('complete')
        else:
            to_update: set = set()
            for cell in to_reveal:
                cell.click()
                to_update.add(cell)
            self.update_from(to_update)

    # returns a set of cells to flag
    def get_cells_to_flag(self) -> set:
        to_flag: set = set()
        for cell in self.workset:
            to_flag |= cell.get_neighbors_to_flag()
        return to_flag

    # returns a set of cells to reveal
    def get_cells_to_reveal(self) -> set:
        to_reveal: set = set()
        to_discard: set = set()
        for cell in self.workset:
            exhausted, neighbors = cell.get_neighbors_to_reveal()
            if exhausted:
                to_discard.add(cell)
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

        out: str = f'Board(rows = {self.rows},\n' \
                   + f'\tcols = {self.cols}\n' \
                   + f'\tmines = {self.mines}\n' \
                   + f'\tblank.size = {len(self.blank)}\n' \
                   + f'\tbombs.size = {len(self.bombs)}\n' \
                   + f'\tnumbers.size = {len(self.numbers)}\n' \
                   + f'\tworkset.size = {len(self.workset)}\n' \
                   + f'\tMatrix as String:\n'
        field: str = ''
        for row in self.matrix:
            field += '\t\t'
            for cell in row:
                field += cell.field_string() + ' '
            field += '\n'
        return out + field
