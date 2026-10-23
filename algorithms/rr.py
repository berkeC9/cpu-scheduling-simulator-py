from collections import deque


def run_round_robin(processes, time_quantum):
    """
    Preemptive Round Robin (RR) Scheduling with a fixed time quantum.
    """
    # Initialize FIFO ready queue
    job_queue = deque()
    # Pointer to track upcoming process arrivals
    proc_idx = 0
    n = len(processes)
    # Sort by arrival time, then PID (alphabetical) for deterministic tie-breaking
    sorted_procs = sorted([p.copy() for p in processes], key=lambda x: (x['arrival'], x['pid']))

    current_time = 0
    completed_jobs = []
    gantt_data = []
    history_log = []
    context_switches = 0

    # Track the last executed process for context switch counting
    last_process_id = None

    # Main simulation loop
    while len(completed_jobs) < n:
        # 1. Enqueue all newly arrived processes up to current_time
        while proc_idx < n and sorted_procs[proc_idx]['arrival'] <= current_time:
            new_proc = sorted_procs[proc_idx]
            history_log.append(f"t={new_proc['arrival']}: {new_proc['pid']} arrives")
            job_queue.append(new_proc)
            proc_idx += 1

        # 2. Handle CPU idle state when ready queue is empty
        if not job_queue:
            # Advance clock to the next process arrival
            if proc_idx < n:
                current_time = sorted_procs[proc_idx]['arrival']
            continue

        # 3. Dequeue the next ready process
        current_proc = job_queue.popleft()

        # Check for context switch
        if last_process_id is not None and current_proc['pid'] != last_process_id:
            context_switches += 1

        # Record start_time on first execution for response time calculation
        if current_proc['start_time'] == -1:
            current_proc['start_time'] = current_time
            history_log.append(f"t={current_time}: {current_proc['pid']} starts running")
        elif last_process_id != current_proc['pid']:
            # Log resume event if the process was previously preempted
            history_log.append(f"t={current_time}: {current_proc['pid']} running (resumed)")

        last_process_id = current_proc['pid']

        # 4. Determine execution slice (time quantum vs. remaining burst time)
        exec_duration = min(time_quantum, current_proc['remaining_time'])

        # Record Gantt chart segment
        gantt_data.append({
            "pid": current_proc['pid'],
            "start": current_time,
            "end": current_time + exec_duration
        })

        # Advance simulation clock and decrement remaining burst time
        current_time += exec_duration
        current_proc['remaining_time'] -= exec_duration

        # 5. Enqueue any processes that arrived during this execution slice
        while proc_idx < n and sorted_procs[proc_idx]['arrival'] <= current_time:
            new_p = sorted_procs[proc_idx]
            history_log.append(f"t={new_p['arrival']}: {new_p['pid']} arrives")
            job_queue.append(new_p)
            proc_idx += 1

        # 6. Check whether the process completed or needs to be re-queued
        if current_proc['remaining_time'] == 0:
            current_proc['finish_time'] = current_time
            completed_jobs.append(current_proc)
            history_log.append(f"t={current_time}: {current_proc['pid']} completes")
        else:
            # Time quantum expired; append process to the back of the ready queue
            history_log.append(f"t={current_time}: Time quantum expired for {current_proc['pid']}")
            job_queue.append(current_proc)

    return {
        "gantt": gantt_data,
        "history_log": history_log,
        "completed_processes": completed_jobs,
        "context_switches": context_switches
    }
