class Queen:
    '''Queens have positions and regions.'''
    
    def __init__(self, row: int, col: int, region: int):
        self.row = row
        self.col = col
        self.region = region

class Cell:
    '''Cells have rows, columns and regions'''
    def __init__(self, region: int, row: int, col: int):
        if row is None or col is None:
            raise ValueError(f"row and col both required, values given: r: {row}, c: {col}")
        
        self.region = region
        self.row = row
        self.col = col
        
    def __str__(self):
        return f"region: {self.region}, row: {self.row}, col: {self.col}"
    
    def __repr__(self):
        return self.__str__()

# num queens <= board.size
# Fast look up 

class Board:
    '''Board class represent a queens board.
    The board can have queens on it and is made up of cells'''
    def __init__(self, size: int):
        self.size = size
        self.cells = []
        self.queens = []
        self._build_board()
        
    def _build_board(self):
        for row in range(self.size):
            self.cells.append([])
            for col in range(self.size):
                self.cells[row].append(Cell(-1, row, col))
        
    def __str__(self):
        s = ""
        for cell in self.cells:
            s.join(f"{cell.__str__()}, ")
    
    def __repr__(self):
        return self.__str__()