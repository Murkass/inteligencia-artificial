from collections import deque
import time

class BFS:
    """
    Algoritmo de Busca em Largura (Breadth-First Search).
    
    Características:
    - Explora todos os estados no nível atual antes de ir para o próximo
    - Garante encontrar a solução com menos movimentos (ótimo)
    - Consome muita memória (armazena todos os estados em fila)
    - Completo: sempre encontra solução se existir
    
    Como funciona:
    1. Adiciona o estado inicial à fila
    2. Retira o primeiro estado da fila
    3. Se for o objetivo, retorna o caminho
    4. Se não, gera sucessores e adiciona à fila
    5. Repete até encontrar solução ou fila vazia
    """
    
    def solve(self, initial_state):
        """
        Resolve o problema usando BFS
        
        Args:
            initial_state: Estado inicial do problema
            
        Returns:
            Tupla (caminho, explorações, tempo)
            caminho: lista de movimentos para resolver
            explorações: número de estados explorados
            tempo: tempo gasto
        """
        start_time = time.time()
        
        # Fila de estados a explorar: [(estado, caminho_até_aqui), ...]
        queue = deque([(initial_state, [])])
        
        # Conjunto de estados já visitados (para não repetir)
        visited = {initial_state}
        
        nodes_explored = 0
        
        while queue:
            current_state, path = queue.popleft()
            nodes_explored += 1
            
            # Verifica se é o objetivo
            if current_state.is_goal():
                elapsed_time = time.time() - start_time
                return path, nodes_explored, elapsed_time
            
            # Gera sucessores
            for next_state, action in current_state.get_successors():
                if next_state not in visited:
                    visited.add(next_state)
                    new_path = path + [action]
                    queue.append((next_state, new_path))
        
        # Nenhuma solução encontrada
        elapsed_time = time.time() - start_time
        return None, nodes_explored, elapsed_time