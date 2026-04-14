#!/usr/bin/env python3
"""
Script para comparar e visualizar resultados de testes em bulk.
"""

import json
import glob
from pathlib import Path
from datetime import datetime

def colors(text, color_code):
    """Função para colorir texto no terminal"""
    return f"\033[{color_code}m{text}\033[0m"

# Caminho para pasta de resultados
RESULTS_DIR = Path(__file__).parent / "test_results"

class ResultsComparator:
    """Compara múltiplas sessões de testes"""
    
    @staticmethod
    def get_all_results():
        """Recebe todos os arquivos de resultados"""
        if not RESULTS_DIR.exists():
            return []
        
        files = sorted(RESULTS_DIR.glob("*.json"))
        results = []
        
        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    results.append({
                        'filename': filepath.name,
                        'data': data,
                        'timestamp': datetime.fromisoformat(data['timestamp'])
                    })
            except Exception as e:
                print(f"Erro ao carregar {filepath.name}: {e}")
        
        return results
    
    @staticmethod
    def print_single_result(result):
        """Imprime resultado único em formato legível"""
        data = result['data']
        config = data['config']
        stats = data['statistics']
        
        print(f"\n{'='*140}")
        print(f" 📊 {result['filename']}")
        print(f"{'='*140}")
        print(f"Data: {data['timestamp'][:19]}")
        print(f"Config: {config['num_tests']} testes | {config['board_size']}x{config['board_size']} | Dif. inicial: {config['initial_difficulty']}")
        print(f"{'='*140}\n")
        
        # Cabeçalho
        print(f"{'Algoritmo':<20} {'Suc/Fal':<12} {'Min Mov':<12} {'Méd Mov':<12} {'Máx Mov':<12} {'Mín Tempo':<15} {'Méd Tempo':<15} {'Máx Tempo':<15}")
        print("-" * 140)
        
        # Dados
        for alg_name in sorted(stats.keys()):
            s = stats[alg_name]
            
            suc_fal = f"{s['successes']}/{s['failures']}"
            min_mov = f"{s['min_moves']:.0f}" if s['min_moves'] != '-' else '-'
            avg_mov = f"{s['avg_moves']:.1f}" if s['avg_moves'] != '-' else '-'
            max_mov = f"{s['max_moves']:.0f}" if s['max_moves'] != '-' else '-'
            
            min_time = f"{s['min_time']:.5f}s" if isinstance(s['min_time'], (int, float)) else s['min_time']
            avg_time = f"{s['avg_time']:.5f}s" if isinstance(s['avg_time'], (int, float)) else s['avg_time']
            max_time = f"{s['max_time']:.5f}s" if isinstance(s['max_time'], (int, float)) else s['max_time']
            
            print(f"{alg_name:<20} {suc_fal:<12} {min_mov:<12} {avg_mov:<12} {max_mov:<12} {min_time:<15} {avg_time:<15} {max_time:<15}")
    
    @staticmethod
    def compare_multiple(results):
        """Compara múltiplos resultados"""
        if not results:
            print(colors("Nenhum resultado para comparar.", "31"))
            return
        
        print(f"\n{'='*140}")
        print(colors(" COMPARAÇÃO DE SESSÕES DE TESTES", "34"))
        print(f"{'='*140}\n")
        
        print(f"{'Sessão':<5} {'Config':<25} {'BFS':<15} {'A*':<15} {'Greedy':<15} {'HC':<15} {'SA':<15} {'DFS':<15}")
        print("-" * 140)
        
        for i, result in enumerate(results, 1):
            data = result['data']
            config = data['config']
            stats = data['statistics']
            
            config_str = f"{config['board_size']}x{config['board_size']}-{config['num_tests']}t"
            
            # Para cada algoritmo, pega taxa de sucesso
            bfs_success = f"({stats['BFS']['successes']}/{config['num_tests']})"
            astar_success = f"({stats['A*']['successes']}/{config['num_tests']})"
            greedy_success = f"({stats['Greedy Search']['successes']}/{config['num_tests']})"
            hc_success = f"({stats['Hill Climbing']['successes']}/{config['num_tests']})"
            sa_success = f"({stats['Simulated Annealing']['successes']}/{config['num_tests']})"
            dfs_success = f"({stats['DFS']['successes']}/{config['num_tests']})"
            
            print(f"{i:<5} {config_str:<25} {bfs_success:<15} {astar_success:<15} {greedy_success:<15} {hc_success:<15} {sa_success:<15} {dfs_success:<15}")
        
        print(f"\n{colors('Taxa de sucesso (Sucessos/Total)', '32')}\n")

def main():
    """Menu principal"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        results = ResultsComparator.get_all_results()
        
        print("\n" + "="*80)
        print(colors(" COMPARADOR DE RESULTADOS", "34"))
        print("="*80)
        
        if not results:
            print(colors("\nNenhum resultado salvo encontrado!", "31"))
            print("Execute 'python bulk_test.py' ou 'python test_runner.py' para gerar resultados.")
            break
        
        print(f"\nResultados disponíveis: {len(results)}\n")
        
        for i, result in enumerate(results, 1):
            config = result['data']['config']
            print(f"{i}. {result['filename']} ({config['board_size']}x{config['board_size']}, {config['num_tests']} testes)")
        
        print(f"\n0. Comparar todos")
        print(f"-1. Sair")
        
        try:
            choice = int(input("\nEscolha uma opção: ").strip())
            
            if choice == 0:
                ResultsComparator.compare_multiple(results)
                input("\nPressione Enter para continuar...")
            elif 0 < choice <= len(results):
                ResultsComparator.print_single_result(results[choice - 1])
                input("\nPressione Enter para continuar...")
            elif choice == -1:
                print(colors("\nAté logo!", "32"))
                break
            else:
                print(colors("Opção inválida.", "31"))
        
        except ValueError:
            print(colors("Entrada inválida.", "31"))
        
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
