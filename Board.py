import time
import Info
import random
from Cell import Cell
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


# represents a MineSweeper Board 
class Board:

    # constructor
    def __init__(self, difficulty: int):

        if not 1 <= difficulty <= 3:
            raise NotImplementedError

        start_time = time.time()

        # define dimensions
        rows, cols, mines, link = Info.DIFFICULTIES[difficulty - 1]
        driver = webdriver.Chrome(Info.DRIVER_PATH)
        driver.get(link)

        # assign fields
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

        # initialize fields and cells todo is this a good idea to call this here
        self.init_fields_and_cells()

        print(f'{round(time.time() - start_time, 3)} seconds to initialize a board with {self.rows * self.cols} cells')

    # returns a string representation of the state of this board
    def __str__(self):
        out = f'Board(rows = {self.rows},\n' \
              + f'\tcols = {self.cols}\n' \
              + f'\tblank.size = {len(self.blank)}\n' \
              + f'\tbombs.size = {len(self.bombs)}\n' \
              + f'\tnumbers.size = {len(self.numbers)}\n' \
              + f'\tworklist.size = {len(self.workset)}\n' \
              + f'\tMatrix as String:\n'
        field = ''
        for row in self.matrix:
            field += '\t\t'
            for cell in row:
                field += cell.field_string() + ' '
            field += '\n'
        return out + field

    # initialize the board's matrix, blank set with cells
    def init_fields_and_cells(self):
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

    # reveals a random cell from the blank set
    def reveal_random(self):
        cell = random.sample(self.blank, 1)[0]
        cell.click()
        self.update_from({cell})

    # updates the cells from a set of cells
    def update_from(self, workset: set):
        start_time = time.time()
        counter = 0
        visited = set()
        while not len(workset) == 0:
            popped = workset.pop()
            if popped not in visited:
                visited.add(popped)
                updated, boom = popped.update()
                if boom:
                    # print('RESETTING GAME')
                    self.reset_game()
                    return
                elif updated:
                    workset |= popped.blank_neighbors()
                    self.blank.discard(popped)
                    self.numbers.add(popped)
                    if not popped.get_number() == 0:
                        self.workset.add(popped)
                    counter += 1
        print(f'{round(time.time() - start_time, 3)} seconds to update {counter} cells')

    # resets the board's sets and cells
    def reset_game(self):

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

    # returns a set of cells to flag
    def get_cells_to_flag(self) -> set:
        to_flag = set()
        for cell in self.workset:
            if cell.can_flag_neighbors():
                to_flag |= cell.blank_neighbors()
        return to_flag

    # flags all cells in the given set
    def flag_all(self, to_flag: set):
        for cell in to_flag:
            cell.flag()
            self.blank.discard(cell)

    # returns a set of cells to reveal
    def get_cells_to_reveal(self) -> set:
        to_reveal = set()
        for cell in self.workset:
            if cell.can_reveal_neighbors():
                to_reveal |= cell.blank_neighbors()
        return to_reveal

    # reveals all cells in the given set
    def reveal_all(self, to_reveal: set):
        to_update = set()
        for cell in to_reveal:
            cell.click()
            to_update.add(cell)
        self.update_from(to_update)

    # main game loop todo consider moving to runner
    def play(self):
        self.reveal_random()
        while not len(self.bombs) == self.mines:
            to_flag = self.get_cells_to_flag()
            to_reveal = self.get_cells_to_reveal()
            if len(to_flag) > 0 or len(to_reveal) > 0:
                self.flag_all(to_flag)
                self.reveal_all(to_reveal)
                # todo else if find set difference to add to the sets
            else:
                # todo find with lowest probability if it comes to this
                print("REVEALING RANDOM")
                self.reveal_random()
