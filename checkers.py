"""
-Иногда фигуры противника не ходят
"""

def copy(matrix):
	"""Make copy of matrix"""

	return [row[:] for row in matrix]

def sign(x):
	"""Check's sign of x"""

	return x and (1,-1)[x < 0]

class Game:
	def __init__(self):
		self.board = [[0 for _ in range(8)] for _ in range(8)]

		self.depth = 1
		self.up_moves = [(-1, 1), (-1, -1)]
		self.down_moves = [(1, 1), (1, -1)] 
		self.two_moves = [(2, 2), (2, -2), (-2, 2), (-2, -2)]

		self.current_player = ("w", "W")
		self.player = ('w', 'W')
		self.ai = ('b', 'B')
		self.last = None, None

	def setPlayer(self, isBlack):
		self.player = ('b', 'B') if isBlack else ('w', 'W')
		self.ai = ('w', 'W') if isBlack else ('b', 'B')

	def setAiDepth(self, depth):
		self.depth = depth

	def start(self):
		"""(Re)start game with button"""
		self.cnt = 0
		self.last = None, None
		self.current_player = ("w", "W")
		self.board = [[0 for _ in range(8)] for _ in range(8)]

		#Place figures on board
		for i in range(8):
			for j in range(8):
				if (i + j) % 2 == 1:
					if i < 3:
						self.board[i][j] = self.ai[0]
					elif i > 4:
						self.board[i][j] = self.player[0]

		#First move for white in case of playing black
		if self.player == ("b", "B"):
			self.aiMove()
			
	def endMove(self):
		"""Changes current player and clear last move"""

		self.last = None, None
		self.current_player = ("w", "W") if self.current_player == ("b", "B") else ("b", "B")

	def aiMove(self):
		""" Starts minimax algoritm and coose best move for AI """

		best_move = self.minimaxRoot(self.board, self.depth, self.ai)
		self.setBoard(best_move)
		self.endMove()

		print("I count", self.cnt, "moves")
		self.cnt = 0

	def minimaxRoot(self, board, depth, player):
		""" Function to start minimax for AI, return's bestBoard not bestValue """

		all_moves = self.getChildrens(board, player)
		best_move = 1e500
		bestMoveFound = None

		enemy = ("b", "B") if player == ("w", "W") else ("w", "W")
		for move in all_moves:
			value = self.minimax(-1e500, 1e500, move, depth-1, enemy)
			if value < best_move:
				best_move = value 
				bestMoveFound = move

		return bestMoveFound

	def minimax(self, alpha, beta, board, depth, player):
		""" Universl minimax for both player, return value of bestBoard"""
		self.cnt += 1
		if depth == 0:
			best_move = self.countHeuristic(board)
			return best_move

		sign = -1 
		all_moves = self.getChildrens(board, player)
		
		if all_moves:
			for move in all_moves:
				if player == self.player:
					best_move = -1e500 

					value = self.minimax(alpha, beta, move, depth-1, self.ai)
					best_move = max(best_move, value)
					alpha = max(alpha, best_move)
					
					if beta <= alpha:
						return best_move
		
				elif player == self.ai:
					best_move = 1e500 
					
					value = self.minimax(alpha, beta, move, depth-1, self.player)
					best_move = min(best_move, value)
					beta = min(beta, best_move)

					if beta <= alpha:
						return best_move

			return best_move
		else:
			print("Player {} is out of turns".format(player))
			return 1e500 if player == self.ai else -1e500

	def setBoard(self, board):
		"""Set current board to board"""

		self.board[:] = board[:]

	def makeMove(self, i, j, n_i, n_j):
		""" Moves playe from (i,j) to (n_i, n_j) """

		board = self.board
		legal_kills = self.getKills(board, i, j)
		
		if legal_kills:
			for move in legal_kills:
				if board[n_i][n_j] == 0 and move[i][j] == 0\
				and move[n_i][n_j] in self.player:
					self.setBoard(move)

					if self.getKills(board, n_i, n_j):
						return

					self.endMove()
					self.aiMove()
					return
		
		legal_moves = self.getMoves(board, i, j) 
		if legal_moves:
			for move in legal_moves:
				if board[n_i][n_j] == 0 and move[i][j] == 0\
				and move[n_i][n_j] in self.player:
					self.setBoard(move)
					self.endMove()
					self.aiMove()
					return
		return
			
	def countHeuristic(self, board):
		"""Big value if human player is winning"""
		
		totalScore = 0
		
		cnt = {"w": 0, "W": 0, "b": 0, "B": 0}

		for i in range(8):
			for j in range(8):
				if board[i][j] != 0:
					cnt[board[i][j]] += 1

		if (cnt[self.player[0]] + cnt[self.player[1]]) == 0:
			totalScore = -1e500
		elif (cnt[self.ai[0]] + cnt[self.ai[1]]) == 0:
			totalScore = 1e500
		else:
			totalScore += cnt[self.player[0]]*10 + cnt[self.player[1]]*50
			totalScore -= cnt[self.ai[0]]*15 + cnt[self.ai[1]]*55

		return totalScore

	def getChildrens(self, board, current_player):
		"""Get sorted possible boards from this position for current player"""
		
		all_kills = []
		for i in range(8):
			for j in range(8):
				if board[i][j] in current_player:
					kills = self.getKills(board, i, j)
					if kills:
						all_kills += kills

		if all_kills:
			return all_kills

		all_moves = []
		for i in range(8):
			for j in range(8):
				if board[i][j] in current_player:
					moves = self.getMoves(board, i, j)
					if moves:
						all_moves += moves 
		
		if all_moves:
			return all_moves

	def getMoves(self, board, i, j):
		"""Get all boards with (i,j)`s figure moves"""
		moves = []
		all_moves = None

		if board[i][j] == self.player[0]:
			all_moves = self.up_moves
		elif board[i][j] == self.ai[0]:
			all_moves = self.down_moves
		else:
			all_moves = self.up_moves + self.down_moves

		for d_i, d_j in all_moves:
			for mul in range(1, 8):
				if board[i][j] in ("w", "b") and mul != 1:
					break

				n_i, n_j = i + mul * d_i, j + mul * d_j 

				if self.isOnBoard(n_i, n_j):
					if board[n_i][n_j] == 0:
						new_board = copy(board)
						
						new_board[i][j], new_board[n_i][n_j] = new_board[n_i][n_j], new_board[i][j]
						
						if n_i == 0 and new_board[n_i][n_j] == self.player[0]:
							new_board[n_i][n_j] = self.player[1]
						elif n_i == 7 and new_board[n_i][n_j] == self.ai[0]:
							new_board[n_i][n_j] = self.ai[1]

						moves += [new_board]
					else:
						break

		return moves

	def getKills(self, board, i, j):
		"""Get all boards with (i,j)`s figure kills"""

		kills = []
		all_moves = self.up_moves + self.down_moves

		for d_i, d_j in all_moves:
			for mul in range(1, 8):
				if board[i][j] in ("w", "b") and mul != 1:
					break

				e_i, e_j = i + mul * d_i, j + mul * d_j
				n_i, n_j = i + (mul+1) * d_i, j + (mul+1) * d_j

				#ПОФИКСИТЬ, ДАМКА РУБИТ И ВСТАЁТ НА ЛЮБОЕ ПОЛЕ ПОСЛЕ СРУБЛЕННОЙ ФИГУРЫ, НО НЕ РАБОТАЕТ
				if board[i][j] == 0:
					return

				if self.isOnBoard(n_i, n_j) and self.isOnBoard(e_i, e_j):
					#Can't kill over self two figures
					if board[e_i][e_j] != 0 and board[e_i][e_j].lower() == board[i][j].lower():
						break
					
					#Can't kill over two figures
					if board[e_i][e_j] != 0 and board[n_i][n_j] != 0 and board[e_i][e_j] == board[n_i][n_j]:
						break

					if board[n_i][n_j] == 0 and board[e_i][e_j] != 0\
					and board[e_i][e_j].lower() != board[i][j].lower():
						while self.isOnBoard(n_i, n_j) and board[n_i][n_j] == 0:
							new_board = copy(board)
							
							new_board[e_i][e_j] = 0
							new_board[i][j], new_board[n_i][n_j] = new_board[n_i][n_j], new_board[i][j]
							
							if n_i == 0 and new_board[n_i][n_j] == self.player[0]:
								new_board[n_i][n_j] = self.player[1]
							elif n_i == 7 and new_board[n_i][n_j] == self.ai[0]:
								new_board[n_i][n_j] = self.ai[1]

							kills += [new_board]

							complicated_kills = self.getKills(new_board, n_i, n_j)
							if complicated_kills:
								kills += complicated_kills

							if new_board[n_i][n_j] in ("w", "b"):
								break

							n_i, n_j = n_i + d_i, n_j + d_j

						break
						
		return kills

	def isOnBoard(self, i, j):
		"""Check if board[i][j] exists"""

		return True if (0 <= i < 8 and 0 <= j < 8) else False
