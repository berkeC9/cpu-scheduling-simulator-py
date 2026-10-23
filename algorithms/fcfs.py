def run_fcfs(processes):
    # Sort by arrival time first, then PID
    process_queue = sorted([p.copy() for p in processes], key=lambda x: (x['arrival'], x['pid']))
    
    current_time = 0
    gantt_chart = []
    log = []
    completed = []
    context_switches = 0
    last_pid = None

    for proc in process_queue:
        # If CPU is idle until process arrives
        if current_time < proc['arrival']:
            current_time = proc['arrival']

        # Log arrival (technically happened earlier, but we process it now)
        log.append(f"t={proc['arrival']}: {proc['pid']} arrives")

        start_t = current_time
        end_t = start_t + proc['burst']
        
        # Start Running
        log.append(f"t={start_t}: {proc['pid']} starts running")
        
        # Update metrics
        proc['start_time'] = start_t
        proc['finish_time'] = end_t
        
        # Check Context Switch
        if last_pid is not None and last_pid != proc['pid']:
            context_switches += 1
        last_pid = proc['pid']

        # Update Gantt
        gantt_chart.append({"pid": proc['pid'], "start": start_t, "end": end_t})
        
        # Completion
        log.append(f"t={end_t}: {proc['pid']} completes")
        completed.append(proc)
        current_time = end_t

    return {
        "gantt": gantt_chart,
        "history_log": log,
        "completed_processes": completed,
        "context_switches": context_switches
    }