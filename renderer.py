import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from base import Board

REGION_COLORS = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
    "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
    "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
    "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080",
]


def region_color(region: int) -> str:
    return REGION_COLORS[region % len(REGION_COLORS)] if region != -1 else "white"


class BoardRenderer:
    '''Keeps a single figure open so the board can be re-rendered in place via update().'''

    def __init__(self, board: Board, show_queens: bool = True):
        self.show_queens = show_queens
        self.fig, self.ax = plt.subplots(figsize=(board.size, board.size))
        self.cells = []       # Rectangle patches, indexed [row][col]
        self.queen_texts = []
        self.size = None
        self.update(board, pause=None)

    def _build_grid(self, size: int):
        '''(Re)creates the cell patches. Only needed when the board size changes.'''
        self.ax.clear()
        self.cells = [[None] * size for _ in range(size)]
        for row in range(size):
            for col in range(size):
                rect = Rectangle((col, size - 1 - row), 1, 1,
                                 facecolor="white", edgecolor="black", linewidth=1.5)
                self.ax.add_patch(rect)
                self.cells[row][col] = rect

        self.ax.set_xlim(0, size)
        self.ax.set_ylim(0, size)
        self.ax.set_aspect("equal")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.queen_texts = []
        self.size = size

    def update(self, board: Board, queens: list | None = None, title: str | None = None,
               pause: float | None = 0.05):
        '''Re-renders with the given board. Pass `queens` to draw a different queen list
        than board.queens (e.g. the solver's working list). `pause` > 0 refreshes the window
        live; None skips the redraw (useful when you'll save/show afterwards).'''
        if board.size != self.size:
            self._build_grid(board.size)

        for row in range(board.size):
            for col in range(board.size):
                self.cells[row][col].set_facecolor(region_color(board.cells[row][col].region))

        for text in self.queen_texts:
            text.remove()
        self.queen_texts = []

        if self.show_queens:
            for queen in (board.queens if queens is None else queens):
                self.queen_texts.append(self.ax.text(
                    queen.col + 0.5, board.size - 1 - queen.row + 0.5, "♛",
                    ha="center", va="center", fontsize=24 * (8 / board.size), color="black"))

        if title is not None:
            self.ax.set_title(title)

        if pause is not None:
            self.fig.canvas.draw_idle()
            plt.pause(pause)

    def save(self, path: str):
        self.fig.savefig(path, bbox_inches="tight")

    def show(self):
        '''Blocks until the window is closed.'''
        plt.show()


def render_board(board: Board, show_queens: bool = True, save_path: str | None = None):
    '''Renders the board as a grid, colouring each cell by its region.'''
    renderer = BoardRenderer(board, show_queens)
    if save_path:
        renderer.save(save_path)
    else:
        renderer.show()
    return renderer.fig


if __name__ == "__main__":
    from puzzleGenerator import queen_setter, region_creator

    demo_board = Board(8)
    demo_board.queens = queen_setter(demo_board)
    region_creator(demo_board, demo_board.queens)
    render_board(demo_board)
