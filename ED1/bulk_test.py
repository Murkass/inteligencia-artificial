import json
import os
import signal
from datetime import datetime
from pathlib import Path
from Problem.LightOut_Setup import LightOutSetup
from Problem.State import State
from Algorithm.BFS import BFS
from Algorithm.DFS import DFS
from Algorithm.LocalSearch import HillClimbing, SimulatedAnnealing
from Algorithm.A_star import AStar
from Algorithm.GreedySearch import GreedySearch

# Caminho para pasta de resultados
RESULTS_DIR = Path(__file__).parent / "test_results"
RESULTS_DIR.mkdir(exist_ok=True)

class BulkTester:
    """
    Sistema de testes em bulk para os algoritmos de IA.
    Testa múltiplos algoritmos nos mesmos tabuleiros com dificuldade crescente.
    """
    
    def __init__(self, num_tests=20, board_size=5, initial_difficulty=1):
        self.num_tests = num_tests
        self.board_size = board_size
        self.initial_difficulty = initial_difficulty
        self.test_boards = []
        self.results = {}
        self.interrupted = False
        self.current_algorithm = None
        self.current_board_id = None
        self.test_start_time = None
        self.algorithm_timeout = 30  # 30 segundos por algoritmo
        signal.signal(signal.SIGINT, self._interrupt_handler)
    
    def _interrupt_handler(self, signum, frame):
        """Handler para Ctrl+C - force exit do loop"""
        self.interrupted = True
        print(f"\n\n{'='*80}")
        print(" ⚠️  Teste interrompido pelo usuário - Salvando dados...")
        print("="*80)
        # Lança exceção para forçar saída
        raise KeyboardInterrupt("Interrupção do usuário")
    
        
    def generate_test_boards(self):
        """Gera tabuleiros com dificuldade crescente"""
        print(f"\n{'='*80}")
        print(f" Gerando {self.num_tests} tabuleiros com dificuldade crescente")
        print(f"{'='*80}\n")
        
        self.test_boards = []
        for i in range(1, self.num_tests + 1):
            # Dificuldade aumenta: 1º tabuleiro tem 1 movimento, último tem mais
            difficulty = self.initial_difficulty + (i - 1)
            
            setup = LightOutSetup(self.board_size, difficulty)
            initial_state = State(setup.board, self.board_size)
            
            # Armazena como cópia profunda para não alterar
            self.test_boards.append({
                'id': i,
                'board': [row[:] for row in setup.board],
                'state': initial_state,
                'difficulty': difficulty,
                'lights_on': initial_state.count_lights_on()
            })
            
            print(f"  Tabuleiro {i:2d}: Dificuldade {difficulty} | Luzes ligadas: {initial_state.count_lights_on()}")
    
    def run_tests(self):
        """Executa todos os algoritmos em todos os tabuleiros"""
        print(f"\n{'='*80}")
        print(f" Executando testes")
        print(f"{'='*80}\n")
        
        algorithms = {
            'BFS': BFS(),
            'DFS': DFS(max_depth=50, timeout=10),
            'Hill Climbing': HillClimbing(),
            'Simulated Annealing': SimulatedAnnealing(initial_temp=100, cooling_rate=0.98, iterations_per_temp=100),
            'A*': AStar(heuristic='lights'),
            'Greedy Search': GreedySearch(heuristic='lights')
        }
        
        # Inicializa resultados
        for alg_name in algorithms.keys():
            self.results[alg_name] = {
                'times': [],
                'moves': [],
                'explored': [],
                'successes': 0,
                'failures': 0
            }
        
        # Executa testes
        total_tests = len(self.test_boards) * len(algorithms)
        current_test = 0
        
        for board_data in self.test_boards:
            if self.interrupted:
                break
            
            print(f"\nTabuleiro {board_data['id']} (Dificuldade: {board_data['difficulty']}, Luzes: {board_data['lights_on']})")
            print("-" * 80)
            
            for alg_name, algorithm in algorithms.items():
                if self.interrupted:
                    break
                
                current_test += 1
                self.current_algorithm = alg_name
                self.current_board_id = board_data['id']
                print(f"  [{current_test:3d}/{total_tests}] {alg_name:20s} ", end="", flush=True)
                
                try:
                    # Cria novo estado para este algoritmo (para não compartilhar objeto)
                    test_state = State(board_data['board'], self.board_size)
                    
                    # Executa algoritmo
                    path, explored, elapsed_time = algorithm.solve(test_state)
                    
                    if path is not None:
                        moves = len(path)
                        self.results[alg_name]['successes'] += 1
                        self.results[alg_name]['moves'].append(moves)
                        print(f"✓ Movimentos: {moves:3d} | Explorados: {explored:6d} | Tempo: {elapsed_time:.4f}s")
                    else:
                        self.results[alg_name]['failures'] += 1
                        print(f"✗ Falhou     | Explorados: {explored:6d} | Tempo: {elapsed_time:.4f}s")
                    
                    self.results[alg_name]['times'].append(elapsed_time)
                    self.results[alg_name]['explored'].append(explored)
                    
                except Exception as e:
                    self.results[alg_name]['failures'] += 1
                    print(f"✗ Erro: {str(e)[:40]}")
    
    
    def calculate_statistics(self):
        """Calcula estatísticas para cada algoritmo"""
        stats = {}
        
        for alg_name, data in self.results.items():
            stats[alg_name] = {}
            
            # Movimentos
            if data['moves']:
                stats[alg_name]['min_moves'] = min(data['moves'])
                stats[alg_name]['avg_moves'] = sum(data['moves']) / len(data['moves'])
                stats[alg_name]['max_moves'] = max(data['moves'])
            else:
                stats[alg_name]['min_moves'] = '-'
                stats[alg_name]['avg_moves'] = '-'
                stats[alg_name]['max_moves'] = '-'
            
            # Tempos
            stats[alg_name]['min_time'] = min(data['times']) if data['times'] else '-'
            stats[alg_name]['avg_time'] = sum(data['times']) / len(data['times']) if data['times'] else '-'
            stats[alg_name]['max_time'] = max(data['times']) if data['times'] else '-'
            
            # Sucessos e Falhas
            stats[alg_name]['successes'] = data['successes']
            stats[alg_name]['failures'] = data['failures']
        
        return stats
    
    def print_report(self):
        """Imprime relatório detalhado dos testes"""
        stats = self.calculate_statistics()
        
        print(f"\n{'='*120}")
        print(f" RELATÓRIO DE TESTES EM BULK")
        if self.interrupted:
            print(f" ⚠️  TESTE INTERROMPIDO (Dados parciais)")
        print(f"{'='*120}")
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Tabuleiros testados: {self.num_tests}")
        print(f"Tamanho do tabuleiro: {self.board_size}x{self.board_size}")
        print(f"Dificuldade inicial: {self.initial_difficulty}")
        if self.interrupted:
            print(f"Último teste: Tabuleiro {self.current_board_id} - {self.current_algorithm}")
        print(f"{'='*120}\n")
        
        # Tabela de comparação
        print(f"{'Algoritmo':<20} {'Sucessos':<12} {'Falhas':<12} {'Min.Mov':<12} {'Méd.Mov':<12} {'Máx.Mov':<12}")
        print("-" * 120)
        
        for alg_name in sorted(stats.keys()):
            s = stats[alg_name]
            min_mov = f"{s['min_moves']:.0f}" if s['min_moves'] != '-' else '-'
            avg_mov = f"{s['avg_moves']:.1f}" if s['avg_moves'] != '-' else '-'
            max_mov = f"{s['max_moves']:.0f}" if s['max_moves'] != '-' else '-'
            
            print(f"{alg_name:<20} {s['successes']:<12} {s['failures']:<12} {min_mov:<12} {avg_mov:<12} {max_mov:<12}")
        
        print("\n" + "-" * 120)
        print(f"{'Algoritmo':<20} {'Min.Tempo':<15} {'Méd.Tempo':<15} {'Máx.Tempo':<15}")
        print("-" * 120)
        
        for alg_name in sorted(stats.keys()):
            s = stats[alg_name]
            min_time = f"{s['min_time']:.6f}s" if s['min_time'] != '-' else '-'
            avg_time = f"{s['avg_time']:.6f}s" if s['avg_time'] != '-' else '-'
            max_time = f"{s['max_time']:.6f}s" if s['max_time'] != '-' else '-'
            
            print(f"{alg_name:<20} {min_time:<15} {avg_time:<15} {max_time:<15}")
        
        print("\n" + "="*120)
    
    def save_results(self, filename=None):
        """Salva resultados em JSON para análise posterior"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            status = "_interrupted" if self.interrupted else ""
            filename = f"test_results_{self.board_size}x{self.board_size}_{timestamp}{status}.json"
        
        filepath = RESULTS_DIR / filename
        stats = self.calculate_statistics()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'config': {
                'num_tests': self.num_tests,
                'board_size': self.board_size,
                'initial_difficulty': self.initial_difficulty
            },
            'status': {
                'completed': not self.interrupted,
                'interrupted': self.interrupted,
                'last_algorithm': self.current_algorithm,
                'last_board_id': self.current_board_id
            },
            'statistics': stats,
            'raw_results': self.results
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Resultados salvos em: test_results/{filename}")
        if self.interrupted:
            print(f"  Último teste: Tabuleiro {self.current_board_id} - {self.current_algorithm}")
        return str(filepath)
    
    def run_full_test(self, save=True):
        """Executa teste completo"""
        try:
            self.generate_test_boards()
            self.run_tests()
            self.print_report()
            
            if save:
                self.save_results()
            
            return True
        except KeyboardInterrupt:
            print("\n✓ Salvando dados acumulados...")
            self.interrupted = True
            if save:
                self.save_results()
            print("\n✓ Dados salvos com sucesso!")
            return False
        except Exception as e:
            print(f"\n✗ Erro durante os testes: {str(e)}")
            import traceback
            traceback.print_exc()
            # Salva resultados mesmo com erro
            if save:
                self.save_results()
            return False
        finally:
            # Remove o handler de signal
            signal.signal(signal.SIGINT, signal.default_int_handler)

class IsolatedAlgorithmTester:
    """
    Testa um único algoritmo isoladamente nos mesmos tabuleiros.
    Útil para algoritmos que podem travar ou demorar muito.
    """
    
    def __init__(self, algorithm_name, num_tests=10, board_size=5, initial_difficulty=1):
        self.algorithm_name = algorithm_name
        self.num_tests = num_tests
        self.board_size = board_size
        self.initial_difficulty = initial_difficulty
        self.test_boards = []
        self.results = []
        self.interrupted = False
        self.current_board_id = None
        signal.signal(signal.SIGINT, self._interrupt_handler)
    
    def _interrupt_handler(self, signum, frame):
        """Handler para Ctrl+C - force exit"""
        self.interrupted = True
        print(f"\n\n{'='*80}")
        print(" ⚠️  Teste isolado interrompido pelo usuário - Salvando dados...")
        print("="*80)
        # Lança exceção para forçar saída
        raise KeyboardInterrupt("Interrupção do usuário")
    
    
    def get_algorithm(self):
        """Retorna instância do algoritmo solicitado"""
        algorithms = {
            'BFS': BFS(),
            'DFS': DFS(max_depth=50, timeout=10),
            'Hill Climbing': HillClimbing(),
            'Simulated Annealing': SimulatedAnnealing(initial_temp=100, cooling_rate=0.98, iterations_per_temp=100),
            'A*': AStar(heuristic='lights'),
            'Greedy Search': GreedySearch(heuristic='lights')
        }
        return algorithms.get(self.algorithm_name)
    
    def generate_test_boards(self):
        """Gera tabuleiros com dificuldade crescente"""
        print(f"\n{'='*80}")
        print(f" Gerando {self.num_tests} tabuleiros para {self.algorithm_name}")
        print(f"{'='*80}\n")
        
        self.test_boards = []
        for i in range(1, self.num_tests + 1):
            difficulty = self.initial_difficulty + (i - 1)
            
            setup = LightOutSetup(self.board_size, difficulty)
            initial_state = State(setup.board, self.board_size)
            
            self.test_boards.append({
                'id': i,
                'board': [row[:] for row in setup.board],
                'state': initial_state,
                'difficulty': difficulty,
                'lights_on': initial_state.count_lights_on()
            })
            
            print(f"  Tabuleiro {i:2d}: Dificuldade {difficulty} | Luzes ligadas: {initial_state.count_lights_on()}")
    
    def run_tests(self):
        """Executa testes para um único algoritmo"""
        print(f"\n{'='*80}")
        print(f" Executando testes para {self.algorithm_name}")
        print(f"{'='*80}\n")
        
        algorithm = self.get_algorithm()
        self.results = {
            'times': [],
            'moves': [],
            'explored': [],
            'successes': 0,
            'failures': 0,
            'details': []
        }
        
        for board_data in self.test_boards:
            if self.interrupted:
                break
            
            self.current_board_id = board_data['id']
            print(f"\nTabuleiro {board_data['id']} (Dificuldade: {board_data['difficulty']}, Luzes: {board_data['lights_on']})")
            print("-" * 80)
            
            try:
                test_state = State(board_data['board'], self.board_size)
                print(f"  Executando {self.algorithm_name}...", end=" ", flush=True)
                
                path, explored, elapsed_time = algorithm.solve(test_state)
                
                if path is not None:
                    moves = len(path)
                    self.results['successes'] += 1
                    self.results['moves'].append(moves)
                    print(f"✓ {moves:3d}mov | {explored:6d}exp | {elapsed_time:.4f}s")
                    self.results['details'].append({
                        'board_id': board_data['id'],
                        'success': True,
                        'moves': moves,
                        'explored': explored,
                        'time': elapsed_time
                    })
                else:
                    self.results['failures'] += 1
                    print(f"✗ Falhou | {explored:6d}exp | {elapsed_time:.4f}s")
                    self.results['details'].append({
                        'board_id': board_data['id'],
                        'success': False,
                        'explored': explored,
                        'time': elapsed_time
                    })
                
                self.results['times'].append(elapsed_time)
                self.results['explored'].append(explored)
                
            except Exception as e:
                self.results['failures'] += 1
                print(f"✗ Erro: {str(e)[:40]}")
                self.results['details'].append({
                    'board_id': board_data['id'],
                    'success': False,
                    'error': str(e)
                })
    
    def print_report(self):
        """Imprime relatório detalhado"""
        print(f"\n{'='*120}")
        print(f" RELATÓRIO - TESTE ISOLADO: {self.algorithm_name}")
        if self.interrupted:
            print(f" ⚠️  TESTE ISOLADO INTERROMPIDO (Dados parciais)")
        print(f"{'='*120}")
        print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Tabuleiros testados: {self.num_tests}")
        print(f"Tamanho do tabuleiro: {self.board_size}x{self.board_size}")
        print(f"Dificuldade inicial: {self.initial_difficulty}")
        if self.interrupted:
            print(f"Último tabuleiro: {self.current_board_id}")
        print(f"{'='*120}\n")
        
        # Resumo geral
        print(f"{'Status':<30} {'Quantidade':<20}")
        print("-" * 120)
        print(f"{'Sucessos':<30} {self.results['successes']:<20}")
        print(f"{'Falhas':<30} {self.results['failures']:<20}")
        print(f"{'Total':<30} {self.num_tests:<20}\n")
        
        # Estatísticas de movimentos
        if self.results['moves']:
            print(f"{'MOVIMENTOS':<30}")
            print("-" * 120)
            print(f"{'Mínimo':<30} {min(self.results['moves']):<20.0f}")
            print(f"{'Médio':<30} {sum(self.results['moves']) / len(self.results['moves']):<20.1f}")
            print(f"{'Máximo':<30} {max(self.results['moves']):<20.0f}\n")
        else:
            print(f"{'MOVIMENTOS':<30} Sem sucessos\n")
        
        # Estatísticas de tempo
        if self.results['times']:
            print(f"{'TEMPO (segundos)':<30}")
            print("-" * 120)
            print(f"{'Mínimo':<30} {min(self.results['times']):<20.6f}")
            print(f"{'Médio':<30} {sum(self.results['times']) / len(self.results['times']):<20.6f}")
            print(f"{'Máximo':<30} {max(self.results['times']):<20.6f}\n")
        
        print("="*120)
    
    def save_results(self, filename=None):
        """Salva resultados em JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            alg_short = self.algorithm_name.replace(" ", "_").replace("*", "star")
            status = "_interrupted" if self.interrupted else ""
            filename = f"isolated_{alg_short}_{self.board_size}x{self.board_size}_{timestamp}{status}.json"
        
        filepath = RESULTS_DIR / filename
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'config': {
                'algorithm': self.algorithm_name,
                'num_tests': self.num_tests,
                'board_size': self.board_size,
                'initial_difficulty': self.initial_difficulty
            },
            'status': {
                'completed': not self.interrupted,
                'interrupted': self.interrupted,
                'last_board_id': self.current_board_id
            },
            'statistics': {
                'successes': self.results['successes'],
                'failures': self.results['failures'],
                'min_moves': min(self.results['moves']) if self.results['moves'] else '-',
                'avg_moves': sum(self.results['moves']) / len(self.results['moves']) if self.results['moves'] else '-',
                'max_moves': max(self.results['moves']) if self.results['moves'] else '-',
                'min_time': min(self.results['times']) if self.results['times'] else '-',
                'avg_time': sum(self.results['times']) / len(self.results['times']) if self.results['times'] else '-',
                'max_time': max(self.results['times']) if self.results['times'] else '-',
            },
            'details': self.results['details']
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Resultados salvos em: test_results/{filename}")
        if self.interrupted:
            print(f"  Último tabuleiro testado: {self.current_board_id}")
        return str(filepath)
    
    def run_full_test(self, save=True):
        """Executa teste isolado completo"""
        try:
            self.generate_test_boards()
            self.run_tests()
            self.print_report()
            
            if save:
                self.save_results()
            
            return True
        except KeyboardInterrupt:
            print("\n✓ Salvando dados acumulados...")
            self.interrupted = True
            if save:
                self.save_results()
            print("\n✓ Dados salvos com sucesso!")
            return False
        except Exception as e:
            print(f"\n✗ Erro durante os testes: {str(e)}")
            import traceback
            traceback.print_exc()
            # Salva resultados mesmo com erro
            if save:
                self.save_results()
            return False
        finally:
            # Remove o handler de signal
            signal.signal(signal.SIGINT, signal.default_int_handler)


