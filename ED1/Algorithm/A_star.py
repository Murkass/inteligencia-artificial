import heapq
import time

class AStar:
    """
    Algoritmo A* (A-Star).
    
    Características:
    - Busca INFORMADA: usa heurística + custo do caminho
    - f(n) = g(n) + h(n)
      - g(n): custo do caminho até agora
      - h(n): heurística estimada até o objetivo
    - Encontra solução ÓTIMA (se heurística é admissível)
    - Melhor que Greedy Search e BFS
    - Usa MENOS explorações que BFS
    
    Como funciona:
    1. Coloca estado inicial em fila com prioridade (f-value)
    2. Retira estado com menor f-value
    3. Se for objetivo, encontrou solução ótima
    4. Se não, gera sucessores e adiciona à fila com suas f-values
    5. Repete até encontrar solução
    """
    
    def __init__(self, heuristic='lights'):
        """
        Args:
            heuristic: Qual heurística usar
                      'lights': Número de luzes acesas (padrão)
                      'manhattan': Distância de Manhattan modificada
        """
        self.heuristic = heuristic
    
    def _estimate_cost(self, state):
        """Cálcula heurística h(n)"""
        if self.heuristic == 'manhattan':
            return state.manhattan_distance_to_goal()
        else:  # 'lights'
            return state.count_lights_on()
    
    def solve(self, initial_state):
        """
        Resolve o problema usando A*
        
        Args:
            initial_state: Estado inicial do problema
            
        Returns:
            Tupla (caminho, explorações, tempo)
            caminho: lista de movimentos para resolver
            explorações: número de estados explorados
            tempo: tempo gasto
        """
        start_time = time.time()
        
        # Fila com prioridade: (f_value, counter, estado, caminho, g_value)
        # counter evita comparação de estados (que pode gerar erro)
        open_set = []
        counter = 0
        
        h_initial = self._estimate_cost(initial_state)
        heapq.heappush(open_set, (h_initial, counter, initial_state, [], 0))
        counter += 1
        
        # Conjunto de estados já visitados
        visited = set()
        nodes_explored = 0
        
        while open_set:
            f_value, _, current_state, path, g_value = heapq.heappop(open_set)
            
            # Usa tupla do estado para comparação
            state_tuple = tuple(tuple(row) for row in current_state.board)
            if state_tuple in visited:
                continue
            
            visited.add(state_tuple)
            nodes_explored += 1
            
            # Verifica se é o objetivo
            if current_state.is_goal():
                elapsed_time = time.time() - start_time
                return path, nodes_explored, elapsed_time
            
            # Gera sucessores
            successors = current_state.get_successors()
            
            for next_state, action in successors:
                next_tuple = tuple(tuple(row) for row in next_state.board)
                
                # Se não foi visitado, adiciona à fila
                if next_tuple not in visited:
                    new_g = g_value + 1  # Cada movimento custa 1
                    h_value = self._estimate_cost(next_state)
                    f_value = new_g + h_value
                    
                    new_path = path + [action]
                    heapq.heappush(open_set, (f_value, counter, next_state, new_path, new_g))
                    counter += 1
        
        # Nenhuma solução encontrada
        elapsed_time = time.time() - start_time
        return None, nodes_explored, elapsed_time