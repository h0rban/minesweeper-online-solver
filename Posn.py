class Posn:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return isinstance(other, Posn) and self.row == other.row and self.col == other.col

    def __str__(self):
        return f'Posn(row = {self.row}, col = {self.col})'

    def in_range(self, rows: int, cols: int) -> bool:
        return 0 <= self.col < cols and 0 <= self.row < rows

    def surrounding(self) -> list:
        x = self.col
        y = self.row
        posns = []
        for row in range(y - 1, (y + 1) + 1):
            for col in range(x - 1, (x + 1) + 1):
                if not (col == x and row == y):
                    posns.append(Posn(row, col))
        return posns

    def surrounding_in_range(self, rows: int, cols: int) -> list:
        return list(filter(lambda posn: posn.in_range(rows, cols), self.surrounding()))

    def coordinates(self) -> str:
        return f'({self.row}, {self.col})'
