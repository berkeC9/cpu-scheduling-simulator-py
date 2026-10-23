import sys
import argparse
# Import utility modules
from utils.parser import load_process_file
from utils.statistics import calculate_metrics

# Import algorithms from the modular structure
from algorithms.fcfs import run_fcfs
from algorithms.sjf import run_sjf
from algorithms.srtf import run_srtf
from algorithms.rr import run_round_robin
from algorithms.priority_np import run_priority_np
from algorithms.priority_p import run_priority_p

def run_comparison(input_file="processes.txt", quantum=3):
    """
    Runs all algorithms on the given input file and prints a comparison table.
    Returns the results dictionary for plotting purposes.
    """
    print(f"--- Loading processes from {input_file} ---")
    
    try:
        # Load the process file (catch errors if file is missing)
        original_processes = load_process_file(input_file)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return []

    # List of scenarios to test
    # (Display Name, Function, Parameter)
    scenarios = [
        ("FCFS", run_fcfs, None),
        ("SJF", run_sjf, None),
        ("SRTF", run_srtf, None),
        (f"RR (q={quantum})", run_round_robin, quantum),
        ("PRIO_NP", run_priority_np, None),
        ("PRIO_P", run_priority_p, None)
    ]

    # Print table header
    print(f"\n{'Algorithm':<15} {'Avg TAT':<10} {'Avg WT':<10} {'Avg RT':<10} {'Ctx Switch':<10}")
    print("-" * 60)

    results_for_graph = []

    for name, func, param in scenarios:
        # Create a fresh copy of processes for each run.
        # This ensures previous runs dont affect the current one.
        proc_copy = [p.copy() for p in original_processes]

        # Execute the selected algorithm
        if param:
            output = func(proc_copy, param)
        else:
            output = func(proc_copy)

        # Compute statistics
        stats = calculate_metrics(output['completed_processes'])
        avgs = stats['averages']
        cs_count = output['context_switches']

        # Print the result row to the table
        print(f"{name:<15} {avgs['avg_tat']:<10.2f} {avgs['avg_wt']:<10.2f} "
              f"{avgs['avg_rt']:<10.2f} {cs_count:<10}")

        # Store results for plotting graphs
        results_for_graph.append({
            "name": name,
            "tat": avgs['avg_tat'],
            "wt": avgs['avg_wt']
        })

    return results_for_graph

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Compare Algorithms")
    parser.add_argument("--input", default="processes.txt", help="Input file path")
    parser.add_argument("--quantum", type=int, default=3, help="Time quantum for Round Robin")
    args = parser.parse_args()
    run_comparison(args.input, args.quantum)