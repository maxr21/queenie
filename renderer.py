import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from base import Board

REGION_COLORS = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
    "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
    "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
    "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080",
]

def render_board(board: Board, show_queens: bool = True, save_path: str | None = None):
    '''Renders the board as a grid, colouring each cell by its region.'''
    fig, ax = plt.subplots(figsize=(board.size, board.size))

    for row in range(board.size):
        for col in range(board.size):
            cell = board.cells[row][col]
            color = REGION_COLORS[cell.region % len(REGION_COLORS)] if cell.region != -1 else "white"
            ax.add_patch(Rectangle((col, board.size - 1 - row), 1, 1,
                                    facecolor=color, edgecolor="black", linewidth=1.5))

    if show_queens:
        for queen in board.queens:
            ax.text(queen["col"] + 0.5, board.size - 1 - queen["row"] + 0.5, "♛",
                    ha="center", va="center", fontsize=24 * (8 / board.size), color="black")

    ax.set_xlim(0, board.size)
    ax.set_ylim(0, board.size)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    if save_path:
        fig.savefig(save_path, bbox_inches="tight")
    else:
        plt.show()

    return fig


if __name__ == "__main__":
    from puzzleGenerator import queen_setter, region_creator

    demo_board = Board(8)
    demo_board.queens = queen_setter(demo_board)
    region_creator(demo_board, demo_board.queens)
    render_board(demo_board)
