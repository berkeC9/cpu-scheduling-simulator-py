def calculate_metrics(completed_processes):
    """
    Calculates TAT, WT, and RT for all processes.
    TAT = Completion Time - Arrival Time
    WT = Turnaround Time - Burst Time
    RT = First Start Time - Arrival Time
    """
    # Sort processes by PID for a cleaner table
    sorted_procs = sorted(completed_processes, key=lambda x: x['pid'])
    
    total_tat = 0
    total_wt = 0
    total_rt = 0
    n = len(sorted_procs)

    stats = []

    for p in sorted_procs:
        # Calculate basic metrics
        tat = p['finish_time'] - p['arrival']
        wt = tat - p['burst']
        rt = p['start_time'] - p['arrival']

        # ensure waiting time is not negative
        if wt < 0: wt = 0
        
        total_tat += tat
        total_wt += wt
        total_rt += rt

        stats.append({
            "pid": p['pid'],
            "arrival": p['arrival'],
            "burst": p['burst'],
            "finish": p['finish_time'],
            "tat": tat,
            "wt": wt,
            "rt": rt
        })

    averages = {
        "avg_tat": total_tat / n if n > 0 else 0,
        "avg_wt": total_wt / n if n > 0 else 0,
        "avg_rt": total_rt / n if n > 0 else 0
    }
    
    return {"process_stats": stats, "averages": averages}

def print_stats_table(stats_data, context_switches):
    """Prints per-process and summary scheduling metrics in a formatted table."""
    print(f"{'PID':<5} {'Arr':<5} {'Burst':<7} {'Compl':<7} {'TAT':<5} {'WT':<5} {'RT':<5}")
    print("-" * 50)
    
    for p in stats_data['process_stats']:
        print(f"{p['pid']:<5} {p['arrival']:<5} {p['burst']:<7} "
              f"{p['finish']:<7} {p['tat']:<5} {p['wt']:<5} {p['rt']:<5}")

    avgs = stats_data['averages']
    print("\nSummary: ")
    print(f"Average Turnaround Time : {avgs['avg_tat']:.2f}")
    print(f"Average Waiting Time    : {avgs['avg_wt']:.2f}")
    print(f"Average Response Time   : {avgs['avg_rt']:.2f}")
    print(f"Total Context Switches  : {context_switches}")