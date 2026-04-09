import time

class DFS:
    """
    Algoritmo de Busca em Profundidade (Depth-First Search).
    
    Características:
    - Explora o máximo possível em cada ramo antes de backtracking
    - Consome menos memória que BFS (pilha vs fila)
    - NÃO garante solução ótima (pode encontrar solução com mais movimentos)
    - Completo: encontra solução se existir (com limite de profundidade)
    
    Como funciona:
    1. Adiciona o estado inicial à pilha
    2. Retira o último estado da pilha (LIFO)
    3. Se for o objetivo, retorna o caminho
    4. Se não, gera sucessores e adiciona à pilha
    5. Repete até encontrar solução ou pilha vazia
    """
    
    def __init__(self, max_depth=20, timeout=10):
        """
        Args:
            max_depth: Profundidade máxima para limitar busca infinita (padrão: 20)
            timeout: Tempo máximo em segundos para a busca (padrão: 10s)
        """
        self.max_depth = max_depth
        self.timeout = timeout
    
    def solve(self, initial_state):
        """
        Resolve o problema usando DFS com limite de profundidade
        
        Args:
            initial_state: Estado inicial do problema
            
        Returns:
            Tupla (caminho, explorações, tempo)
            caminho: lista de movimentos para resolver
            explorações: número de estados explorados
            tempo: tempo gasto
        """
        start_time = time.time()
        
        # Pilha de estados: [(estado, caminho_até_aqui), ...]
        stack = [(initial_state, [])]
        
        # Conjunto de estados já visitados
        visited = set()
        nodes_explored = 0
        
        while stack:
            current_state, path = stack.pop()
            
            # Verifica timeout para evitar busca infinita
            elapsed = time.time() - start_time
            if elapsed > self.timeout:
                # Timeout atingido - interrompe busca
                return None, nodes_explored, elapsed
            
            # Limita a profundidade da busca
            if len(path) > self.max_depth:
                continue
            
            # Usa tupla do estado para comparação em visited
            state_tuple = tuple(tuple(row) for row in current_state.board)
            if state_tuple in visited:
                continue
            
            visited.add(state_tuple)
            nodes_explored += 1
            
            # Verifica se é o objetivo
            if current_state.is_goal():
                elapsed_time = time.time() - start_time
                return path, nodes_explored, elapsed_time
            
            # Gera sucessores e adiciona à pilha (em ordem reversa para explorar ordem correta)
            successors = current_state.get_successors()
            for next_state, action in reversed(successors):
                new_path = path + [action]
                stack.append((next_state, new_path))
        
        # Nenhuma solução encontrada
        elapsed_time = time.time() - start_time
        return None, nodes_explored, elapsed_time