def main():
    """Menu interativo para testes em bulk"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + "="*80)
    print(" SISTEMA DE TESTES EM BULK PARA ALGORITMOS DE IA - LIGHT OUT")
    print("="*80)
    print("\nConfigurações:")
    
    # Número de testes
    try:
        num_tests = int(input("\nQuantidade de testes por algoritmo (padrão 20): ").strip() or "20")
        if num_tests <= 0:
            num_tests = 20
    except ValueError:
        num_tests = 20
    
    # Tamanho do tabuleiro
    try:
        board_size = int(input("Tamanho do tabuleiro (padrão 5): ").strip() or "5")
        if board_size <= 0:
            board_size = 5
    except ValueError:
        board_size = 5
    
    # Dificuldade inicial
    try:
        initial_difficulty = int(input("Dificuldade inicial em movimentos (padrão 1): ").strip() or "1")
        if initial_difficulty <= 0:
            initial_difficulty = 1
    except ValueError:
        initial_difficulty = 1
    
    print("\n" + "="*80)
    print("⏳ Iniciando testes... (Isto pode levar alguns minutos)")
    print("="*80)
    
    # Executa testes
    tester = BulkTester(
        num_tests=num_tests,
        board_size=board_size,
        initial_difficulty=initial_difficulty
    )
    
    tester.run_full_test(save=True)

if __name__ == "__main__":
    main()
