import Info
from Posn import Posn
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


# represents a cell on the MineSweeper board
class Cell:
    # global variable
    ATTRIBUTES = Info.REPS

    # constructor
    def __init__(self, row: int, col: int, driver: webdriver):
        self.bomb: bool = False
        self.blank: bool = True
        self.number: bool = False
        self.attribute: str = 'square blank'
        self.cell_integer: int = -1
        self.posn: Posn = Posn(row, col)
        self.neighbors: set = set()
        self.pointer: WebElement = driver.find_element_by_id(f'{row + 1}_{col + 1}')

    # returns a string representation of this Cell
    def __str__(self) -> str:
        return f'Cell(@{self.posn.coordinates()}, ...)'

    # returns hash code for this cell based on it's position
    def __hash__(self) -> int:
        x = self.posn.col
        y = self.posn.row
        return ((x + y) * (x + y + 1) // 2) + y

    # returns a list neighbors of this cell in the given range of the board
    def neighbors_posns(self, rows: int, cols: int) -> list:
        return self.posn.surrounding_in_range(rows, cols)

    # returns a set of blank neighbors
    def blank_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.blank, self.neighbors))

    # returns a set of bomb neighbors
    def bomb_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.bomb, self.neighbors))

    # returns a set of number neighbors
    def number_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.number, self.neighbors))

    # can we flag this cell's blank neighbors?
    def can_flag_neighbors(self):
        return len(self.blank_neighbors()) == self.get_number() - len(self.bomb_neighbors())

    # can we reveal this cell's blank neighbors?
    def can_reveal_neighbors(self):
        return self.get_number() == len(self.bomb_neighbors())

    # sets the neighbors of this cell (only once)
    def assign_neighbors(self, neighbors: set):
        if not len(self.neighbors) == 0:
            raise NotImplementedError
        else:
            self.neighbors = neighbors

    # clicks on the web element of this cell
    def click(self):
        if not self.blank:
            raise NotImplementedError
        else:
            try:
                self.pointer.click()
            except Exception as ex:
                raise ex

    # returns an integer of this cell on the board
    def get_number(self) -> int:
        if not self.number:
            raise NotImplementedError
        else:
            return self.cell_integer

    # converts this cell from blank to a number cell
    def to_number(self):
        num = self.ATTRIBUTES.get(self.attribute)
        if not isinstance(num, int):
            raise NotImplementedError
        else:
            self.number = True
            self.blank = False
            self.cell_integer = num

    # flags this cell as a bomb
    def flag(self):
        if not self.blank:
            raise NotImplementedError
        else:
            self.bomb = True
            self.blank = False

    # returns a string representing the type of the cell
    def field_string(self):
        if self.blank:
            return '_'
        elif self.bomb:
            return 'f'
        else:
            return self.cell_integer

    # resets this object to a blank cell
    def reset(self):
        self.attribute = 'square blank'
        self.bomb = False
        self.blank = True
        self.number = False

    # updates the attribute of this cell
    def update_attribute(self):
        try:
            self.attribute = self.pointer.get_attribute('class')
            return self.attribute
        except Exception as ex:
            raise ex

    # has this cell changed its attribute and was there an explosion?
    def update(self) -> tuple:
        if not self.blank:
            raise NotImplementedError
        else:
            current_attribute = self.attribute
            new_attribute = self.update_attribute()

            if current_attribute != new_attribute:
                self.attribute = new_attribute
                if new_attribute not in self.ATTRIBUTES.keys():
                    return False, True
                else:
                    self.to_number()
                    return True, False
            else:
                return False, False
