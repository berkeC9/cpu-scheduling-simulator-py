def run_priority_np(processes):
    """
    Non-Preemptive Priority Scheduling.
    Small integer = Higher priority (Assumed convention).
    """
    n = len(processes)
    all_procs = sorted([p.copy() for p in processes], key=lambda x: x['arrival'])
    
    completed = []
    gantt = []
    log = []
    current_time = 0
    context_switches = 0
    last_pid = None
    
    while len(completed) < n:
        ready = [p for p in all_procs if p['arrival'] <= current_time and p not in completed]
        
        if not ready:
            remaining = [p for p in all_procs if p not in completed]
            if remaining:
                current_time = min(p['arrival'] for p in remaining)
            continue
            
        # Sort by Priority -> Arrival -> PID
        ready.sort(key=lambda x: (x['priority'], x['arrival'], x['pid']))
        proc = ready[0]
        
        start = current_time
        end = start + proc['burst']
        
        if proc['start_time'] == -1: 
            proc['start_time'] = start
            
        log.append(f"t={start}: {proc['pid']} starts running (Priority: {proc['priority']})")
        
        if last_pid is not None and last_pid != proc['pid']:
            context_switches += 1
        last_pid = proc['pid']
        
        gantt.append({"pid": proc['pid'], "start": start, "end": end})
        proc['finish_time'] = end
        
        log.append(f"t={end}: {proc['pid']} completes")
        completed.append(proc)
        current_time = end

    return {"gantt": gantt, "history_log": log, "completed_processes": completed, "context_switches": context_switches}