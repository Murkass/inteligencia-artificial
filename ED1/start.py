from Problem.LightOut_Setup import LightOutSetup
from Problem.State import State
from Algorithm.BFS import BFS
from Algorithm.DFS import DFS
from Algorithm.LocalSearch import HillClimbing, SimulatedAnnealing
from Algorithm.A_star import AStar
from Algorithm.GreedySearch import GreedySearch

class Menu:
    def __init__(self, board_size=10, initial_moves=3):
        self.board_size = board_size
        self.initial_moves = initial_moves
        self.setup = LightOutSetup(board_size, initial_moves)
        self.initial_state = State(self.setup.board, board_size)

    def print_header(self):
        print("\n" + "="*80)
        print("Bem-vindo ao Teste de Algoritmos de IA para Light Out")
        print("="*80)
        print("Objetivo: Apagar todas as luzes (deixar matriz com zeros)")
        print("="*80 + "\n")

    def print_board_initial(self):
        print("Estado inicial do tabuleiro:")
        print(self.initial_state)
        print(f"Luzes ligadas: {self.initial_state.count_lights_on()}")
    
    def regenerate_board(self):
        """Regenera um novo tabuleiro aleatório"""
        self.setup.regenerate(self.initial_moves)
        self.initial_state = State(self.setup.board, self.board_size)
        print("\n✅ Novo tabuleiro gerado!")
        self.print_board_initial()

    def print_solution(self, path, explored, elapsed_time):
        """Imprime a solução encontrada"""
        if path is None:
            print("❌ Nenhuma solução encontrada!")
            print(f"Estados explorados: {explored}")
            print(f"Tempo gasto: {elapsed_time:.4f}s\n")
            return
        
        print("✅ SOLUÇÃO ENCONTRADA!")
        print(f"Número de movimentos: {len(path)}")
        print(f"Estados explorados: {explored}")
        print(f"Tempo gasto: {elapsed_time:.4f}s")
        print(f"\nMovimentos (posições clicadas):")
        for i, (x, y) in enumerate(path, 1):
            print(f"  {i}. Clicar em ({x}, {y})")
        print()

    def run_algorithm(self, algorithm_name, algorithm):
        """Executa um algoritmo e mostra resultado"""
        print(f"\nExecutando {algorithm_name}...")
        print("-" * 50)
        
        path, explored, elapsed_time = algorithm.solve(self.initial_state)
        self.print_solution(path, explored, elapsed_time)

    def start(self):
        self.print_header()
        self.print_board_initial()
        
        play = True
        while play:
            print("\n" + "="*50)
            print("ALGORITMOS DISPONÍVEIS:")
            print("="*50)
            print("""
1. Busca em Largura (BFS)
   - Encontra solução ÓTIMA (menos movimentos)
   - Usa muita memória
   - Mais lento

2. Busca em Profundidade (DFS)
   - Usa menos memória
   - Mais rápido, mas solução pode não ser ótima
   - Limite de profundidade: 50

3. Hill Climbing (Busca Local)
   - Muito rápido
   - Pode ficar preso em ótimos locais
   - Não garante solução

4. Simulated Annealing (Têmpera Simulada)
   - Escapa de ótimos locais
   - Probabilisticamente encontra solução
   - Mais lento que Hill Climbing

5. A* (A-Star)
   - Busca informada: usa heurística + custo
   - Encontra solução ÓTIMA
   - Mais eficiente que BFS

6. Greedy Search (Busca Gulosa)
   - Busca informada: usa apenas heurística
   - Rápido, mas não garante ótimo
   - Menos explorações que A*

7. Regenerar Tabuleiro (Novo Jogo)
   - Gera um novo tabuleiro aleatório
   - Mantém o tamanho e número de movimentos

0. Sair
            """)
            print("="*50)
            
            try:
                alg_choice = input("Escolha um algoritmo (0-7): ").strip()
                
                match alg_choice:
                    case "1":
                        bfs = BFS()
                        self.run_algorithm("BFS (Breadth-First Search)", bfs)
                    
                    case "2":
                        dfs = DFS(max_depth=20, timeout=10)
                        self.run_algorithm("DFS (Depth-First Search)", dfs)
                    
                    case "3":
                        hc = HillClimbing()
                        self.run_algorithm("Hill Climbing", hc)
                    
                    case "4":
                        sa = SimulatedAnnealing(initial_temp=100, cooling_rate=0.98, iterations_per_temp=100)
                        self.run_algorithm("Simulated Annealing", sa)
                    
                    case "5":
                        astar = AStar(heuristic='lights')
                        self.run_algorithm("A* (A-Star)", astar)
                    
                    case "6":
                        greedy = GreedySearch(heuristic='lights')
                        self.run_algorithm("Greedy Search", greedy)
                    
                    case "7":
                        self.regenerate_board()
                    
                    case "0":
                        print("\nObrigado por usar o teste de algoritmos!")
                        print("Até logo! 👋")
                        play = False
                    
                    case _:
                        print("❌ Opção inválida. Por favor, escolha 0-7.")
                        continue
                
            except Exception as e:
                print(f"❌ Erro: {e}")
                print("Por favor, tente novamente.")

if __name__ == "__main__":
    # Você pode ajustar o tamanho do tabuleiro e movimentos iniciais aqui
    menu = Menu(board_size=5, initial_moves=3)
    menu.start()