# represents a position on the MineSweeper board
class Posn:

    # constructor
    def __init__(self, row: int, col: int) -> None:
        self.row: int = row
        self.col: int = col

    # returns the string representation of the Posn
    def __str__(self) -> str:
        return f'Posn(row = {self.row}, col = {self.col})'

    # returns a string representation of Cartesian coordinates
    def coordinates(self) -> str:
        return f'({self.col + 1}, {self.row + 1})'

    # is the given object a Posn and has the same coordinates?
    def __eq__(self, other) -> bool:
        return isinstance(other, Posn) and self.row == other.row and self.col == other.col

    # is this posn in the given range of rows and columns?
    def in_range(self, rows: int, cols: int) -> bool:
        return 0 <= self.col < cols and 0 <= self.row < rows

    # returns eight surrounding positions excluding this Posn
    def surrounding(self) -> list:
        x: int = self.col
        y: int = self.row
        posns: list = []
        for row in range(y - 1, (y + 1) + 1):
            for col in range(x - 1, (x + 1) + 1):
                if not (col == x and row == y):
                    posns.append(Posn(row, col))
        return posns

    # returns the list of surrounding positions in the given range of rows and columns
    def surrounding_in_range(self, rows: int, cols: int) -> list:
        return list(filter(lambda posn: posn.in_range(rows, cols), self.surrounding()))
