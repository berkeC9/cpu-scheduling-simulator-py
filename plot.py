import sys
import os
import argparse  

# Check if matplotlib is installed
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("\n[ERROR] 'matplotlib' library is not installed.")
    print("Solution: Run 'pip install matplotlib' in the terminal.\n")
    sys.exit(1)

# Check if the compare module can be imported
try:
    from compare import run_comparison
except ImportError:
    print("\n[ERROR] compare.py file not found.")
    print("Please ensure compare.py is in the same directory as this file.\n")
    sys.exit(1)
def generate_graphs(input_file="processes.txt", quantum=3):
    print(f"Generating graphs using {input_file} (RR Quantum={quantum})...")
    
    # Retrieve data
    try:
        results = run_comparison(input_file, quantum=quantum)
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return

    if not results:
        print("Error: No data found to plot.")
        return

    # Create 'graphs' directory if it doesn't exist
    if not os.path.exists("graphs"):
        os.makedirs("graphs")

    names = [r['name'] for r in results]
    avg_wt = [r['wt'] for r in results]
    avg_tat = [r['tat'] for r in results]

    # Graph: Waiting Time
    plt.figure(figsize=(10, 6))
    plt.bar(names, avg_wt, color='skyblue', edgecolor='black')
    plt.xlabel('Algorithms')
    plt.ylabel('Average Waiting Time')
    plt.title(f'Average Waiting Time Comparison (RR q={quantum})') 
    plt.savefig('graphs/waiting.png')
    plt.close()
    print("-> graphs/waiting.png created.")

    # Graph: Turnaround Time 
    plt.figure(figsize=(10, 6))
    plt.bar(names, avg_tat, color='salmon', edgecolor='black')
    plt.xlabel('Algorithms')
    plt.ylabel('Average Turnaround Time')
    plt.title(f'Average Turnaround Time Comparison (RR q={quantum})') 
    plt.savefig('graphs/turnaround.png')
    plt.close()
    print("-> graphs/turnaround.png created.")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Generate Scheduling Graphs")
    # (Default: processes.txt)
    parser.add_argument("--input", default="processes.txt", help="Input file path")
    # (Default: 3)
    parser.add_argument("--quantum", type=int, default=3, help="Time quantum for Round Robin")
    args = parser.parse_args()
    generate_graphs(input_file=args.input, quantum=args.quantum)
    