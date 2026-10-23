import argparse
import sys
from utils.parser import load_process_file
from utils.statistics import calculate_metrics, print_stats_table
from utils.gantt import display_gantt_chart

# Import algorithms from separate modules
from algorithms.fcfs import run_fcfs
from algorithms.sjf import run_sjf
from algorithms.srtf import run_srtf
from algorithms.rr import run_round_robin
from algorithms.priority_np import run_priority_np
from algorithms.priority_p import run_priority_p

def main():
    # Define Arguments with using argparse
    parser = argparse.ArgumentParser(description="CPU Scheduling Simulator 2025")
    
    parser.add_argument("--input", required=True, help="Input file path (e.g., processes.txt)")
    parser.add_argument("--algo", required=True, 
                        choices=["FCFS", "SJF", "SRTF", "RR", "PRIO_NP", "PRIO_P"],
                        help="Scheduling algorithm to use")
    parser.add_argument("--quantum", type=int, help="Time quantum for Round Robin")

    args = parser.parse_args()

    # Read the Input File
    try:
        process_list = load_process_file(args.input)
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.")
        sys.exit(1)

    # Select and Run the Algorithm
    print("------------------------------------------------------------------------------------------------------")
    print(f"Simulation Started: {args.algo} ")
    
    sim_result = {}

    if args.algo == "FCFS":
        sim_result = run_fcfs(process_list)
    elif args.algo == "SJF":
        sim_result = run_sjf(process_list)
    elif args.algo == "SRTF":
        sim_result = run_srtf(process_list)
    elif args.algo == "PRIO_NP":
        sim_result = run_priority_np(process_list)
    elif args.algo == "PRIO_P":
        sim_result = run_priority_p(process_list)
    elif args.algo == "RR":
        if not args.quantum:
            print("Error: --quantum is required for RR algorithm.")
            sys.exit(1)
        sim_result = run_round_robin(process_list, args.quantum)

    # Print Results (Gantt Chart, Logs, Statistics)
    
    # Gantt Chart
    print("\nGantt Chart: ")
    display_gantt_chart(sim_result['gantt'])

    # Execution Log
    print("\nExecution Log: ")
    for log_entry in sim_result['history_log']:
        print(log_entry)

    # Statistics
    print("\nFinal Statistics: ")
    stats = calculate_metrics(sim_result['completed_processes'])
    print_stats_table(stats, sim_result['context_switches'])

if __name__ == "__main__":
    main()