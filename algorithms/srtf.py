def run_srtf(processes):
    # Deep copy and initialize
    active_procs = [p.copy() for p in processes]
    # To track arrivals correctly
    active_procs.sort(key=lambda x: x['arrival'])
    
    current_time = 0
    completed_count = 0
    n = len(processes)
    
    gantt = []
    log = []
    context_switches = 0
    
    last_proc = None
    # We will simulate second by second
    
    while completed_count < n:
        # Find ready processes
        ready = [p for p in active_procs if p['arrival'] <= current_time and p['remaining_time'] > 0]
        
        # Check for new arrivals just for logging purposes
        for p in active_procs:
            if p['arrival'] == current_time:
                log.append(f"t={current_time}: {p['pid']} arrives")

        if not ready:
            current_time += 1
            continue
            
        # Selection: Shortest Remaining Time -> Arrival -> PID
        ready.sort(key=lambda x: (x['remaining_time'], x['arrival'], x['pid']))
        current_proc = ready[0]
        
        # Detect Context Switch / Preemption
        if last_proc != current_proc:
            if last_proc is not None and last_proc['remaining_time'] > 0:
                log.append(f"t={current_time}: {current_proc['pid']} preempts {last_proc['pid']}")
                context_switches += 1
            elif last_proc is not None:
                context_switches += 1 # Standard switch after completion
            
            # First run check
            if current_proc['start_time'] == -1:
                current_proc['start_time'] = current_time
                log.append(f"t={current_time}: {current_proc['pid']} starts running")
            elif last_proc and last_proc != current_proc:
                 log.append(f"t={current_time}: {current_proc['pid']} resumes")
                 
        last_proc = current_proc
        
        # Execute for 1 unit
        current_proc['remaining_time'] -= 1
        
        # Gantt update (optimize later to merge continuous blocks)
        if gantt and gantt[-1]['pid'] == current_proc['pid'] and gantt[-1]['end'] == current_time:
            gantt[-1]['end'] += 1
        else:
            gantt.append({"pid": current_proc['pid'], "start": current_time, "end": current_time + 1})
            
        current_time += 1
        
        # Completion check
        if current_proc['remaining_time'] == 0:
            current_proc['finish_time'] = current_time
            completed_count += 1
            log.append(f"t={current_time}: {current_proc['pid']} completes")
            # Don't set last_proc to None, so we can detect switch on next loop

    return {
        "gantt": gantt, 
        "history_log": log, 
        "completed_processes": [p for p in active_procs if p['remaining_time'] == 0],
        "context_switches": context_switches
    }