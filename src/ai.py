from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

class SuperTicTacToeGameController(TwoPlayerGame):
  def __init__(self, players):
    self.players = players
    self.current_player = 1 
    self.active_boards = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    self.won_boards = [0] * 9
    self.super_board = [[0] * 9] * 9
  
  def show(self):
    print('\n'+'\n'.join([' '.join([['.', 'O', 'X'][self.super_board[3*j + i]] for i in range(3)]) for j in range(3)]))

  def possible_moves(self):
    return [move for moves in [[(i, a) for a, b in enumerate(self.super_board[i]) if b == 0] for i in self.active_boards] for move in moves]
  
  def make_move(self, move):
    self.super_board[move[0]][move[1]] = self.current_player
    self.current_board = int(move[1])
  
  def loss_condition(self):
    possible_combinations = [[1,2,3], [4,5,6], [7,8,9], [1,4,7], [2,5,8], [3,6,9], [1,5,9], [3,5,7]]
    return any([all([(self.super_board[i-1] == self.opponent_index) for i in combination]) for combination in possible_combinations]) 
  
  def is_over(self):
    return (self.possible_moves() == []) or self.loss_condition()
      
  def scoring(self):
    return -100 if self.loss_condition() else 0

#------------------------------------------------------------------------------------------------------------------
#   Program
#------------------------------------------------------------------------------------------------------------------
# Search algorithm of the AI player
algorithm = Negamax(8)

# Start the game
game = SuperTicTacToeGameController([AI_Player(algorithm), Human_Player()])
game.play()    
    
if game.loss_condition():
    print('\nPlayer', game.opponent_index, 'wins.')
else:
    print("\nIt's a draw.")