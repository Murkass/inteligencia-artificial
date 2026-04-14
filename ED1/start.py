from Problem.LightOut_Setup import LightOutSetup
from Problem.State import State
from Algorithm.BFS import BFS
from Algorithm.DFS import DFS
from Algorithm.LocalSearch import HillClimbing, SimulatedAnnealing
from Algorithm.A_star import AStar
from Algorithm.GreedySearch import GreedySearch

'''
codigos:
31 - vermelho
32 - verde
33 - amarelo
34 - azul
35 - magenta
36 - ciano
'''
def colors(text, color_code):
    """Função para colorir texto no terminal"""
    return f"\033[{color_code}m{text}\033[0m"

class Menu:
    def __init__(self, board_size=3, initial_moves=1):
        self.board_size = board_size
        self.initial_moves = initial_moves
        self.setup = LightOutSetup(board_size, initial_moves)
        self.initial_state = State(self.setup.board, board_size)

    def print_header(self):
        print("\n" + "="*80)
        print(colors(" Bem-vindo ao Teste de Algoritmos de IA para Light Out ", "34"))
        print("="*80)
        print(f"Objetivo: Apagar todas as luzes {colors('(deixar matriz com zeros)', '33')}")
        print("="*80 + "\n")

    def print_board_initial(self):
        print("Estado inicial do tabuleiro:")
        print(self.initial_state)
        print(f"Luzes ligadas: {colors(self.initial_state.count_lights_on(), '31')}")
    
    def regenerate_board(self, board_size=None):
        """Regenera um novo tabuleiro aleatório, podendo alterar o tamanho"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        if board_size is not None:
            self.board_size = board_size
        self.setup.regenerate(self.initial_moves, self.board_size)
        self.initial_state = State(self.setup.board, self.board_size)
        print("\n" + colors("Novo tabuleiro gerado!", "32"))
        self.print_board_initial()

    def print_solution(self, path, explored, elapsed_time):
        """Imprime a solução encontrada"""
        if path is None:
            print(colors("Nenhuma solução encontrada!", "31"))
            print(f"Estados explorados: {colors(explored, '33')}")
            print(f"Tempo gasto: {colors(f'{elapsed_time:.4f}s', '33')}\n")
            return
        
        print(colors("SOLUÇÃO ENCONTRADA!", "32"))
        print(f"Número de movimentos: {colors(len(path), '33')}")
        print(f"Estados explorados: {colors(explored, '33')}")
        print(f"Tempo gasto: {colors(f'{elapsed_time:.4f}s', '33')}")
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
        import os
        self.print_header()
        self.print_board_initial()
        play = True
        while play:
            print("\n" + "="*50)
            print(colors("ALGORITMOS DISPONÍVEIS:", "32"))
            print("="*50)
            print(f"""   
{colors("1. Busca em Largura (BFS)", "34")}
   - Encontra solução ÓTIMA (menos movimentos)
   - Usa muita memória
   - Mais lento

{colors("2. Busca em Profundidade (DFS)", "34")}
   - Usa menos memória
   - Mais rápido, mas solução pode não ser ótima
   - Limite de profundidade: 50

{colors("3. Hill Climbing (Busca Local)", "34")}
   - Muito rápido
   - Pode ficar preso em ótimos locais
   - Não garante solução

{colors("4. Simulated Annealing (Têmpera Simulada)", "34")}
   - Escapa de ótimos locais
   - Probabilisticamente encontra solução
   - Mais lento que Hill Climbing

{colors("5. A* (A-Star)", "34")}
   - Busca informada: usa heurística + custo
   - Encontra solução ÓTIMA
   - Mais eficiente que BFS

{colors("6. Greedy Search (Busca Gulosa)", "34")}
   - Busca informada: usa apenas heurística
   - Rápido, mas não garante ótimo
   - Menos explorações que A*

{colors("7. Regenerar Tabuleiro (Novo Jogo)", "34")}
   - Gera um novo tabuleiro aleatório
   - Mantém o tamanho e número de movimentos

{colors("0. Sair", "34")}
            """)
            print("="*50)
            
            try:
                alg_choice = input("Escolha um algoritmo (0-7): ").strip()
                if alg_choice == "7":
                    # Permite ao usuário escolher novo tamanho
                    size_input = input("Novo tamanho do tabuleiro (pressione Enter para manter "+str(self.board_size)+"): ").strip()
                    if size_input:
                        try:
                            new_size = int(size_input)
                            self.regenerate_board(board_size=new_size)
                        except ValueError:
                            print(colors("Tamanho inválido. Mantendo o atual.", "31"))
                            self.regenerate_board()
                    else:
                        self.regenerate_board()
                    continue
                # Limpa terminal após cada clique/ação
                os.system('cls' if os.name == 'nt' else 'clear')
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
                    case "0":
                        print("\nObrigado por usar o teste de algoritmos!")
                        print("Até logo!")
                        play = False
                    case _:
                        print(colors("Opção inválida. Por favor, escolha 0-7.", "31"))
                        continue
            except Exception as e:
                print(colors(f"Erro: {e}", "31"))
                print(colors("Por favor, tente novamente.", "31"))

if __name__ == "__main__":
    # Você pode ajustar o tamanho do tabuleiro e movimentos iniciais aqui
    menu = Menu(board_size=10, initial_moves=3)
    menu.start()