def run_sjf(processes):
    n = len(processes)
    # Master list sorted by arrival
    all_procs = sorted([p.copy() for p in processes], key=lambda x: (x['arrival'], x['pid']))
    
    completed = []
    gantt = []
    log = []
    
    current_time = 0
    context_switches = 0
    last_pid = None
    
    while len(completed) < n:
        # 1. Filter processes that have arrived and are not finished
        ready_queue = [p for p in all_procs if p['arrival'] <= current_time and p not in completed]
        
        if not ready_queue:
            # CPU Idle: Jump to next arrival
            remaining_procs = [p for p in all_procs if p not in completed]
            if remaining_procs:
                current_time = min(p['arrival'] for p in remaining_procs)
            continue

        # 2. Select process with shortest burst (Tie-break: PID)
        # Note: We sort by burst, then pid
        ready_queue.sort(key=lambda x: (x['burst'], x['pid']))
        selected_proc = ready_queue[0]
        
        # Log arrival if it's the first time we see it technically? 
        # (Simplified: usually we log arrivals as they happen globally, but here we log actions)

        # 3. Execution (Non-preemptive: runs to completion)
        start = current_time
        end = start + selected_proc['burst']
        
        # Log Start
        if selected_proc['start_time'] == -1:
            selected_proc['start_time'] = start
        log.append(f"t={start}: {selected_proc['pid']} starts running")
        
        # Context Switch
        if last_pid is not None and last_pid != selected_proc['pid']:
            context_switches += 1
        last_pid = selected_proc['pid']
        
        # Update Data
        gantt.append({"pid": selected_proc['pid'], "start": start, "end": end})
        selected_proc['finish_time'] = end
        
        log.append(f"t={end}: {selected_proc['pid']} completes")
        
        completed.append(selected_proc)
        current_time = end

    return {
        "gantt": gantt,
        "history_log": log,
        "completed_processes": completed,
        "context_switches": context_switches
    }