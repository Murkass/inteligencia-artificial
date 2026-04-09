import time
import random
import math

class HillClimbing:
    """
    Algoritmo Hill Climbing (Subida de Encosta).
    
    Características:
    - Busca LOCAL: melhora o estado atual gradualmente
    - Ganancioso: sempre escolhe o melhor movimento possível
    - Rápido: baixa complexidade computacional
    - Incompleto: pode ficar preso em ótimos locais
    - Não garante solução global
    
    Como funciona:
    1. Começa no estado inicial
    2. Avalia todos os sucessores
    3. Escolhe o melhor (menor número de luzes ligadas)
    4. Se melhorou, move para esse estado
    5. Se não melhorou, para (plateau/ótimo local)
    """
    
    def solve(self, initial_state):
        """
        Resolve usando Hill Climbing
        
        Args:
            initial_state: Estado inicial
            
        Returns:
            Tupla (caminho, explorações, tempo)
        """
        start_time = time.time()
        
        current_state = initial_state
        path = []
        nodes_explored = 0
        
        while True:
            nodes_explored += 1
            
            # Se é objetivo, encontrou solução
            if current_state.is_goal():
                elapsed_time = time.time() - start_time
                return path, nodes_explored, elapsed_time
            
            # Avalia todos os sucessores
            successors = current_state.get_successors()
            
            best_state = None
            best_action = None
            best_heuristic = current_state.count_lights_on()
            
            # Encontra o melhor sucessor
            for next_state, action in successors:
                heuristic_value = next_state.count_lights_on()
                
                # Se é melhor que o atual, marca como melhor
                if heuristic_value < best_heuristic:
                    best_state = next_state
                    best_action = action
                    best_heuristic = heuristic_value
            
            # Se não encontrou melhoria, para (plateau ou ótimo local)
            if best_state is None:
                elapsed_time = time.time() - start_time
                return None, nodes_explored, elapsed_time  # Falhou
            
            # Move para o melhor estado
            current_state = best_state
            path.append(best_action)


class SimulatedAnnealing:
    """
    Algoritmo Simulated Annealing (Têmpera Simulada).
    
    Características:
    - Busca LOCAL com aceitação probabilística
    - Pode aceitar movimentos piores com certa probabilidade
    - Escapa de ótimos locais (ao contrário de Hill Climbing)
    - Temperatura decresce com o tempo (menos aceitação de piores)
    - Mais probabilidade de encontrar solução global
    
    Como funciona:
    1. Começa com temperatura alta
    2. Escolhe vizinho aleatório
    3. Se melhor, aceita sempre
    4. Se pior, aceita com probabilidade P = e^(-ΔE/T)
    5. Menor temperatura = menor probabilidade de aceitar piores
    6. Repete até temperatura muy baixa ou solução encontrada
    """
    
    def __init__(self, initial_temp=100, cooling_rate=0.98, iterations_per_temp=100, max_iterations=50000):
        """
        Args:
            initial_temp: Temperatura inicial
            cooling_rate: Taxa de resfriamento (0-1), mais próximo de 1 = mais lento
            iterations_per_temp: Iterações em cada temperatura
            max_iterations: Limite total de iterações
        """
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.iterations_per_temp = iterations_per_temp
        self.max_iterations = max_iterations
    
    def solve(self, initial_state):
        """
        Resolve usando Simulated Annealing
        
        Args:
            initial_state: Estado inicial
            
        Returns:
            Tupla (caminho, explorações, tempo)
        """
        start_time = time.time()
        
        current_state = initial_state
        best_state = initial_state
        best_path = []
        current_path = []
        
        nodes_explored = 0
        temperature = self.initial_temp
        total_iterations = 0
        
        while temperature > 0.01 and total_iterations < self.max_iterations:
            for _ in range(self.iterations_per_temp):
                total_iterations += 1
                nodes_explored += 1
                
                # Se current_state é objetivo, encontrou solução!
                if current_state.is_goal():
                    elapsed_time = time.time() - start_time
                    return current_path, nodes_explored, elapsed_time
                
                # Se best_state é objetivo, encontrou solução
                if best_state.is_goal():
                    elapsed_time = time.time() - start_time
                    return best_path, nodes_explored, elapsed_time
                
                # Escolhe um sucessor aleatório
                successors = current_state.get_successors()
                next_state, action = random.choice(successors)
                
                # Calcula diferença de qualidade (número de luzes)
                current_lights = current_state.count_lights_on()
                next_lights = next_state.count_lights_on()
                delta_e = next_lights - current_lights
                
                # Critério de aceitação
                # Sempre aceita se melhor (delta_e < 0)
                # Aceita se pior com probabilidade P = e^(-delta_e/T)
                if delta_e < 0 or random.random() < math.exp(-delta_e / max(temperature, 0.01)):
                    current_state = next_state
                    current_path.append(action)
                    
                    # Atualiza melhor estado encontrado
                    if current_state.count_lights_on() < best_state.count_lights_on():
                        best_state = current_state
                        best_path = current_path.copy()
                
                if total_iterations >= self.max_iterations:
                    break
            
            # Reduz temperatura
            temperature *= self.cooling_rate
        
        # Se melhor estado é objetivo, sucesso
        if best_state.is_goal():
            elapsed_time = time.time() - start_time
            return best_path, nodes_explored, elapsed_time
        
        # Falhou - retorna melhor que encontrou
        elapsed_time = time.time() - start_time
        return None, nodes_explored, elapsed_time