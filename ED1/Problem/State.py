from copy import deepcopy

class State:
    """
    Classe que representa um estado do jogo Light Out.
    Encapsula o tabuleiro e oferece métodos para gerar sucessores e verificar objetivo.
    """
    
    def __init__(self, board, board_size):
        self.board = deepcopy(board)
        self.board_size = board_size
    
    def __eq__(self, other):
        """Dois estados são iguais se têm o mesmo tabuleiro"""
        if not isinstance(other, State):
            return False
        return self.board == other.board
    
    def __hash__(self):
        """Permite usar State em conjuntos (set) e dicionários"""
        return hash(tuple(tuple(row) for row in self.board))
    
    def __str__(self):
        """Representação visual do tabuleiro"""
        result = ""
        for row in self.board:
            result += ' '.join(str(cell) for cell in row) + '\n'
        return result
    
    def is_goal(self):
        """Verifica se é o estado objetivo (tudo desligado)"""
        for row in self.board:
            for cell in row:
                if cell != 0:
                    return False
        return True
    
    def get_successors(self):
        """
        Gera todos os estados sucessores possíveis.
        Cada movimento consiste em clicar em uma posição (x, y)
        """
        successors = []
        
        for x in range(self.board_size):
            for y in range(self.board_size):
                # Cria uma cópia do tabuleiro
                new_board = deepcopy(self.board)
                
                # Toggle a luz na posição (x, y)
                new_board[x][y] = 1 - new_board[x][y]
                
                # Toggle as luzes adjacentes
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                        new_board[nx][ny] = 1 - new_board[nx][ny]
                
                new_state = State(new_board, self.board_size)
                successors.append((new_state, (x, y)))
        
        return successors
    
    def count_lights_on(self):
        """
        Heurística: conta quantas luzes estão ligadas.
        Útil para Hill Climbing e A*.
        """
        count = 0
        for row in self.board:
            for cell in row:
                count += cell
        return count
    
    def manhattan_distance_to_goal(self):
        """
        Heurística alternativa: soma das distâncias de Manhattan
        das luzes ligadas até o canto mais próximo.
        """
        total = 0
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 1:
                    # Distância até o ponto mais próximo
                    min_dist = min(i, j, self.board_size - 1 - i, self.board_size - 1 - j)
                    total += min_dist
        return total
