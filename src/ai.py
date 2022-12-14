from easyAI import TwoPlayerGame

class SuperTicTacToeGameController(TwoPlayerGame):
  def __init__(self, players):
    self.players = players
    self.current_player = 1 
    self.active_boards = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    self.won_boards = [0] * 9
    self.super_board = [[0]*9 for _ in range(9)]

  def possible_moves(self):
    return [move for moves in [[(i, a) for a, b in enumerate(self.super_board[i]) if b == 0] for i in self.active_boards] for move in moves]
  
  def make_move(self, move):
    self.super_board[move[0]][move[1]] = self.current_player
    self.active_boards = [move[1]]

    if self.is_won(move[0]):
      self.won_boards[move[0]] = self.current_player
    if self.is_won(move[1]) or self.is_tied(move[1]):
      self.active_boards = [index for index, board in enumerate(self.won_boards) if board == 0]

  def is_won(self, board):
    possible_combinations = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    return any([all([(self.super_board[board][i] == 1) for i in combination]) or all([(self.super_board[board][i] == 2) for i in combination]) for combination in possible_combinations])

  def is_tied(self, board):
    return all([self.super_board[board][i] != 0 for i in range(9)])
    
  def loss_condition(self):
    possible_combinations = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    return any([all([(self.won_boards[i] == self.opponent_index) for i in combination]) for combination in possible_combinations]) 
  
  def is_over(self):
    return (self.possible_moves() == []) or self.loss_condition()
      
  def scoring(self):
    return -100 if self.loss_condition() else 0

  def boardsWon(self, player):
    return sum([(board == player) for board in self.won_boards])