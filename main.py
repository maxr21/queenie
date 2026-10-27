from renderer import BoardRenderer
from puzzleGenerator import queen_setter, region_creator
from solver import solve
from base import Board


demo_board = Board(8)
demo_board.queens = queen_setter(demo_board)
region_creator(demo_board, demo_board.queens)

# Clear board so solution isn't posted
demo_board.queens = []
renderer = BoardRenderer(demo_board)
solution = solve(demo_board, renderer)
# Now the board has 

renderer.update(demo_board, solution, "DONE!")
renderer.show()