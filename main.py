from renderer import BoardRenderer
from puzzleGenerator import queen_setter, region_creator
from solver import calculate_loss, solve
from base import Board


demo_board = Board(8)
demo_board.queens = queen_setter(demo_board)
region_creator(demo_board, demo_board.queens)

# Clear board so solution isn't posted
demo_board.queens = []

solution = solve(demo_board)
# Now the board has 
renderer = BoardRenderer(demo_board)
renderer.update(demo_board, solution, "grah")
renderer.show()