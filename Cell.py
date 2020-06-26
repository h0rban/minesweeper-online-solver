import Info
from Posn import Posn
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement


# represents a cell on the MineSweeper board
class Cell:
    # global variable
    ATTRIBUTES = Info.REPS

    # constructor
    def __init__(self, row: int, col: int, driver: webdriver) -> None:
        self.bomb: bool = False
        self.blank: bool = True
        self.number: bool = False
        self.attribute: str = 'square blank'
        self.cell_integer: int = -1
        self.posn: Posn = Posn(row, col)
        self.neighbors: set = set()
        self.driver: webdriver = driver
        self.pointer: WebElement = driver.find_element_by_id(f'{row + 1}_{col + 1}')

    # sets the neighbors of this cell (only once)
    def assign_neighbors(self, neighbors: set) -> None:
        if not len(self.neighbors) == 0:
            raise NotImplementedError
        else:
            self.neighbors = neighbors

    # converts this cell from blank to a number cell
    def to_number(self) -> None:
        num = self.ATTRIBUTES.get(self.attribute)
        if not isinstance(num, int):
            raise NotImplementedError
        else:
            self.number = True
            self.blank = False
            self.cell_integer = num

    # resets this object to a blank cell
    def reset(self) -> None:
        self.bomb = False
        self.blank = True
        self.number = False
        self.attribute = 'square blank'

    # clicks on the web element of this cell
    def click(self) -> None:
        if not self.blank:
            raise NotImplementedError
        else:
            try:
                self.pointer.click()
            except Exception as ex:
                raise ex

    # flags this cell as a bomb
    def flag(self, mark_flags: bool) -> None:
        if not self.blank:
            raise NotImplementedError
        else:
            self.bomb = True
            self.blank = False
            if mark_flags:
                ActionChains(self.driver).context_click(self.pointer).perform()

    # returns a string representation of this Cell
    def __str__(self) -> str:
        return f'Cell{self.field_string()}@{self.posn.coordinates()}'

    # returns a string representing the type of the cell
    def field_string(self) -> str:
        if self.blank:
            return '▢'
        elif self.bomb:
            return '⚐'
        else:
            return str(self.cell_integer)

    # updates the attribute of this cell
    def update_attribute(self) -> str:
        try:
            self.attribute = self.pointer.get_attribute('class')
            return self.attribute
        except Exception as ex:
            raise ex

    # returns hash code for this cell based on it's position
    def __hash__(self) -> int:
        x: int = self.posn.col
        y: int = self.posn.row
        return ((x + y) * (x + y + 1) // 2) + y

    # returns an integer of this cell on the board
    def get_number(self) -> int:
        if not self.number:
            raise NotImplementedError
        else:
            return self.cell_integer

    # returns the number of bombs to be found remaining that are neighbors of this cell
    def bombs_remaining(self) -> int:
        return self.cell_integer - len(self.bomb_neighbors())

    # returns a set of bomb neighbors
    def bomb_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.bomb, self.neighbors))

    # returns a set of blank neighbors
    def blank_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.blank, self.neighbors))

    # returns a set of blank neighbors to flag based on a more complex logic
    def get_more_to_flag(self) -> set:
        pattern_flag: set = set()
        for neighbor in self.non_zero_number_neighbors():
            dif: set = neighbor.blank_neighbors().difference(self.blank_neighbors())
            if len(dif) == neighbor.bombs_remaining() - self.bombs_remaining():
                pattern_flag |= dif
        return pattern_flag

    # returns a set of blank neighbors if we can flag them and an empty set otherwise
    def get_neighbors_to_flag(self) -> set:
        this_blank: set = self.blank_neighbors()
        return this_blank if len(this_blank) == self.bombs_remaining() else self.get_more_to_flag()

    # returns a set of number neighbors whose number is greater than 0
    def non_zero_number_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.number and neighbor.get_number() > 0, self.neighbors))

    # has this cell changed its attribute and was there an explosion?
    def update(self) -> tuple:
        if not self.blank:
            raise NotImplementedError
        else:
            current_attribute: str = self.attribute
            new_attribute: str = self.update_attribute()
            if current_attribute != new_attribute:
                self.attribute = new_attribute
                if new_attribute not in self.ATTRIBUTES.keys():
                    return False, True
                else:
                    self.to_number()
                    return True, False
            else:
                return False, False

    # returns a set of blank neighbors if we can reveal them and an empty set otherwise
    def get_neighbors_to_reveal(self) -> tuple:
        if self.get_number() == len(self.bomb_neighbors()):
            return True, self.blank_neighbors()
        else:
            return False, self.get_more_to_reveal()

    # returns a set of blank neighbors to reveal based on a more complex logic
    def get_more_to_reveal(self) -> set:
        this_blank: set = self.blank_neighbors()
        pattern_reveal: set = set()
        for neighbor in self.non_zero_number_neighbors():
            other_blank: set = neighbor.blank_neighbors()
            is_sub_set: bool = len(this_blank) > 0 and this_blank.issubset(other_blank)
            eq_remaining: bool = self.bombs_remaining() == neighbor.bombs_remaining()
            dif: set = other_blank.difference(this_blank)
            dif_over_zero: bool = len(dif) > 0
            if is_sub_set and eq_remaining and dif_over_zero:
                pattern_reveal |= dif
        return pattern_reveal

    # returns whether this cell's integer is greater than one and it has blank neighbors
    def should_add_to_workset(self) -> bool:
        if not self.number:
            raise NotImplementedError
        else:
            return self.cell_integer > 0 and len(self.blank_neighbors()) > 0

    # returns a list neighbors of this cell in the given range of the board
    def neighbors_posns(self, rows: int, cols: int) -> list:
        return self.posn.surrounding_in_range(rows, cols)
