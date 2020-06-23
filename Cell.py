import Info
from Posn import Posn
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


class Cell:
    attributes = Info.REPS

    def __init__(self, row: int, col: int, driver: webdriver):
        self.bomb: bool = False
        self.blank: bool = True
        self.number: bool = False
        self.neighbors: set = set()
        self.posn: Posn = Posn(row, col)
        self.attribute: str = 'square blank'
        self.pointer: WebElement = driver.find_element_by_id(f'{row + 1}_{col + 1}')

    def __str__(self) -> str:
        return f'Cell(posn = {self.posn.coordinates()}, ...)'

    def __hash__(self):
        x = self.posn.col
        y = self.posn.row
        return ((x + y) * (x + y + 1) // 2) + y

    def reset(self):
        self.attribute = 'square blank'
        self.bomb = False
        self.blank = True
        self.number = False

    def assign_neighbors(self, neighbors: set):
        if len(self.neighbors) == 0:
            self.neighbors = neighbors
        else:
            raise NotImplementedError

    def neighbors_posns(self, rows: int, cols: int) -> list:
        return self.posn.surrounding_in_range(rows, cols)

    def blank_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.blank, self.neighbors))

    def bomb_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.bomb, self.neighbors))

    def number_neighbors(self) -> set:
        return set(filter(lambda neighbor: neighbor.number, self.neighbors))

    def click(self):
        if self.blank:
            self.pointer.click()
        else:
            raise NotImplementedError

    def update(self) -> tuple:
        if not self.blank:
            raise NotImplementedError
        else:
            current_attribute = self.attribute
            try:
                new_attribute = self.pointer.get_attribute('class')
            except Exception:  # todo learn how to use ejections better
                raise Exception(f'error occurred when trying to retrieve the attribute for {self}')
            if current_attribute != new_attribute:
                self.attribute = new_attribute
                if new_attribute not in self.attributes.keys():
                    return False, True
                else:
                    self.to_number()
                    return True, False
            else:
                return False, False

    def to_number(self):
        if not isinstance(self.attributes.get(self.attribute), int):
            raise NotImplementedError
        else:
            self.number = True
            self.blank = False

    def get_number(self) -> int:
        if self.number:
            return self.attributes.get(self.attribute)
        else:
            raise NotImplementedError

    def flag(self):
        if not self.blank:
            raise NotImplementedError
        else:
            self.bomb = True
            self.blank = False
