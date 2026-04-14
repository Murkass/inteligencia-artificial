#!/usr/bin/env python3
"""
Script auxiliar para executar testes em bulk com presets de dificuldade
e visualizar resultados de testes anteriores.
"""

import json
import os
from datetime import datetime
from pathlib import Path
import glob

def colors(text, color_code):
    """Função para colorir texto no terminal"""
    return f"\033[{color_code}m{text}\033[0m"

class ResultsAnalyzer:
    """Analisa e compara resultados de testes anteriores"""
    
    @staticmethod
    def list_saved_results():
        """Lista todos os arquivos de resultados salvos"""
        results = sorted(glob.glob("test_results_*.json"))
        return results
    
    @staticmethod
    def load_results(filename):
        """Carrega resultados de um arquivo JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar {filename}: {e}")
            return None
    
    @staticmethod
    def print_results_table(results):
        """Imprime tabela formatada de resultados"""
        if not results or 'statistics' not in results:
            return
        
        stats = results['statistics']
        config = results['config']
        
        print(f"\n{'='*130}")
        print(f" Testes: {config['num_tests']} | Tabuleiro: {config['board_size']}x{config['board_size']} | Dificuldade: {config['initial_difficulty']}")
        print(f" Data: {results['timestamp'][:19]}")
        print(f"{'='*130}\n")
        
        print(f"{'Algoritmo':<20} {'Sucessos':<12} {'Falhas':<12} {'Min':<12} {'Médio':<12} {'Máx':<12} {'T.Min':<12} {'T.Méd':<12} {'T.Máx':<12}")
        print("-" * 130)
        
        for alg_name in sorted(stats.keys()):
            s = stats[alg_name]
            
            # Movimentos
            min_mov = f"{s['min_moves']:.0f}" if s['min_moves'] != '-' else '-'
            avg_mov = f"{s['avg_moves']:.1f}" if s['avg_moves'] != '-' else '-'
            max_mov = f"{s['max_moves']:.0f}" if s['max_moves'] != '-' else '-'
            
            # Tempos
            min_time = f"{s['min_time']:.4f}s" if isinstance(s['min_time'], (int, float)) else s['min_time']
            avg_time = f"{s['avg_time']:.4f}s" if isinstance(s['avg_time'], (int, float)) else s['avg_time']
            max_time = f"{s['max_time']:.4f}s" if isinstance(s['max_time'], (int, float)) else s['max_time']
            
            print(f"{alg_name:<20} {s['successes']:<12} {s['failures']:<12} {min_mov:<12} {avg_mov:<12} {max_mov:<12} {min_time:<12} {avg_time:<12} {max_time:<12}")
    
    @staticmethod
    def compare_results(files):
        """Compara múltiplos resultados de testes"""
        print(f"\n{'='*130}")
        print(f" COMPARAÇÃO DE RESULTADOS")
        print(f"{'='*130}\n")
        
        all_results = []
        for filename in files:
            results = ResultsAnalyzer.load_results(filename)
            if results:
                all_results.append((filename, results))
        
        if not all_results:
            print("Nenhum resultado para comparar.")
            return
        
        for filename, results in all_results:
            print(f"\n📊 {filename}")
            ResultsAnalyzer.print_results_table(results)

def run_isolated_test():
    """Menu para testar um algoritmo isolado"""
    from bulk_test import BulkTester, IsolatedAlgorithmTester
    
    algorithms = ['BFS', 'DFS', 'Hill Climbing', 'Simulated Annealing', 'A*', 'Greedy Search']
    
    print("\n" + "="*80)
    print(" TESTE ISOLADO - SELECIONE UM ALGORITMO")
    print("="*80 + "\n")
    
    for i, alg in enumerate(algorithms, 1):
        print(f"{i}. {alg}")
    
    print(f"\n0. Voltar")
    
    try:
        choice = int(input("\nEscolha um algoritmo: ").strip())
        
        if choice == 0:
            return
        elif 0 < choice <= len(algorithms):
            algorithm = algorithms[choice - 1]
            
            print(f"\n" + "="*80)
            print(f" CONFIGURAÇÃO - {algorithm}")
            print("="*80)
            
            try:
                num_tests = int(input("Quantidade de testes (10): ").strip() or "10")
                board_size = int(input("Tamanho do tabuleiro (5): ").strip() or "5")
                initial_difficulty = int(input("Dificuldade inicial (1): ").strip() or "1")
                
                if num_tests <= 0:
                    num_tests = 10
                if board_size <= 0:
                    board_size = 5
                if initial_difficulty <= 0:
                    initial_difficulty = 1
                
                print(f"\n✓ Iniciando teste isolado para {algorithm}...")
                
                tester = IsolatedAlgorithmTester(
                    algorithm_name=algorithm,
                    num_tests=num_tests,
                    board_size=board_size,
                    initial_difficulty=initial_difficulty
                )
                tester.run_full_test(save=True)
            
            except ValueError:
                print(colors("Entrada inválida.", "31"))
        else:
            print(colors("Opção inválida.", "31"))
    
    except ValueError:
        print(colors("Entrada inválida.", "31"))

def run_quick_test():
    """Menu para executar testes com presets"""
    from bulk_test import BulkTester
    
    print("\n" + "="*80)
    print(" PRESETS DE TESTES")
    print("="*80)
    print("""
{1} Fácil       - 10 testes, 3x3, dificuldade 1-5
{2} Normal      - 15 testes, 5x5, dificuldade 1-8
{3} Difícil     - 20 testes, 7x7, dificuldade 1-12
{4} Hardcore    - 25 testes, 10x10, dificuldade 1-15
{5} Customizado - Configuração manual
{6} Teste Isolado - Um algoritmo por vez
{7} Ver resultados anteriores
{0} Voltar
    """.format(*map(lambda x: colors(str(x), "34"), range(8))))
    
    choice = input("Escolha uma opção: ").strip()
    
    presets = {
        '1': {'num_tests': 10, 'board_size': 3, 'difficulty': 1, 'name': 'Fácil'},
        '2': {'num_tests': 15, 'board_size': 5, 'difficulty': 1, 'name': 'Normal'},
        '3': {'num_tests': 20, 'board_size': 7, 'difficulty': 1, 'name': 'Difícil'},
        '4': {'num_tests': 25, 'board_size': 10, 'difficulty': 1, 'name': 'Hardcore'},
    }
    
    if choice in presets:
        preset = presets[choice]
        print(f"\n✓ Iniciando teste {colors(preset['name'], '32')}...")
        
        tester = BulkTester(
            num_tests=preset['num_tests'],
            board_size=preset['board_size'],
            initial_difficulty=preset['difficulty']
        )
        tester.run_full_test(save=True)
    
    elif choice == '5':
        print("\n" + "="*80)
        print(" CONFIGURAÇÃO CUSTOMIZADA")
        print("="*80)
        
        try:
            num_tests = int(input("Quantidade de testes (padrão 20): ").strip() or "20")
            board_size = int(input("Tamanho do tabuleiro (padrão 5): ").strip() or "5")
            initial_difficulty = int(input("Dificuldade inicial (padrão 1): ").strip() or "1")
            
            if num_tests <= 0:
                num_tests = 20
            if board_size <= 0:
                board_size = 5
            if initial_difficulty <= 0:
                initial_difficulty = 1
            
            print(f"\n✓ Iniciando teste customizado...")
            
            tester = BulkTester(
                num_tests=num_tests,
                board_size=board_size,
                initial_difficulty=initial_difficulty
            )
            tester.run_full_test(save=True)
        
        except ValueError:
            print(colors("Entrada inválida.", "31"))
    
    elif choice == '6':
        run_isolated_test()
    
    elif choice == '7':
        results_files = ResultsAnalyzer.list_saved_results()
        
        if not results_files:
            print(colors("\nNenhum resultado salvo encontrado.", "31"))
            return
        
        print(f"\n{'='*80}")
        print(" RESULTADOS SALVOS")
        print("="*80 + "\n")
        
        for i, filename in enumerate(results_files, 1):
            print(f"{i}. {filename}")
        
        print(f"\n0. Voltar")
        
        try:
            choice = int(input("\nEscolha uma opção: ").strip())
            
            if 0 < choice <= len(results_files):
                results = ResultsAnalyzer.load_results(results_files[choice - 1])
                if results:
                    ResultsAnalyzer.print_results_table(results)
            elif choice == 0:
                return
            else:
                print(colors("Opção inválida.", "31"))
        
        except ValueError:
            print(colors("Entrada inválida.", "31"))

def main():
    """Menu principal"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        print("\n" + "="*80)
        print(colors(" TESTE EM BULK - SISTEMA AUXILIAR", "34"))
        print("="*80)
        print(f"""
{colors("1. Executar teste", "32")}
{colors("2. Ver resultados", "32")}
{colors("0. Sair", "31")}
        """)
        
        choice = input("Escolha uma opção: ").strip()
        
        if choice == "1":
            run_quick_test()
        elif choice == "2":
            results_files = ResultsAnalyzer.list_saved_results()
            if results_files:
                print(f"\n{'='*130}")
                print(" ÚLTIMOS RESULTADOS")
                print("="*130)
                ResultsAnalyzer.print_results_table(
                    ResultsAnalyzer.load_results(results_files[-1])
                )
            else:
                print(colors("\nNenhum resultado salvo encontrado.", "31"))
        elif choice == "0":
            print(colors("\nAté logo!", "32"))
            break
        else:
            print(colors("Opção inválida.", "31"))

if __name__ == "__main__":
    main()
