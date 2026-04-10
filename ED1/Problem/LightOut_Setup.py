from random import randint

class LightOutSetup:
    def __init__(self, board_size, initial_moves):
        self.board_size = board_size
        self.board = self.createBoard(initial_moves)

    def createBoard(self, moves):
        board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        for _ in range(moves):
            x, y = randint(0, self.board_size - 1), randint(0, self.board_size - 1)
            board = self.toggle(x, y, board)
        return board

    def toggle(self, x, y, board):
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            board[x][y] = 1 - board[x][y]  # Toggle the light
        else:
            print("Invalid position. Please choose a position within the board.")
            return False
        # Toggle adjacent lights
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                board[nx][ny] = 1 - board[nx][ny]
        return board

    def checkBoard(self):
        for row in self.board:
            for cell in row:
                if cell != 0:
                    return False
        return True
        
    def drawBoard(self):
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print()
    
    def regenerate(self, initial_moves=None, board_size=None):
        """Regenera um novo tabuleiro aleatório.
        Pode receber novo tamanho de tabuleiro e novo número de movimentos iniciais."""
        if board_size is not None:
            self.board_size = board_size
        if initial_moves is None:
            initial_moves = 2
        self.board = self.createBoard(initial_moves)
        return self.board